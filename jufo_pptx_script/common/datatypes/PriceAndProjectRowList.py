from functools import cmp_to_key as _cmp_to_key

from typing import Callable, Iterator
from jufo_pptx_script.common.datatypes.PriceAndProjectRow import ProjectAndPriceRow as _ProjectAndPrice

class PriceAndProjectRowList:

    def __init__(self, rows: [_ProjectAndPrice]):
        self.__list = rows


    def skip(self, amount: int):
        """
        Skips "amount" entries (Does not copy the list)
        """
        for i in range(amount):
            self.__list.pop(0)
        return self

    def at(self, idx: int):
        """
        Returns the element at the "idx" position (Counting from zero)
        """
        return self.__list[idx]

    def copy(self):
        """
        Copies the list and returns it
        """
        return PriceAndProjectRowList(self.__list.copy())

    def filter(self, filter_func: Callable[[_ProjectAndPrice], bool]):
        """
        Filters the list (Does not create a new list
        """
        self.__list = list(filter(filter_func, self.__list))
        return self

    def sortByKeys(self, sort_func: Callable[[_ProjectAndPrice], any]):
        self.__list = sorted(self.__list, key=sort_func)
        return self

    def sortByCompare(self, sort_func: Callable[[_ProjectAndPrice, _ProjectAndPrice], int]):
        def internal_sort_function(a: _ProjectAndPrice, b: _ProjectAndPrice):
            res = sort_func(a, b)

            if res == a or res == b:
                return 1 if a == res else -1

            if type(res) is int:
                return res

            if type(res) is bool:
                return 1 if res else -1

            return int(res)

        self.__list.sort(key=_cmp_to_key(internal_sort_function))
        return self


    # region Overwritten default functions

    def __copy__(self):
        return self.copy()

    def __len__(self):
        return len(self.__list)

    @property
    def length(self):
        return len(self)

    def __getitem__(self, item):
        return self.at(item)

    def __str__(self):
        return "[ "+", ".join(map(lambda x: str(x), self.__list))+" ]"

    # endregion

    # region Iteration logic

    def __iter__(self) -> Iterator[_ProjectAndPrice]:
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__list):
            result = self.__list[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration

    # endregion