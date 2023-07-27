"""Tasks running the core analyses."""

import pandas as pd
import pytask

from conjoint.analysis.model import fit_multi_logit_model, load_model
from conjoint.analysis.predict import predict_prob_by_age
from config import BLD, GROUPS, SRC
from conjoint.utilities import read_yaml

@pytask.mark.depends_on(
    {
        "scripts": ["model.py", "predict.py"],
        "data": BLD / "python" / "data" / "data_clean.csv",
        "data_info": SRC / "data_management" / "data_info.yaml",
    },
)
@pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
def task_fit_model_python(depends_on, produces):
    """Fit a logistic regression model (Python version)."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    model = fit_multi_logit_model(data, data_info, model_type="linear")
    model.save(produces)
