import lark.exceptions
from lark import Lark as _Lark, Transformer as _Transformer

from jufo_pptx_script.easypresentation.EasyTextformatter import EasyTextformatter
from jufo_pptx_script.templater.Template import Template as _Template
from jufo_pptx_script.templater.ImagePropertiesParser import ImageInfoParser as _ImageInfoParser
from dataclasses import dataclass as _dt
from typing import Any, Dict
import sys
import inspect
import os

@_dt
class ParseResult:
    result: str


@_dt
class ImageParseResult(ParseResult):
    scale: None or int or (int, int)
    raw: str


# Lark transformer to flatten and map the syntax
class _TemplateTransformer(_Transformer):
    def __init__(self, template_collection: _Template, data: Dict[str, Any]):
        super().__init__()
        self.template_collection = template_collection._get_registered()
        self.data = data

    def function_call(self, args):
        func_name = args[0]
        args = args[1] if len(args) > 1 else {}

        # Checks if any key is part of both
        duplicated_keys = list(filter(lambda k: k in self.data,args))
        if len(duplicated_keys) > 0:
            print(f"\rWarning: Argument(s) '{', '.join(duplicated_keys)}' for function '{func_name}' is duplicated (Given from the user script and from the interpreted text). ",file=sys.stderr)

        # Builds the dict with the arguments
        args2pass = {
            **self.data, # Data passed from the script
            **args       # Data passed from the text-call
        }

        # Retrieves the function that got registered using the template
        func = self.template_collection.get(func_name, None)

        # Ensures the function exists
        if func is None:
            raise ValueError(f"Function {func_name} is not defined")

        # TODO: make better
        # Checks if the function shall be ignored
        is_ignored = func == 'ignored_func'

        if not is_ignored:
            # Checks that the keys from the function and args2pass dict match
            sig = inspect.signature(func)


            # Gets all parameter's in general
            func_params = sig.parameters.values()
            func_params_names = list(map(lambda param: param.name, func_params))

            # Gets all parameters that are required to run the function but are missing
            missing_func_params = filter(lambda param: param.default is param.empty and param.name not in args2pass, func_params)
            missing_func_params_names = list(map(lambda param: param.name, missing_func_params))

            # Gets the parameters that have been submitted but are not part of the function
            none_func_params_names = list(filter(lambda name: name not in func_params_names, args2pass.keys()))

            # Checks that all required parameters are given
            if len(missing_func_params_names) > 0:
                raise ValueError(f"Function '{func_name}' requires the parameter(s) '{', '.join(missing_func_params_names)}', which are/were not given.")

            # Filters out any parameters that the function does not have any use for
            args2pass = {key: value for key, value in args2pass.items() if key in func_params_names}
        try:
            result = "" if is_ignored else func(**args2pass)

            if isinstance(result, EasyTextformatter):
                return result

            return str(result)
        except Exception as err:
            raise ValueError(f"Function '{func_name}' run into an error while executing: {err}")

    def args(self, args):
        return args[0]

    def template(self, args):
        return args[0]

    def function_arg(self, args):
        return {key: value for key, value in args}

    def function_name(self, name):
        return str(name[0])

    def argument(self, arg):
        return arg

    def argument_name(self, arg):
        return str(arg[0]).strip()

    def argument_value(self, arg):
        return str(arg[0]).strip()

    def text(self, text):
        return str(text[0])


class TemplateApplier:

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'template_grammar.lark')
        with open(path, "r") as file:
            grammar = file.read()

        self.__parser = _Lark(grammar, start='start', parser='lalr')
        self.__img_parser = _ImageInfoParser()

    def parse_with_image_properties(self, template: _Template, data: Any, text: str)\
            -> ImageParseResult:
        # Parses first for templates
        res = self.parse_as_string(template, data, text)

        path, scale = self.__img_parser.parse(res)

        return ImageParseResult(path, scale, res)

    def parse_as_string(self, template: _Template, data: Dict[str, Any], text: str) -> str:
        return ''.join(self.parse(template, data, text))

    def parse(self, template: _Template, data: Dict[str, Any], text: str) -> [str or EasyTextformatter]:
        if len(text) <= 0:
            return []

        try:
            tree = self.__parser.parse(text)
            transformer = _TemplateTransformer(template, data)
            results = transformer.transform(tree)

            # Creates a flat list of the results
            output = []
            for item in results.children:
                if isinstance(item, str) or isinstance(item, EasyTextformatter):
                    output.append(item)
                else:
                    output.append(item.children[0])

            return output
        except lark.exceptions.UnexpectedInput as err:
            raise ValueError(f"Unexpected input while parsing for templates:\n'{err.get_context(text)}'")
            pass
        except Exception as err:
            raise ValueError(f"Unknown error occurred. Please check your input: '{text}' ({err})")
