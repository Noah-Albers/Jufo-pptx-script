from dataclasses import dataclass as _dt
from jufo_pptx_script.common.datatypes.ProjectRow import ProjectRow as _ProjectRow
from jufo_pptx_script.common.datatypes.PriceRow import PriceRow as _PriceRow

@_dt
class ProjectAndPriceRow:
    project: _ProjectRow
    price: _PriceRow

    def __iter__(self):
        return iter((self.project, self.price))