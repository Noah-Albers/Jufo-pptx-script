from jufo_pptx_script.data.DataRow import DataRow
from jufo_pptx_script.data.DataRowList import DataRowList

def inspect(data: DataRow or DataRowList or [DataRowList],
            attributes: [str] or str or None = None, __redirect: bool = False) -> str or None:

    def get_for_single_proj(proj: DataRow):

        if type(attributes) is str:
            return f"DataRow[{attributes}='{proj.get(attributes)}']"
        elif attributes is None:
            return str(proj)
        else:
            return "DataRow["+", ".join(list(map(lambda attr: f"{attr}='{proj.get(attr)}'", attributes)))+"]"

    output = ""

    found_type = ""

    if isinstance(data, DataRow):
        output += get_for_single_proj(data)
        found_type = "DataRow"
    elif isinstance(data, DataRowList):
        for p in data:
            output += "\n\t"+get_for_single_proj(p)
        found_type = "DataRowList"
    elif type(data) is list and (len(data) <= 0 or isinstance(data[0], DataRowList)):
        for p in data:
            output += "\n\t" + " / ".join(list(map(lambda r: inspect(r, attributes, True), p))).replace("\n", "\n\t")
        found_type = "[DataRowList]"
    else:
        raise ValueError(f"Inspect was called with an invalid data type '{type(data)}', please use DataRow or "
                         f"DataRowList.")

    if __redirect:
        return output
    else:
        print(f"Inspect ({found_type}): {output}")
