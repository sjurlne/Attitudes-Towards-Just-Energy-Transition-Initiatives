"""Tasks running the core analyses."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import fit_multi_logit_model
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
        }
    )
def task_fit_model_python(depends_on, produces):
    
    data = pd.read_csv(depends_on["data"])
    data_control = data[data['treatment_status']==0]
    data_treated = data[data['treatment_status']==1]

    model = fit_multi_logit_model(data)
    model_control = fit_multi_logit_model(data_control)
    model_treated = fit_multi_logit_model(data_treated)

    model.save(produces['model'])
    model_control.save(produces['model_control'])
    model_treated.save(produces['model_treated'])
