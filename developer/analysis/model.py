"""Functions for fitting the regression model."""

from statsmodels.iolib.smpickle import load_pickle
import statsmodels.api as sm
import numpy as np
import pandas as pd


def fit_model_support(data):
    """Fit a logit model to data."""

    outcome_name = 'support'
    explanatory_vars = [col for col in data.columns if "att" in col] + ['ID']

    X = data[explanatory_vars].astype(int)
    y = data[outcome_name].astype(int)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups':X['ID']})

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
