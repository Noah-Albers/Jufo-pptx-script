from jufo_pptx_script.data.DataRow import DataRow
from jufo_pptx_script.easypresentation.EasyPresentation import EasyPresentation as load_presentation
from jufo_pptx_script.templater.Template import Template as create_template
from jufo_pptx_script.data.CSVLoader import load_csv_file
from jufo_pptx_script.data.RowInspector import inspect
from jufo_pptx_script.common.datatypes.ProjectRow import ProjectRow as as_projectrow
from jufo_pptx_script.common.datatypes.ProjectRow import ProjectRow
from jufo_pptx_script.common.datatypes.PriceRow import PriceRow as as_pricerow
from jufo_pptx_script.common.datatypes.PriceRow import PriceRow
from tqdm import tqdm as inform_user
from jufo_pptx_script.easypresentation.EasyTextformatter import EasyTextformatter as format