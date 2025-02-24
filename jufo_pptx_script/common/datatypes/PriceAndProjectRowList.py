from jufo_pptx_script.common.datatypes.ProjectRow import ProjectRow as _ProjectRow
from jufo_pptx_script.common.datatypes.PriceRow import PriceRow as _PriceRow
from typing import Callable, Iterator

class PriceAndProjectRowList:

    def __init__(self, rows: [(_ProjectRow, _PriceRow)]):
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

    def filter(self, filter_func: Callable[[(_ProjectRow, _PriceRow)], bool]):
        """
        Filters the list (Does not create a new list
        """
        self.__list = list(filter(filter_func, self.__list))
        return self

    def sort(self, sort_func: Callable[[(_ProjectRow, _PriceRow)], any]):
        self.__list = sorted(self.__list, key=sort_func)
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

    def __iter__(self) -> Iterator[(_ProjectRow, _PriceRow)]:
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