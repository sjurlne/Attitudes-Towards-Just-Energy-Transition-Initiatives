"""Tasks running the core analyses."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import fit_model_support, fit_model_group, marginal_means
from config import OUT, CODE


@pytask.mark.depends_on(
        {
            "data": OUT / "data" / "data_regression.csv",
        }
    )
@pytask.mark.produces(
        {
        'model' : OUT / "models" / "model.pickle",
        "model_MM" : OUT / "models" / "data_MM.csv",
        'model_control' : OUT / "models" / "model_control.csv",
        'model_treated' : OUT / "models" / "model_treated.csv",
        'model_low_trust' : OUT / "models" / "model_low_trust.csv",
        'model_high_trust' : OUT / "models" / "model_high_trust.csv",
        'model_non_coal_region' : OUT / "models" / "model_non_coal_region.csv",
        'model_coal_region' : OUT / "models" / "model_coal_region.csv",
        'model_low_income' : OUT / "models" / "model_low_income.csv",
        'model_high_income' :OUT / "models" / "model_high_income.csv",
        'model_not_aware' : OUT / "models" / "model_not_aware.csv",
        'model_aware' :OUT / "models" / "model_aware.csv",
        }
    )
def task_fit_model_python(depends_on, produces):
    
    data = pd.read_csv(depends_on["data"])
    data_control = data[data['treatment_status']==0]
    data_treated = data[data['treatment_status']==1]
    data_low_trust = data[data['trust_ID']==0]
    data_high_trust = data[data['trust_ID']==1]
    data_non_coal_region = data[data['coal_prox'] == 0]
    data_coal_region = data[data['coal_prox'] == 1]
    data_low_income = data[data['high_income'] == 0]
    data_high_income = data[data['high_income'] == 1]
    data_not_aware = data[data['aware'] == 0]
    data_aware = data[data['aware'] == 1]

    model = fit_model_support(data)
    model_MM = marginal_means(data)
    model_control = marginal_means(data_control)
    model_treated = marginal_means(data_treated)
    model_low_trust = marginal_means(data_low_trust)
    model_high_trust = marginal_means(data_high_trust)
    model_non_coal_region = marginal_means(data_non_coal_region)
    model_coal_region = marginal_means(data_coal_region)
    model_low_income = marginal_means(data_low_income)
    model_high_income = marginal_means(data_high_income)
    model_not_aware = marginal_means(data_not_aware)
    model_aware = marginal_means(data_aware)

    model.save(produces['model'])
    model_MM.to_csv(produces["model_MM"])
    model_control.to_csv(produces['model_control'])
    model_treated.to_csv(produces['model_treated'])
    model_low_trust.to_csv(produces['model_low_trust'])
    model_high_trust.to_csv(produces['model_high_trust'])
    model_non_coal_region.to_csv(produces['model_non_coal_region'])
    model_coal_region.to_csv(produces['model_coal_region'])
    model_low_income.to_csv(produces['model_low_income'])
    model_high_income.to_csv(produces['model_high_income'])
    model_not_aware.to_csv(produces['model_not_aware'])
    model_aware.to_csv(produces['model_aware'])




