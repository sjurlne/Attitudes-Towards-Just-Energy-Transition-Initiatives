"""Tasks for managing the data."""

import pandas as pd
import pytask

from config import BLD, SRC, MOCK_DATA, DATA
from conjoint.data_management import clean_data
from conjoint.utilities import read_yaml


RAW_FILES = {
        "raw_data": SRC / "data" / "mock_data" / "raw_data.csv",
        "mock_data" : MOCK_DATA / "raw_data_mock.csv", 
        "specs": SRC / "conjoint" / "data_management" / "specs.yaml",
        "renaming_replacing" : SRC / "conjoint" / "data_management" / "renaming_replacing.yaml",
    }
@pytask.mark.produces(BLD / "data" / "data_clean.csv")
def task_clean_data_python(produces, raw_files=RAW_FILES,):
    """Clean the data"""
    data = pd.read_csv(RAW_FILES["mock_data"], encoding='cp1252')
    specs = read_yaml(RAW_FILES["specs"])
    renaming_specs = read_yaml(RAW_FILES["renaming_replacing"])

    data = clean_data(data, specs, renaming_specs)

    data.to_csv(produces, index=False)
