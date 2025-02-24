from dataclasses import dataclass as _dt
from ProjectRow import ProjectRow as _ProjectRow
from PriceRow import PriceRow as _PriceRow

@_dt
class ProjectAndPriceRow:
    project: _ProjectRow
    price: _PriceRow
