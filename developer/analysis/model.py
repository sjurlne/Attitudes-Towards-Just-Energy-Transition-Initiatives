"""Functions for fitting the regression model."""

from statsmodels.iolib.smpickle import load_pickle
import statsmodels.api as sm
import numpy as np
import pandas as pd


def fit_model_1(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if "att_1" in col]

    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model

def fit_model_1_c(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if "att_1" in col] + ['ageFilter', 'genderFilter', 'urban', 'district_NorthernZone', 
                                                                            'district_NorthEasternZone', 'district_CentralZone', 'district_EasternZone',
                                                                            'district_WesternZone', 'district_SouthernZone', 'treatment_status']

    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model

def fit_model_2(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if any(att in col for att in ["att_1", "att_2", "att_3"])]


    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model

def fit_model_2_c(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if any(att in col for att in ["att_1", "att_2", "att_3"])] + ['ageFilter', 'genderFilter', 'urban', 'district_NorthernZone', 
                                                                            'district_NorthEasternZone', 'district_CentralZone', 'district_EasternZone',
                                                                            'district_WesternZone', 'district_SouthernZone', 'treatment_status']

    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model

def fit_model_3(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if "att" in col]

    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model

def fit_model_3_c(data):
    """Fit a linear probability model to data."""
    outcome = 'support'
    explanatory_vars = [col for col in data.columns if "att" in col] +  ['ageFilter', 'genderFilter', 'urban', 'district_NorthernZone', 
                                                                            'district_NorthEasternZone', 'district_CentralZone', 'district_EasternZone',
                                                                            'district_WesternZone', 'district_SouthernZone', 'treatment_status']

    # Having a reference category for each att:
    to_remove = ['att_1_Eliminate2070', 'att_2_NothingSoc', 'att_3_NothingEco', 'att_4_GovAlone', 'att_5_NoInterference']
    explanatory_vars = [x for x in explanatory_vars if x not in to_remove]


    X = data[explanatory_vars].astype(int)
    y = data[outcome].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':data['ID']})

    return model




def fit_model_support_c(data):
    """Fit a linear probability model to data."""

    outcome_name = 'support'
    explanatory_vars = [col for col in data.columns if "att" in col] + ['ageFilter', 'genderFilter', 'urban', 'district_NorthernZone', 
                                                                        'district_NorthEasternZone', 'district_CentralZone', 'district_EasternZone',
                                                                        'district_WesternZone', 'district_SouthernZone']

    X = data[explanatory_vars].astype(int)
    y = data[outcome_name].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': data['ID']})

    return model


def fit_model_group(data):
    """Fit a logit model to data."""

    outcome_name = 'support'
    explanatory_vars = [col for col in data.columns if "att" in col] + ['ID']

    X = data[explanatory_vars].astype(int)
    y = data[outcome_name].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':X['ID']}) #MIGHT NOT WORK

    return model


def load_model(path):
    """Load statsmodels model.

    Args:
        path (str or pathlib.Path): Path to model file.

    Returns:
        statsmodels.base.model.Results: The stored model.

    """
    return load_pickle(path)

def _calculate_conditional_probability(df, column_x, column_y):

    nobs = len(df)
    # Step 1: Count occurrences of X=1 and Y=1 simultaneously
    xy_count = ((df[column_x] == True) & (df[column_y] == True)).sum()
    
    # Step 2: Count occurrences of X=1
    x_count = (df[column_x] == True).sum()
    
    # Step 3: Calculate P(Y=1|X=1)
    if x_count > 0:
        probability_y_given_x = xy_count / x_count
        probability_y_given_x = probability_y_given_x.round(4)
    else:
        probability_y_given_x = np.nan
    
    # Step 4: Calculate standard deviation
    variance_y_given_x = (probability_y_given_x * (1 - probability_y_given_x)) / x_count
    std_deviation = np.sqrt(variance_y_given_x).round(4)
    
    return probability_y_given_x, std_deviation, nobs

def marginal_means(df): 
    attributes_levels = df.columns[df.columns.str.startswith('att')]

    outcome = 'support'

    marginal_means ={}

    for att_level in attributes_levels:
        results = _calculate_conditional_probability(df, att_level, outcome)
        marginal_means[f'{att_level}_MM'] = []
        marginal_means[f'{att_level}_MM'].append(results[0])
        marginal_means[f'{att_level}_MM'].append(results[1])
        marginal_means[f'{att_level}_MM'].append(results[2])

    return pd.DataFrame(marginal_means)
