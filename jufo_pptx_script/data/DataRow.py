from typing import Any

class DataRow:

    def __init__(self, titles: [str], data: [str]):
        """

        Args:
            titles: the title row of the csv file (Used to determine the index (offset) of each item)
            data: The data row of the csv file
        """
        self.__title = titles
        self.__data = data

        if len(data) != len(titles):
            raise ValueError(f"DataRow {self._get_minimal_infos()} has an invalidly "
                             f"formatted csv row:\n'{', '.join(data)}'")

    def _get_minimal_infos(self) -> str:

        if len(self.__title) < 1 or len(self.__data) < 1:
            return f"Unknown DataRow"

        return f"{self.__title[0]} {self.__data[0]}"

    def has(self, field: str):
        try:
            value = self.__data[self.__title.index(field)]
            return len(value.strip()) > 0
        except ValueError as err:
            return False

    def get(self, field: str, default_value: Any or None = None, raise_raw_error: bool = False) -> str:
        """
        Getter for any field on the project.
        Args:
            # TODO:
            raise_raw_error:
            default_value:
            field:

        Returns: the value of the field
        Raises: ValueError if any field is not set

        """
        try:
            return self.__data[self.__title.index(field)]
        except ValueError as err:
            if default_value is not None:
                return default_value
            if raise_raw_error:
                raise err
            raise ValueError(f"Field '{field}' couldn't be found on DataRow "
                             f"{self._get_minimal_infos()} but was requested.'")

    def __str__(self):
        return f"DataRow[{self._get_minimal_infos()}]"
