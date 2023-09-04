"""Functions for fitting the regression model."""

from statsmodels.iolib.smpickle import load_pickle
import statsmodels.api as sm


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
