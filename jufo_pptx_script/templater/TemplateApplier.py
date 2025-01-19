import lark.exceptions
from lark import Lark as _Lark, Transformer as _Transformer
from jufo_pptx_script.templater.Template import Template as _Template
from jufo_pptx_script.templater.ImagePropertiesParser import ImageInfoParser as _ImageInfoParser
from dataclasses import dataclass as _dt
from typing import Any

@_dt
class ParseResult:
    result: str


@_dt
class ImageParseResult(ParseResult):
    scale: None or int or (int, int)
    raw: str


# Lark transformer to flatten and map the syntax
class _TemplateTransformer(_Transformer):
    def __init__(self, template_collection: _Template, data: Any):
        super().__init__()
        self.template_collection = template_collection._get_registered()
        self.data = data

    def function_call(self, args):
        func_name = args[0]
        args = args[1] if len(args) > 1 else []

        if func_name not in self.template_collection:
            raise ValueError(f"Function {func_name} is not defined")
        try:
            return str(self.template_collection[func_name](self.data, args))
        except Exception as err:
            raise ValueError(f"Function '{func_name}' run into an error while executing: {err}")

    def args(self, args):
        return str(args[0])

    def template(self, args):
        return args[1] if len(args) >= 2 else ""

    def function_arg(self, args):
        return args

    def function_name(self, name):
        return str(name[0])

    def argument(self, arg):
        return str(arg[0]).strip()

    def text(self, text):
        return str(text[0])


class TemplateApplier:

    def __init__(self):
        with open("jufo_pptx_script/templater/template_grammar.lark", "r") as file:
            grammar = file.read()

        self.__parser = _Lark(grammar, start='start', parser='lalr')
        self.__img_parser = _ImageInfoParser()

    def parse_with_image_properties(self, template: _Template, data: Any, text: str)\
            -> ImageParseResult:
        # Parses first for templates
        res = self.parse(template, data, text)

        path, scale = self.__img_parser.parse(res)

        return ImageParseResult(path, scale, res)

    def parse(self, template: _Template, data: Any, text: str) -> str:

        if len(text) <= 0:
            return ""

        try:
            tree = self.__parser.parse(text)
            transformer = _TemplateTransformer(template, data)
            results = transformer.transform(tree)

            # Creates a flat list of the results
            output = []
            for item in results.children:
                if isinstance(item, str):
                    output.append(item)
                else:
                    output.append(item.children[0])

            return "".join(output)
        except lark.exceptions.UnexpectedInput as err:
            raise ValueError(f"Unexpected input while parsing for templates:\n'{err.get_context(text)}'")
            pass
        except Exception as err:
            raise ValueError(f"Unknown error occurred. Please check your input: '{text}' ({err})")
