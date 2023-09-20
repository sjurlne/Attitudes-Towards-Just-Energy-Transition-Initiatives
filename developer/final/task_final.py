"""Tasks running the results formatting (tables, figures)."""
import sys
sys.path.append(r'C:\Users\sjurl\OneDrive\Desktop\MasterThesis\Analysis\conjoint\developer')
sys.path = list(set(sys.path))

import pandas as pd
import pytask
import plotly.io as pio

from analysis.model import load_model
from final.plot import attribute_support, plot_regression, plot_MM, plot_MM_group, plot_AMCE_group, spatial_justice_coal_state 
from config import OUT, CODE
from utilities import read_yaml

#Plots: 
@pytask.mark.depends_on(
    {
        "data_info": CODE / "final" / "plot_specs.yaml",
        "data_long" : OUT / "data" / "data_long.csv",
        "data_MM" : OUT / "models" / "data_MM.csv",
        "data": OUT / "models" / "model3c.pickle",
        "model_amce_high_trust": OUT / "models" / "model_amce_high_trust.pickle",
        "model_amce_low_trust" : OUT / "models" / "model_amce_low_trust.pickle",
        "model_amce_aware" : OUT / "models" / "model_amce_aware.pickle",
        "model_amce_not_aware" : OUT / "models" / "model_amce_not_aware.pickle",
        "model_amce_coal_state" : OUT / "models" / "model_amce_coal_state.pickle",
        "model_amce_non_coal" : OUT / "models" / "model_amce_non_coal.pickle",
        "data_control" : OUT / "models" / "model_control.csv",
        "data_treated" : OUT / "models" / "model_treated.csv",
        "data_low_trust" : OUT / "models" / "model_low_trust.csv",
        "data_high_trust" : OUT / "models" / "model_high_trust.csv",
        "data_non_coal_prox" : OUT / "models" / "model_non_coal_prox.csv",
        "data_coal_prox" : OUT / "models" / "model_coal_prox.csv",
        "data_non_coal_state" : OUT / "models" / "model_non_coal_state.csv",
        "data_coal_state" : OUT / "models" / "model_coal_state.csv",
        "data_low_income" : OUT / "models" / "model_low_income.csv",
        "data_high_income" :OUT / "models" / "model_high_income.csv",
        "data_not_aware" : OUT / "models" / "model_not_aware.csv",
        "data_aware" :OUT / "models" / "model_aware.csv",
    }, 
    ) 
@pytask.mark.produces(
    {
        'support' : OUT / "figures" / "FIG1_support_plot_coal_phase_out.png", 
        'reg_amce' : OUT / "figures" / "FIG2_from_reg_on_support.png",
        'MM' : OUT / "figures" / "FIG3_MM_on_support.png",
        'treatment'  : OUT / "figures" / "MM_treatment.png",
        'coal_MM'  : OUT / "figures" / "FIG4_2_MM_coal.png",
        'coal_AMCE'  : OUT / "figures" / "FIG4_1_AMCE_coal.png",
        'trust_MM'  : OUT / "figures" / "FIG5_2_MM_trust.png",
        'trust_AMCE'  : OUT / "figures" / "FIG5_1_AMCE_trust.png",
        'awareness_MM' : OUT / "figures" / "FIG6_2_MM_awareness.png",  
        'awareness_AMCE' : OUT / "figures" / "FIG6_1_AMCE_awareness.png",  
        'coal_prox' : OUT / "figures" / "MM_coal_prox.png", 
        'coal_state' : OUT / "figures" / "MM_coal_state.png",
        'coal_state_spatial' : OUT / "figures" / "MM_coal_state_spatial.png",
        'income' : OUT / "figures" / "MM_income.png",
    }     
    )    
