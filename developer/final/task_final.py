"""Tasks running the results formatting (tables, figures)."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import load_model
from final.plot import plot_relative_differences, plot_relative_differences_treatment
from config import OUT, CODE
from utilities import read_yaml

#Plots:

@pytask.mark.depends_on(
    {
        "data_info": CODE / "final" / "plot_specs.yaml",
        "data": OUT / "models" / "model.pickle",
        "data_control" : OUT / "models" / "model_control.pickle",
        "data_treated" : OUT / "models" / "model_treated.pickle",
    },
)
@pytask.mark.produces(
    {
    'total' : OUT / "figures" / "relative_differences.png",
    'treatment'  : OUT / "figures" / "relative_differences_treatment.png",
    }
    )
def task_plot_relative_differences(depends_on, produces):

    data_info = read_yaml(depends_on["data_info"])

    model = load_model(depends_on["data"])
    model_control = load_model(depends_on["data_control"])
    model_treated = load_model(depends_on["data_treated"])

    fig = plot_relative_differences(model, data_info, width=1.0)
    fig.write_image(produces['total'])

    fig = plot_relative_differences_treatment(model_control, model_treated, data_info, width=1.0)
    fig.write_image(produces['treatment'])


"""Writing Latex Tables out of estimation Tables!!! 
Store a table in LaTeX format with the estimation results (Python version)."""

@pytask.mark.depends_on(OUT / "models" / "model.pickle")
@pytask.mark.produces(OUT / "tables" / "estimation_results.tex")
def task_create_results_table_python(depends_on, produces):
    
    model = load_model(depends_on)
    table = model.summary().as_latex()
    with open(produces, "w") as f:
        f.writelines(table)
