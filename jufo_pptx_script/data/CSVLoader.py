from jufo_pptx_script.data.DataRow import (DataRow)
from jufo_pptx_script.data.DataRowList import DataRowList
import csv

def __normalize_row(row: list[str]):
    return list(map(lambda x: x.replace('\xa0', ' '), row))

def load_csv_file(path: str, delimiter=";", quotechar='"') -> DataRowList:
    with open(path) as csvfile:
        rdr = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)

        title_row = __normalize_row(rdr.__next__())

        return DataRowList([
            DataRow(title_row, __normalize_row(row))
            for row in rdr
        ])
