from typing import Callable as _Callable, Callable
from jufo_pptx_script.data.DataRow import DataRow as _DataRow

class Template:
    def __init__(self):
        self.__registered = {str: _Callable[[[_DataRow], [str]], str]}

    # Event: When a new template-function is registered
    # TODO: Test cases
    def __call__(self, arg):

        # Checks if the function name should be generated automatically
        is_autoname = callable(arg)

        # arg is the function to be registered
        if is_autoname:
            self.register(arg.__name__, arg)
            return arg
        else:
            return lambda func: self.register(arg, func)

    def _get_registered(self):
        return self.__registered

    # TODO: Test cases
    # - Function
    # - Value
    # - Single name
    # - Multiple names
    def register(self, name: [str] or str, value: Callable or any):
        """
        Assigns a value or function to a name.

        Examples:
            - register("foo", 10) results in '10' for '{{ foo }}' or '{{ foo(abc=bar) }}'
            - register(["abc","def"], lambda t: f"t={t}") results in 't=5' for '{{ abc(t=5) }}' or '{{ def(t=5) }}'
        """
        if type(name) is not list:
            name = [name]

        for key in name:
            self.__registered[key] = value if callable(value) else lambda: value
