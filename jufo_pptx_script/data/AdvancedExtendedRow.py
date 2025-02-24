from jufo_pptx_script.data.DataRow import DataRow as _DataRow


class AdvancedExtendedRow:

    def __init__(self, dr: _DataRow):
        self._dr: _DataRow = dr

    #region Abstract methods

    def _get_class_name(self) -> str:
        """
        Returns: the classname to use when identifying the row in error messages
        """
        raise NotImplementedError("Abstract method not implemented")

    def _get_minimal_infos(self) -> str:
        """
        Tries to generate a minimal descriptor about the row to identify it
        """
        raise NotImplementedError("Abstract method not implemented")

    #endregion

    def has(self, field: str):
        return self._dr.has(field)

    def get(self, field: str):
        try:
            return self._dr.get(field, raise_raw_error=True)
        except ValueError:
            raise ValueError(f"Field '{field}' couldn't be found on {self._get_class_name()} "
                             f"{self._get_minimal_infos()} but was requested.'")

    # region Field-retrieve Utils (Get Utils)

    def _get_property_as_int(self, field: str, min_value: int or None = None, max_value: int or None = None):
        value = self.get(field)
        try:
            value = int(value)

            if min_value is not None and value < min_value:
                raise ValueError(f"{field} has a value {value} but must at least be {min_value}.")
            if max_value is not None and value > max_value:
                raise ValueError(f"{field} has a value {value} but must less or equal to {max_value}.")

            return value
        except ValueError:
            raise ValueError(f"{field} is not an integer, instead is '{value}'.")

    def _get_property_as_yes_no_empty(self, field: str) -> bool or None:
        value = self.get(field)

        if value == 'Ja':
            return True
        if value == 'Nein':
            return False
        if len(value.strip()) == 0:
            return None

        raise ValueError(f"{field} is none of 'Ja', 'Nein' or '' but instead is '{value}'.")

    def __str__(self):
        return f"{self._get_class_name()}[{self._get_minimal_infos()}]"

    # endregion