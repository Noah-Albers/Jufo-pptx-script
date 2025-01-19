from jufo_pptx_script.data.DataRow import DataRow as _DataRow
from jufo_pptx_script.data.AdvancedExtendedRow import AdvancedExtendedRow as _AdvancedExtendedRow
from typing import Literal

class PriceRow(_AdvancedExtendedRow):

    def __init__(self, dr: _DataRow):
        super().__init__(dr)
        self._dr = dr

        # Validates the price row
        if self.Type not in ["Sonderpreis",1,2,3]:
            raise ValueError(f"The price-type '{self.Type}' is not valid.")

        if self.IstSonderpreis and type(self.SonderpreisTitle) is not str:
            raise ValueError(f"The sonderpreis-title is not a string")


    def _get_class_name(self) -> str:
        return "PriceRow"

    def _get_minimal_infos(self) -> str:
        return self.Type

    @property
    def Type(self) -> Literal["Sonderpreis"] or 1 or 2 or 3:
        return self.get("type")

    @property
    def IstSonderpreis(self):
        return self.Type == "Sonderpreis"

    @property
    def SonderpreisTitle(self):
        return self.get("title")

