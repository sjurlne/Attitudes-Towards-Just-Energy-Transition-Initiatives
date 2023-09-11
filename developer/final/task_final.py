"""Tasks running the results formatting (tables, figures)."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask

from analysis.model import load_model
from final.plot import attribute_support, plot_amce, plot_regression, plot_MM, plot_MM_group
from config import OUT, CODE
from utilities import read_yaml

#Plots: 

@pytask.mark.depends_on(
    {
        "data_info": CODE / "final" / "plot_specs.yaml",
        "data_long" : OUT / "data" / "data_long.csv",
        "data_MM" : OUT / "models" / "data_MM.csv",
        "data_old": OUT / "models" / "model_old.pickle",
        "data": OUT / "models" / "model3c.pickle",
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
        "data_rural" : OUT / "models" / "model_rural.csv",
        "data_urban" : OUT / "models" / "model_urban.csv",
    },
    ) 
@pytask.mark.produces(
    {
        'support' : OUT / "figures" / "support_plot_coal_phase_out.png",
        'amce' : OUT / "figures" / "AMCE_on_support.png",
        'reg_amce' : OUT / "figures" / "AMCE _from_reg_on_support.png",
        'MM' : OUT / "figures" / "MM_on_support.png",
        'treatment'  : OUT / "figures" / "MM_treatment.png",
        'trust'  : OUT / "figures" / "MM_trust.png",
        'coal_region' : OUT / "figures" / "MM_region.png",
        'income' : OUT / "figures" / "MM_income.png",
        'awareness' : OUT / "figures" / "MM_awareness.png",
        'urban' : OUT / "figures" / "MM_urban.png"
    } 
    ) 
def task_plot_relative_differences(depends_on, produces):

    # Fig 1
    data_clean = pd.read_csv(depends_on["data_long"])
    fig = attribute_support(data_clean, "att_1")
    fig.write_image(produces['support'])

    data_info = read_yaml(depends_on["data_info"])

    # Fig 2
    model = load_model(depends_on["data_old"])
    fig = plot_amce(model, data_info, width=1.0)
    fig.write_image(produces['amce'])

    model = load_model(depends_on["data"])
    fig = plot_regression(model, data_info, width=1.0)
    fig.write_image(produces['reg_amce'])

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
    fig = plot_MM_group(model_non_coal_region, model_coal_region, data_info, group1="MoreThan50km", group2="LessThan50km", width=1.0, plot_title="Marginal Means by living less or more than 50km from coal plant or mine")
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

    # Urban
    model_rural = pd.read_csv(depends_on["data_rural"])
    model_urban = pd.read_csv(depends_on["data_urban"])
    fig = plot_MM_group(model_rural, model_urban, data_info, group1="Rural", group2="Urban", width=1.0, plot_title="Marginal Means by Urban")
    fig.write_image(produces['urban'])

"""Writing Latex Tables out of estimation Tables!!! 
Store a table in LaTeX format with the estimation results (Python version)."""

@pytask.mark.depends_on(
    {
        'model1' : OUT / "models" / "model1.pickle",
        'model1c' : OUT / "models" / "model1c.pickle",
        'model2' : OUT / "models" / "model2.pickle",
        'model2c' : OUT / "models" / "model2c.pickle",
        'model3' : OUT / "models" / "model3.pickle",
        'model3c' : OUT / "models" / "model3c.pickle",
    })
@pytask.mark.produces(OUT / "tables" / "estimation_results.tex")
def task_create_results_table_python(depends_on, produces):
    
    model1_summary = load_model(depends_on["model1"])
    model1c_summary = load_model(depends_on["model1c"])
    model2_summary = load_model(depends_on["model2"])
    model2c_summary = load_model(depends_on["model2c"])
    model3_summary = load_model(depends_on["model3"])
    model3c_summary = load_model(depends_on["model3c"])

    coefficient_names = model3c_summary.params.index

    model_names = ['Model 1', 'Model 1C', 'Model 2', 'Model 2C', 'Model 3', 'Model 3C']

    coefficients = [extract_coefficients(model1_summary),
                extract_coefficients(model1c_summary),
                extract_coefficients(model2_summary),
                extract_coefficients(model2c_summary),
                extract_coefficients(model3_summary),
                extract_coefficients(model3c_summary)]

    data_dict = {' ': [' ']}#, 'Model 1': [], 'Model 1C': [], 'Model 2': [],
             #'Model 2C': [], 'Model 3': [], 'Model 3C': []}

    data_dict[' '] = coefficient_names.to_list() + ['Obs', 'R2', 'f-statistic']

    #for var_index, var_coeffs in enumerate(zip(*coefficients)):
    #    data_dict['Variable'].append(f'{var_coeffs}')
    #    for model_index, coef_stderr in enumerate(coefficients):
    #        data_dict[model_names[model_index]].append(coef_stderr)

    rsquared_values = [round(model1_summary.rsquared, 3), round(model1c_summary.rsquared, 3),
                round(model2_summary.rsquared, 3), round(model2c_summary.rsquared, 3),
                round(model3_summary.rsquared, 3), round(model3c_summary.rsquared, 3)]

    f_statistics = [round(model1_summary.fvalue, 3), round(model1c_summary.fvalue, 3),
                round(model2_summary.fvalue, 3), round(model2c_summary.fvalue, 3),
                round(model3_summary.fvalue, 3), round(model3c_summary.fvalue, 3)]

    nobs_values = [model1_summary.nobs/2/6, model1c_summary.nobs/2/6,
            model2_summary.nobs/2/6, model2_summary.nobs/2/6,
            model3_summary.nobs/2/6, model3c_summary.nobs/2/6]
    
    #data_dict['Variable'].extend(['nobs', 'rsquared', 'f-statistic'])
    #for model_index in range(len(model_names)):
    #    data_dict[model_names[model_index]].extend([nobs_values[model_index], rsquared_values[model_index], f_statistic_values[model_index]])
    for i in range(0,6):
        empty = [None] * (27 - len(coefficients[i]))
        data_dict[model_names[i]] = coefficients[i] + empty + [nobs_values[i], rsquared_values[i], f_statistics[i]]

    #data_dict[' '].append(len(data_dict[' ']))

    df = pd.DataFrame(data_dict)

    latex_table = df.to_latex(index=False, escape=False, decimal=',', na_rep=' ')
    # Convert the DataFrame to a LaTeX table
    #latex_table = df.to_latex(index=False, escape=False, column_format='|c|c|c|c|c|')

    with open(produces, "w") as f:
        f.writelines(latex_table)

def extract_coefficients(summary):
    coefficients = summary.params
    stderrs = summary.bse
    coef_stderr = ["\makecell{{ {:.3f} \\\ ({:.3f}) }}".format(coef, stderr) for coef, stderr in zip(coefficients, stderrs)]
    return coef_stderr


