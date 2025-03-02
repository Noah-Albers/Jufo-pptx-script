from jufo_pptx_script.data.DataRow import DataRow as _DataRow
from jufo_pptx_script.data.AdvancedExtendedRow import AdvancedExtendedRow as _AdvancedExtendedRow

class TutorRowWrapper:

    def __init__(self, idx: int, base):
        self._idx = idx
        self._base: ProjectRow = base
        self._name_cache: [str, str, str] or None = None

    def _create_name_cache(self):
        if self._name_cache is not None:
            return

        raw_value = self._base.get(f"Projektbetreuer {self._idx}")
        value = raw_value.split(" ")

        if len(value) == 1 and len(value[0].strip()) == 0:
            value = ["", "", ""]

        # Ensures correct formatting
        if not (2 <= len(value) <= 3):
            raise ValueError(f"Field Projektbetreuer {self._idx} has invalid value. Must be of type 'TITLE NACHNAME VORNAME' but is actually '{raw_value}'")

        if len(value) == 2:
            value.insert(0, "")

        self._name_cache = value

    @property
    def Ist_Existent(self):
        self._create_name_cache()
        return not all(map(lambda x: len(x) == 0, self._name_cache))

    @property
    def Schule(self):
        return self._base.get(f"Projektbetreuer {self._idx} Schule")

    @property
    def Vorname(self):
        self._create_name_cache()
        return self._name_cache[2]

    @property
    def Nachname(self):
        self._create_name_cache()
        return self._name_cache[1]

    @property
    def Title(self):
        self._create_name_cache()
        return self._name_cache[0]

class MemberRowWrapper:
    def __init__(self, idx: int, base):
        self._idx = idx
        self._base: ProjectRow = base

    def get(self, field: str):
        return self._base.get(f"T{self._idx} {field}")

    @property
    def Alter(self) -> int:
        raw = self._base.get(f"T{self._idx} Alter")
        asStrNum = raw.replace("Jahre", "").strip()

        return int(asStrNum)

    @property
    def Vorname(self) -> str:
        return self.get("Vorname")

    @property
    def Nachname(self) -> str:
        return self.get("Nachname")

    @property
    def Klasse(self) -> str:
        return self.get("Klasse")

    @property
    def Schule_Name(self) -> str:
        return self.get("Schule etc. Name")

    @property
    def Schule_Ort(self) -> str:
        return self.get("Schule etc. Ort")

    @property
    def Schule_Art(self) -> str:
        return self.get("Art der Schule etc.")

class ProjectRow(_AdvancedExtendedRow):

    def __init__(self, dr: _DataRow):
        super().__init__(dr)
        self._members = [MemberRowWrapper(i+1,self) for i in range(3)]
        self._tutors = [TutorRowWrapper(i+1, self) for i in range(2)]

    # region Direct properties

    def get_member(self, idx_from_one):
        if type(idx_from_one) is str:
            idx_from_one = int(idx_from_one.replace("T", ""))

        if type(idx_from_one) is not int or not (1 <= idx_from_one <= 3):
            raise ValueError(f"get_member was passed invalid argument '{idx_from_one}' idx_from_one must be an int between 1 and 3")

        return self._members[idx_from_one-1]

    def get_tutor(self, idx_from_one):
        return self._tutors[idx_from_one-1]

    @property
    def T1(self) -> MemberRowWrapper:
        return self._members[0]

    @property
    def T2(self) -> MemberRowWrapper:
        return self._members[1]

    @property
    def T3(self) -> MemberRowWrapper:
        return self._members[2]

    @property
    def Projektbetreuer1(self) -> TutorRowWrapper:
        return self._tutors[0]

    @property
    def Projektbetreuer2(self) -> TutorRowWrapper:
        return self._tutors[1]

    @property
    def Projektnummer(self) -> str:
        return self.get("Projektnummer")

    @property
    def Wettbewerbsjahr(self) -> int:
        return self._get_property_as_int("Wettbewerbsjahr")

    @property
    def Bundesland(self) -> str:
        return self.get("Bundesland")

    @property
    def Sparte(self) -> str:
        return self.get("Sparte")

    @property
    def Fachgebiet(self) -> str:
        return self.get("Fachgebiet")

    @property
    def Projekttitel(self) -> str:
        return self.get("Projekttitel")

    @property
    def Standnummer(self) -> str:
        return self.get("Standnummer")

    @property
    def Teilnahmestatus(self) -> bool or None:
        val = self.get("Teilnahmestatus")

        if val == "Nimmt teil":
            return True
        if val == "Zurückgezogen":
            return False
        if len(val.strip()) == 0:
            return None

        raise ValueError(f"Field Teilnahmestatus is none of 'Nimmt teil', 'Zurückgezogen', '' but '{val}'.")

    @property
    def Sicherheitsrelevant(self) -> bool or None:
        return self._get_property_as_yes_no_empty("Sicherheitsrelevant")

    @property
    def Erarbeitungsort_Art(self) -> str:
        return self.get("Erarbeitungsort Art")

    @property
    def Erarbeitungsort(self):
        return self.get("Erarbeitungsort")

    @property
    def Erarbeitungsort_Ort(self):
        return self.get("Erarbeitungsort Ort")

    @property
    def Gruppengröße(self) -> int:
        return self._get_property_as_int("Gruppengröße", min_value=1, max_value=3)

    @property
    def Patent(self) -> bool or None:
        return self._get_property_as_yes_no_empty("Patent")

    @property
    def Projekt_mit_Tieren(self):
        return self._get_property_as_yes_no_empty("Projekt mit Tieren")

    # endregion

    # region Abstract methods

    def _get_class_name(self) -> str:
        return "ProjectRow"

    def _get_minimal_infos(self) -> str:

        name = self._dr.get("Projekttitel", default_value=-1)
        number = self._dr.get("Projektnummer", default_value=-1)

        if name == -1 and number == -1:
            return "'Unknown Project'"

        if name == -1:
            return f"'Unknown Title' ({number})"

        if number == -1:
            return f"'{name}' (Unknown Projektnummer)"

        return f"'{name}' ({number})"

    # endregion
