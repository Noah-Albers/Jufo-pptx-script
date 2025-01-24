from typing import Callable, TypeVar, Generic, Iterator
from functools import cmp_to_key


# Defines a generic type for the items
T = TypeVar('T')

class DataRowList(Generic[T]):
    def __init__(self, raw: list[T]):
        self.__list = raw

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

    def copy_and_split_into(self, size: int):
        """
        Copies the list and splits it into small chunks of "size" size.

        For example lets say i have the projects: [A,B,C,D,E,F,G,H,I,J] and use as size 3, it would be returned
        [
            [A,B,C], [D,E,F], [G,H,I], [J]
        ]
        """
        if size <= 0:
            raise ValueError("Split size must be greater than 0")

        list_of_lists = []
        item_list = []

        for proj in self:
            if len(item_list) >= size:
                list_of_lists.append(DataRowList(item_list))
                item_list = []
            item_list.append(proj)

        if len(item_list) > 0:
            list_of_lists.append(DataRowList(item_list))

        return list_of_lists

    def copy(self):
        """
        Copies the list and returns it
        """
        return DataRowList(self.__list.copy())

    def filter(self, filter_func: Callable[[T], bool]):
        """
        Filters the list (Does not create a new list
        """
        self.__list = list(filter(filter_func, self.__list))
        return self

    def sort(self, sort_func: Callable[[T, T], int]):
        def internal_sort_function(a: T, b: T):
            res = sort_func(a, b)

            if res == a or res == b:
                return 1 if a == res else -1

            if type(res) is int:
                return res

            if type(res) is bool:
                return 1 if res else -1

            return int(res)

        self.__list.sort(key=cmp_to_key(internal_sort_function))
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

    def __iter__(self) -> Iterator[T]:
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
