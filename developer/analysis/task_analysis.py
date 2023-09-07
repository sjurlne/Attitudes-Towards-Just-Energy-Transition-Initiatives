"""Tasks running the core analyses."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import fit_model_support, fit_model_group
from config import OUT


@pytask.mark.depends_on(
        {
            "data": OUT / "data" / "data_regression.csv",
        }
    )
@pytask.mark.produces(
        {
        'model' : OUT / "models" / "model.pickle",
        'model_control' : OUT / "models" / "model_control.pickle",
        'model_treated' : OUT / "models" / "model_treated.pickle",
        'model_low_trust' : OUT / "models" / "model_low_trust.pickle",
        'model_high_trust' : OUT / "models" / "model_high_trust.pickle",
        'model_non_coal_region' : OUT / "models" / "model_non_coal_region.pickle",
        'model_coal_region' : OUT / "models" / "model_coal_region.pickle",
        'model_low_income' : OUT / "models" / "model_low_income.pickle",
        'model_high_income' :OUT / "models" / "model_high_income.pickle",
        'model_not_aware' : OUT / "models" / "model_not_aware.pickle",
        'model_aware' :OUT / "models" / "model_aware.pickle",
        }
    )
def task_fit_model_python(depends_on, produces):
    
    data = pd.read_csv(depends_on["data"])
    data_control = data[data['treatment_status']==0]
    data_treated = data[data['treatment_status']==1]
    data_low_trust = data[data['trust_ID']==0]
    data_high_trust = data[data['trust_ID']==1]
    data_non_coal_region = data[data['coal_region'] == 0]
    data_coal_region = data[data['coal_region'] == 1]
    data_low_income = data[data['high_income'] == 0]
    data_high_income = data[data['high_income'] == 1]
    data_not_aware = data[data['aware'] == 0]
    data_aware = data[data['aware'] == 1]

    model = fit_model_support(data)
    model_control = fit_model_group(data_control)
    model_treated = fit_model_group(data_treated)
    model_low_trust = fit_model_group(data_low_trust)
    model_high_trust = fit_model_group(data_high_trust)
    model_non_coal_region = fit_model_group(data_non_coal_region)
    model_coal_region = fit_model_group(data_coal_region)
    model_low_income = fit_model_group(data_low_income)
    model_high_income = fit_model_group(data_high_income)
    model_not_aware = fit_model_group(data_not_aware)
    model_aware = fit_model_group(data_aware)

    model.save(produces['model'])
    model_control.save(produces['model_control'])
    model_treated.save(produces['model_treated'])
    model_low_trust.save(produces['model_low_trust'])
    model_high_trust.save(produces['model_high_trust'])
    model_non_coal_region.save(produces['model_non_coal_region'])
    model_coal_region.save(produces['model_coal_region'])
    model_low_income.save(produces['model_low_income'])
    model_high_income.save(produces['model_high_income'])
    model_not_aware.save(produces['model_not_aware'])
    model_aware.save(produces['model_aware'])




