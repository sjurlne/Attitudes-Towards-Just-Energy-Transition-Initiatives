"""Tasks running the core analyses."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import fit_model_1, fit_model_1_c, fit_model_2, fit_model_2_c, fit_model_3, fit_model_3_c, marginal_means
from config import OUT

@pytask.mark.depends_on(
        {
            "data": OUT / "data" / "data_regression.csv",
        }
    )
@pytask.mark.produces(
        {
        'model1' : OUT / "models" / "model1.pickle",
        'model1c' : OUT / "models" / "model1c.pickle",
        'model2' : OUT / "models" / "model2.pickle",
        'model2c' : OUT / "models" / "model2c.pickle",
        'model3' : OUT / "models" / "model3.pickle",
        'model3c' : OUT / "models" / "model3c.pickle",
        'model_amce_high_trust': OUT / "models" / "model_amce_high_trust.pickle",
        'model_amce_low_trust' : OUT / "models" / "model_amce_low_trust.pickle",
        'model_amce_aware' : OUT / "models" / "model_amce_aware.pickle",
        'model_amce_not_aware' : OUT / "models" / "model_amce_not_aware.pickle",
        'model_amce_coal_state' : OUT / "models" / "model_amce_coal_state.pickle",
        'model_amce_non_coal' : OUT / "models" / "model_amce_non_coal.pickle",
        'model_MM' : OUT / "models" / "data_MM.csv",
        'model_control' : OUT / "models" / "model_control.csv",
        'model_treated' : OUT / "models" / "model_treated.csv",
        'model_low_trust' : OUT / "models" / "model_low_trust.csv",
        'model_high_trust' : OUT / "models" / "model_high_trust.csv",
        'model_non_coal_prox' : OUT / "models" / "model_non_coal_prox.csv",
        'model_coal_prox' : OUT / "models" / "model_coal_prox.csv",
        'model_non_coal_state' : OUT / "models" / "model_non_coal_state.csv",
        'model_coal_state' : OUT / "models" / "model_coal_state.csv",
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
    data_non_coal_prox = data[data['coal_prox'] == 0]
    data_coal_prox = data[data['coal_prox'] == 1]
    data_non_coal_state = data[data['coal_state'] == 0]
    data_coal_state = data[data['coal_state'] == 1]
    data_low_income = data[data['high_income'] == 0]
    data_high_income = data[data['high_income'] == 1]
    data_not_aware = data[data['aware'] == 0]
    data_aware = data[data['aware'] == 1]

    # Fit regressions
    model1 = fit_model_1(data)
    model1c = fit_model_1_c(data)
    model2 = fit_model_2(data)
    model2c = fit_model_2_c(data)
    model3 = fit_model_3(data)
    model3c = fit_model_3_c(data)

    # fit AMCE on Trust and Awareness
    model_amce_high_trust = fit_model_3_c(data_high_trust)
    model_amce_low_trust = fit_model_3_c(data_low_trust)

    model_amce_aware = fit_model_3_c(data_aware)
    model_amce_not_aware = fit_model_3_c(data_not_aware)

    model_amce_coal_state = fit_model_3_c(data_coal_state)
    model_amce_non_coal = fit_model_3_c(data_non_coal_state)

    # Marginal Means
    model_MM = marginal_means(data)
    model_control = marginal_means(data_control)
    model_treated = marginal_means(data_treated)
    model_low_trust = marginal_means(data_low_trust)
    model_high_trust = marginal_means(data_high_trust)
    model_non_coal_prox = marginal_means(data_non_coal_prox)
    model_coal_prox = marginal_means(data_coal_prox)
    model_non_coal_state = marginal_means(data_non_coal_state)
    model_coal_state = marginal_means(data_coal_state)
    model_low_income = marginal_means(data_low_income)
    model_high_income = marginal_means(data_high_income)
    model_not_aware = marginal_means(data_not_aware)
    model_aware = marginal_means(data_aware)

    model1.save(produces['model1'])
    model1c.save(produces['model1c'])
    model2.save(produces['model2'])
    model2c.save(produces['model2c'])
    model3.save(produces['model3'])
    model3c.save(produces['model3c'])

    model_amce_aware.save(produces['model_amce_aware'])
    model_amce_not_aware.save(produces['model_amce_not_aware'])
    model_amce_high_trust.save(produces['model_amce_high_trust'])
    model_amce_low_trust.save(produces['model_amce_low_trust'])
    model_amce_coal_state.save(produces['model_amce_coal_state'])
    model_amce_non_coal.save(produces['model_amce_non_coal'])
    
    model_MM.to_csv(produces["model_MM"])
    model_control.to_csv(produces['model_control'])
    model_treated.to_csv(produces['model_treated'])
    model_low_trust.to_csv(produces['model_low_trust'])
    model_high_trust.to_csv(produces['model_high_trust'])
    model_non_coal_prox.to_csv(produces['model_non_coal_prox'])
    model_coal_prox.to_csv(produces['model_coal_prox'])
    model_non_coal_state.to_csv(produces['model_non_coal_state'])
    model_coal_state.to_csv(produces['model_coal_state'])
    model_low_income.to_csv(produces['model_low_income'])
    model_high_income.to_csv(produces['model_high_income'])
    model_not_aware.to_csv(produces['model_not_aware'])
    model_aware.to_csv(produces['model_aware'])




