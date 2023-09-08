"""Tasks running the results formatting (tables, figures)."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import load_model
from final.plot import plot_relative_differences_grouped, attribute_support, plot_amce, plot_MM, plot_MM_group
from config import OUT, CODE
from utilities import read_yaml

#Plots:

@pytask.mark.depends_on(
    {
        "data_info": CODE / "final" / "plot_specs.yaml",
        "data_long" : OUT / "data" / "data_long.csv",
        "data_MM" : OUT / "models" / "data_MM.csv",
        "data": OUT / "models" / "model.pickle",
        "data_control" : OUT / "models" / "model_control.csv",
        "data_treated" : OUT / "models" / "model_treated.csv",
        "data_low_trust" : OUT / "models" / "model_low_trust.csv",
        "data_high_trust" : OUT / "models" / "model_high_trust.csv",
        "data_non_coal_region" : OUT / "models" / "model_non_coal_region.csv",
        "data_coal_region" : OUT / "models" / "model_coal_region.csv",
        "data_low_income" : OUT / "models" / "model_low_income.csv",
        "data_high_income" :OUT / "models" / "model_high_income.csv",
        "data_not_aware" : OUT / "models" / "model_not_aware.csv",
        "data_aware" :OUT / "models" / "model_aware.csv",
    },
    ) 
@pytask.mark.produces(
    {
        'support' : OUT / "figures" / "support_plot_coal_phase_out.png",
        'total' : OUT / "figures" / "AMCE_on_support.png",
        'MM' : OUT / "figures" / "MM_on_support.png",
        'treatment'  : OUT / "figures" / "MM_treatment.png",
        'trust'  : OUT / "figures" / "MM_trust.png",
        'coal_region' : OUT / "figures" / "MM_region.png",
        'income' : OUT / "figures" / "MM_income.png",
        'awareness' : OUT / "figures" / "MM_awareness.png",
    } 
    )
def task_plot_relative_differences(depends_on, produces):

    # Fig 1
    data_clean = pd.read_csv(depends_on["data_long"])
    fig = attribute_support(data_clean, "att_1")
    fig.write_image(produces['support'])

    data_info = read_yaml(depends_on["data_info"])

    # Fig 2
    model = load_model(depends_on["data"])
    fig = plot_amce(model, data_info, width=1.0)
    fig.write_image(produces['total'])

    # Fig 3
    model = pd.read_csv(depends_on["data_MM"])
    fig = plot_MM(model, data_info)
    fig.write_image(produces['MM'])

    # Grouped by:
    # Treatment
    model_control = pd.read_csv(depends_on["data_control"])
    model_treated = pd.read_csv(depends_on["data_treated"])
    fig = plot_MM_group(model_control, model_treated, data_info, group1="Control", group2="Treatment", width=1.0)
    fig.write_image(produces['treatment'])

    # Trust:  
    model_low_trust = pd.read_csv(depends_on["data_low_trust"])
    model_high_trust = pd.read_csv(depends_on["data_high_trust"])
    fig = plot_MM_group(model_low_trust, model_high_trust, data_info, group1="LowTrust", group2="HighTrust", width=1.0, plot_title="Marginal Means by High trust / Low trust")
    fig.write_image(produces['trust'])
    
    # Coal region
    model_non_coal_region = pd.read_csv(depends_on["data_non_coal_region"])
    model_coal_region = pd.read_csv(depends_on["data_coal_region"])
    fig = plot_MM_group(model_non_coal_region, model_coal_region, data_info, group1="NonCoalRegion", group2="CoalRegion", width=1.0, plot_title="Marginal Means by coal region status")
    fig.write_image(produces['coal_region'])

    # Income
    model_low_income = pd.read_csv(depends_on["data_low_income"])
    model_high_income = pd.read_csv(depends_on["data_high_income"])
    fig = plot_MM_group(model_low_income, model_high_income, data_info, group1="LowIncome", group2="HighIncome", width=1.0, plot_title="Marginal Means by income")
    fig.write_image(produces['income'])

    # Awareness
    model_not_aware = pd.read_csv(depends_on["data_not_aware"])
    model_aware = pd.read_csv(depends_on["data_aware"])
    fig = plot_MM_group(model_not_aware, model_aware, data_info, group1="Not Aware", group2="Aware", width=1.0, plot_title="Marginal Means by awareness")
    fig.write_image(produces['awareness'])

"""Writing Latex Tables out of estimation Tables!!! 
Store a table in LaTeX format with the estimation results (Python version)."""

@pytask.mark.depends_on(OUT / "models" / "model.pickle")
@pytask.mark.produces(OUT / "tables" / "estimation_results.tex")
def task_create_results_table_python(depends_on, produces):
    
    model = load_model(depends_on)
    table = model.summary().as_latex()
    with open(produces, "w") as f:
        f.writelines(table)

        

        






