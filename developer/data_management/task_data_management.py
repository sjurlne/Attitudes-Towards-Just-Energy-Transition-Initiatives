"""Tasks for managing the data."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from config import OUT, CODE, IN, MOCK_DATA
from data_management.cleaning import clean_data, make_long, make_dummy, make_ready_for_regression, frequencies
from utilities import read_yaml

RAW_FILES = {
        "raw_data": IN / "raw_data.csv",
        "mock_data" : MOCK_DATA / "raw_data_mock.csv", 
        "specs": CODE / "data_management" / "specs.yaml",
        "renaming_replacing" : CODE / "data_management" / "renaming_replacing.yaml",
    }
@pytask.mark.produces(
        {
            "clean" : OUT / "data" / "data_clean.csv",
            "regression" : OUT / "data" / "data_regression.csv",
            "freq" : OUT / "data" / "data_freq.csv",
        })
def task_clean_data_python(produces, raw_files=RAW_FILES,):
    """Clean the data"""
    data = pd.read_csv(RAW_FILES["mock_data"], encoding='cp1252')
    specs = read_yaml(RAW_FILES["specs"])
    renaming_specs = read_yaml(RAW_FILES["renaming_replacing"])

    # Cleaned data for inspection
    data = clean_data(data, specs, renaming_specs)
    data = make_long(data, renaming_specs)

    # Cleaned data for regression
    data_regression = make_dummy(data, renaming_specs)
    data_regression = make_ready_for_regression(data_regression)
    
    data_freq = frequencies(data_regression)

    data.to_csv(produces["clean"], index=True)
    data_regression.to_csv(produces["regression"], index=True)
    data_freq.to_csv(produces['freq'], index=True)
