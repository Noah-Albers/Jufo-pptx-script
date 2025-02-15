from typing import Callable as _Callable
from jufo_pptx_script.data.DataRow import DataRow as _DataRow

class Template:
    def __init__(self):
        self.__registered = {str: _Callable[[[_DataRow], [str]], str]}

    # Event: When a new template-function is registered
    def __call__(self, func):

        # Appends it
        self.__registered[func.__name__] = func

        return func

    def _get_registered(self):
        return self.__registered
