"""Tasks running the results formatting (tables, figures)."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import load_model
from final.plot import plot_relative_differences_grouped, attribute_support, plot_amce
from config import OUT, CODE
from utilities import read_yaml

#Plots:

@pytask.mark.depends_on(
    {
        "data_info": CODE / "final" / "plot_specs.yaml",
        "data_clean" : OUT / "data" / "data_clean.csv",
        "data": OUT / "models" / "model.pickle",
        "data_control" : OUT / "models" / "model_control.pickle",
        "data_treated" : OUT / "models" / "model_treated.pickle",
        "data_low_trust" : OUT / "models" / "model_low_trust.pickle",
        "data_high_trust" : OUT / "models" / "model_high_trust.pickle",
        "data_non_coal_region" : OUT / "models" / "model_non_coal_region.pickle",
        "data_coal_region" : OUT / "models" / "model_coal_region.pickle"
    },
) 
@pytask.mark.produces(
    {
    'support' : OUT / "figures" / "support_plot_coal_phase_out.png",
    'total' : OUT / "figures" / "AMCE_on_support.png",
    'treatment'  : OUT / "figures" / "marginal_means_treatment.png",
    'trust'  : OUT / "figures" / "marginal_means_trust.png",
    'coal_region' : OUT / "figures" / "coal_region.png"}
    )
def task_plot_relative_differences(depends_on, produces):

    # Fig 1
    data_clean = pd.read_csv(depends_on["data_clean"])
    fig = attribute_support(data_clean, "att_1")
    fig.write_image(produces['support'])

    data_info = read_yaml(depends_on["data_info"])

    model = load_model(depends_on["data"])

    # Fig 2
    fig = plot_amce(model, data_info, width=1.0)
    fig.write_image(produces['total'])

    # Grouped by:
    # Treatment
    model_control = load_model(depends_on["data_control"])
    model_treated = load_model(depends_on["data_treated"])
    fig = plot_relative_differences_grouped(model_control, model_treated, data_info, width=1.0)
    fig.write_image(produces['treatment'])

    # Trust:
    model_low_trust = load_model(depends_on["data_low_trust"])
    model_high_trust = load_model(depends_on["data_high_trust"])
    fig = fig = plot_relative_differences_grouped(model_low_trust, model_high_trust, data_info, width=1.0, plot_title="Marginal Means High trust / Low trust")
    fig.write_image(produces['trust'])
    
    # Coal region
    model_non_coal_region = load_model(depends_on["data_non_coal_region"])
    model_coal_region = load_model(depends_on["data_coal_region"])
    fig = fig = plot_relative_differences_grouped(model_non_coal_region, model_coal_region, data_info, width=1.0, plot_title="Marginal Means non coal / coal region")
    fig.write_image(produces['coal_region'])


"""Writing Latex Tables out of estimation Tables!!! 
Store a table in LaTeX format with the estimation results (Python version)."""

@pytask.mark.depends_on(OUT / "models" / "model.pickle")
@pytask.mark.produces(OUT / "tables" / "estimation_results.tex")
def task_create_results_table_python(depends_on, produces):
    
    model = load_model(depends_on)
    table = model.summary().as_latex()
    with open(produces, "w") as f:
        f.writelines(table)