def task_plot_relative_differences(depends_on, produces):   
   
    # Fig 1
    data_clean = pd.read_csv(depends_on["data_long"])
    fig = attribute_support(data_clean, "att_1")
    pio.write_image(fig, produces['support'],scale=4, width=700, height=350)

    data_info = read_yaml(depends_on["data_info"])  

    # Fig 2 (Paper)
    model = load_model(depends_on["data"])
    fig = plot_regression(model, data_info, width=1.0)
    pio.write_image(fig, produces['reg_amce'], scale=4, width=550, height=800)  

    # Fig 3 (Paper) 
    model = pd.read_csv(depends_on["data_MM"])
    fig = plot_MM(model, data_info)
    pio.write_image(fig, produces['MM'], scale=4, width=550, height=800) 

    # Fig 4.1 (Paper)  
    model_amce_coal = load_model(depends_on["model_amce_coal_state"])
    model_amce_non_coal = load_model(depends_on["model_amce_non_coal"])
    fig = plot_AMCE_group(model_amce_non_coal, model_amce_coal, data_info, group1="NonCoalState", group2="CoalState", width=1.0, plot_title="AMCE by Coal State")
    fig.write_image(produces['coal_AMCE'])
    pio.write_image(fig, produces['coal_AMCE'], scale=4, width=550, height=800) 

    # Fig 4.2 (Paper):  
    model_non_coal_state = pd.read_csv(depends_on["data_non_coal_state"])
    model_coal_state = pd.read_csv(depends_on["data_coal_state"])
    fig = plot_MM_group(model_non_coal_state, model_coal_state, data_info, group1="NonCoalState", group2="CoalState", width=1.0, plot_title="Marginal Means by Coal State")
    fig.write_image(produces['coal_MM']) 
    pio.write_image(fig, produces['coal_MM'], scale=4, width=550, height=800) 

    # Fig 5.1 (Paper)  
    model_amce_high_trust = load_model(depends_on["model_amce_high_trust"])
    model_amce_low_trust = load_model(depends_on["model_amce_low_trust"])
    fig = plot_AMCE_group(model_amce_low_trust, model_amce_high_trust, data_info, group1="LowTrust", group2="HighTrust", width=1.0, plot_title="AMCE by High trust / Low trust")
    fig.write_image(produces['trust_AMCE'])
    pio.write_image(fig, produces['trust_AMCE'], scale=4, width=550, height=800) 

    # Fig 5.2 (Paper):  
    model_low_trust = pd.read_csv(depends_on["data_low_trust"])
    model_high_trust = pd.read_csv(depends_on["data_high_trust"])
    fig = plot_MM_group(model_low_trust, model_high_trust, data_info, group1="LowTrust", group2="HighTrust", width=1.0, plot_title="Marginal Means by High trust / Low trust")
    fig.write_image(produces['trust_MM']) 
    pio.write_image(fig, produces['trust_MM'], scale=4, width=550, height=800) 
 
    # Fig 6.1 (Paper) 
    model_amce_aware = load_model(depends_on["model_amce_aware"])
    model_amce_not_aware = load_model(depends_on["model_amce_not_aware"])
    fig = plot_AMCE_group(model_amce_not_aware, model_amce_aware, data_info, group1="Not Aware", group2="Aware", width=1.0, plot_title="AMCE by energy policy awareness")
    fig.write_image(produces['awareness_AMCE'])
    pio.write_image(fig, produces['awareness_AMCE'], scale=4, width=550, height=800) 
 
    # Fig 6.2 (Paper)
    model_not_aware = pd.read_csv(depends_on["data_not_aware"])
    model_aware = pd.read_csv(depends_on["data_aware"])
    fig = plot_MM_group(model_not_aware, model_aware, data_info, group1="Not Aware", group2="Aware", width=1.0, plot_title="Marginal Means by awareness")
    fig.write_image(produces['awareness_MM'])
    pio.write_image(fig, produces['awareness_MM'], scale=4, width=550, height=800) 
    
    # Grouped by: 
    # Treatment
    model_control = pd.read_csv(depends_on["data_control"])
    model_treated = pd.read_csv(depends_on["data_treated"])
    fig = plot_MM_group(model_control, model_treated, data_info, group1="Control", group2="Treatment", width=1.0)
    fig.write_image(produces['treatment'])

    # Coal prox
    model_non_coal_prox = pd.read_csv(depends_on["data_non_coal_prox"])
    model_coal_prox = pd.read_csv(depends_on["data_coal_prox"])
    fig = plot_MM_group(model_non_coal_prox, model_coal_prox, data_info, group1="MoreThan50km", group2="LessThan50km", width=1.0, plot_title="Marginal Means by living less or more than 50km from coal plant or mine")
    fig.write_image(produces['coal_prox'])

    model_non_coal = pd.read_csv(depends_on["data_non_coal_state"])
    model_coal = pd.read_csv(depends_on["data_coal_state"])
    fig = spatial_justice_coal_state(model_non_coal, model_coal, data_info, group1="NonCoal", group2="Coal", width=1.0, plot_title="Marginal Means, Spatial Justice")
    fig.write_image(produces['coal_state_spatial'])

    # Coal state
    model_non_coal_state = pd.read_csv(depends_on["data_non_coal_state"])
    model_coal_state = pd.read_csv(depends_on["data_coal_state"])
    fig = plot_MM_group(model_non_coal_state, model_coal_state, data_info, group1="Not Coal State", group2="Coal State", width=1.0, plot_title="Marginal Means by living in a coal state")
    fig.write_image(produces['coal_state'])

    # Income
    model_low_income = pd.read_csv(depends_on["data_low_income"])
    model_high_income = pd.read_csv(depends_on["data_high_income"])
    fig = plot_MM_group(model_low_income, model_high_income, data_info, group1="LowIncome", group2="HighIncome", width=1.0, plot_title="Marginal Means by income")
    fig.write_image(produces['income']) 


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
        empty = [None] * (26 - len(coefficients[i]))
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


