"""Get geolocation"""

import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from config import OUT, CODE, IN, MOCK_DATA
from data_management.geolocator import classify_state

@pytask.mark.depends_on(
    {
    "raw_data" : IN / "main_sample.csv",
    })
@pytask.mark.produces(
    {
    "main_sample" : OUT / "data" / "main_sample_w_geo.csv",
    })

def task_geo_location(produces, depends_on):
    df = pd.read_csv(depends_on["raw_data"], encoding="utf8")

    df = df.drop([0, 1])

    df["state"] = df.apply(classify_state, axis=1)

    df.to_csv(produces["main_sample"])
