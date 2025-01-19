import lark.exceptions
from lark import Lark as _Lark, Transformer as _Transformer


# Lark transformer to flatten and map the syntax
class _TemplateTransformer(_Transformer):
    def __init__(self):
        super().__init__()

    def scaling(self, args):
        return args[0]

    def scale_value(self, args):
        return args[0]

    def percentage(self, args):
        return int(args[0])

    def pixel_ratio(self, args):
        return (args[0], args[1])

    def pixel(self,args):
        return int(args[0])

    def text(self, args):
        return args[0]

    def start(self, args):
        return str(args[0]), args[1] if len(args) > 1 else None


class ImageInfoParser:

    def __init__(self):
        with open("jufo_pptx_script/templater/image_props_gramma.lark", "r") as file:
            grammar = file.read()

        self.__parser = _Lark(grammar, start='start', parser='lalr')

    def parse(self, text: str) -> (str, int or (int, int)):
        try:
            tree = self.__parser.parse(text)
            transformer = _TemplateTransformer()
            path, scale = transformer.transform(tree)

            return path, scale

        except lark.exceptions.UnexpectedInput as err:
            raise ValueError(f"Unexpected input while parsing for image properties:\n'{err.get_context(text)}'")

        except Exception as err:
            raise ValueError(f"Unknown error occurred. Please check your input: '{text}' ({err})")
