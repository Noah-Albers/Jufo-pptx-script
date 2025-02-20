from jufo_pptx_script.data.DataRow import DataRow as _DataRow
from jufo_pptx_script.data.AdvancedExtendedRow import AdvancedExtendedRow as _AdvancedExtendedRow
from typing import Literal

class PriceRow(_AdvancedExtendedRow):

    def __init__(self, dr: _DataRow):
        super().__init__(dr)
        self._dr = dr

        # Ensures the projekt-id exists
        self.ProjektId()

        # Validates the given Price row's
        if self.HatPreis and not self.Preis in [1,2,3]:
            raise ValueError(f"The 'price' '{self.Preis}' is not valid.")

        if self.HatSonderpreis and type(self.SonderpreisTitle) is not str:
            raise ValueError(f"The 'sonderpreis' is not a string")

        # Ensures Preis or Sonderpreis are set
        if not self.HatPreis and not self.HatSonderpreis:
            raise ValueError(f"Either a 'price' or 'sonderpreis' must be specified for Project '{self.ProjektId()}'")



    def _get_class_name(self) -> str:
        return "PriceRow"

    def _get_minimal_infos(self) -> str:
        return self.SonderpreisTitle if self.HatSonderpreis else self.Preis

    @property
    def ProjektId(self):
        return self.get("id")

    @property
    def Preis(self) -> 1 or 2 or 3:
        return self._get_property_as_int("preis")

    @property
    def HatSonderpreis(self):
        return self.has("sonderpreis")

    @property
    def HatPreis(self):
        return self.has("preis")

    @property
    def SonderpreisTitle(self):
        return self.get("sonderpreis")

