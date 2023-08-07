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
@pytask.mark.produces(OUT / "models" / "model.pickle")
def task_fit_model_python(depends_on, produces):
    
    data = pd.read_csv(depends_on["data"])
    model = fit_multi_logit_model(data)

    model.save(produces)
