"""Function(s) for cleaning the data set(s)."""

import pandas as pd

def clean_data(df, specs, renaming_specs):
    """Cleans and preprocesses the input DataFrame according to provided specifications.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing raw data to be cleaned.
        specs (dict): A dictionary containing specifications for data cleaning and preprocessing.
        renaming_specs (dict): A dictionary containing specifications for renaming attribute and utility names.

    Returns:
        pandas.DataFrame: A cleaned and preprocessed DataFrame following the specified operations.

    See Also:
        _inconsistency: An internal function used to compute the inconsistency indicator.

    """
    # Initial Cleaning
    df = df.drop([0, 1])
    
    df = df.replace(renaming_specs['utility'])
    for category in list(renaming_specs['attributes'].keys()):
        df = df.replace(renaming_specs['attributes'][category])

    # Keep Variables
    variable_specs = specs["variables"]
    groups_of_vars = variable_specs.keys()
    vars_to_keep=[]
    for group in groups_of_vars:
        vars_to_keep += variable_specs[group]["names"]

    df = df[vars_to_keep]

    # Transform types
    for group in groups_of_vars:
        if variable_specs[group]["type"] == 'categorical':
            df[variable_specs[group]["names"]] = df[variable_specs[group]["names"]].astype('category')

        elif variable_specs[group]["type"] == 'numerical':
            df[variable_specs[group]["names"]] = df[variable_specs[group]["names"]].astype('int')

        else:
            continue

    
    df['ID'] = range(1, len(df) + 1)
    #df = df.set_index("ID")

    # Add inconsistency indicator
    df = _inconsistency(df)

    return df

def _inconsistency(df):
    """Looks for inconsistency between preferred package and  choices and likert rating"""
    
    for round in range(1,7):
        df[f'likert_choice_{round}_A'] = df[f'likert_{round}_1'] >= df[f'likert_{round}_2']
        df[f'likert_choice_{round}_B'] = df[f'likert_{round}_1'] <= df[f'likert_{round}_2']
    
        df[f'inconsistency_{round}'] = ((df[f'likert_choice_{round}_A'] == 0) & (df[f'choice_set_{round}'] == 'A')) | ((df[f'likert_choice_{round}_B'] == 0) & (df[f'choice_set_{round}'] == 'B'))
    
    return df

def make_long(df):
    """Transforms the wide-format survey daya into a long-format DataFrame with repeated measures.

    This function takes the wide format from the raw survey data, where each row represents a participant
    and each column corresponds different settings for the different choice sets across multiple rounds. 
    It converts the DataFrame into a long format, with each row representing an individual choice round, 
    associated with the participant and the round.

    Parameters:
        df (pandas.DataFrame): The input DataFrame in wide format with participant data and multiple rounds.

    Returns:
        pandas.DataFrame: A long-format DataFrame.

    """

    long_df = pd.DataFrame()
    for round in range(1,7):
        df_temp = df[['ID',
                      f'round_{round}_att_1_a', 
                      f'round_{round}_att_1_b',
                      f'round_{round}_att_2_a', 
                      f'round_{round}_att_2_b', 
                      f'round_{round}_att_3_a', 
                      f'round_{round}_att_3_b', 
                      f'round_{round}_att_4_a', 
                      f'round_{round}_att_4_b', 
                      f'round_{round}_att_5_a', 
                      f'round_{round}_att_5_b', 
#                      f'round_{round}_att_6_a', 
#                      f'round_{round}_att_6_b',  
                      f'choice_set_{round}', 
                      f'likert_{round}_1', 
                      f'likert_{round}_2',
                      f'inconsistency_{round}']]
        df_temp['round'] = round
        df_temp = df_temp.rename(columns={
            f'round_{round}_att_1_a' : 'att_1_A', 
            f'round_{round}_att_1_b' : 'att_1_B',
            f'round_{round}_att_2_a' : 'att_2_A', 
            f'round_{round}_att_2_b' : 'att_2_B', 
            f'round_{round}_att_3_a' : 'att_3_A', 
            f'round_{round}_att_3_b' : 'att_3_B', 
            f'round_{round}_att_4_a' : 'att_4_A', 
            f'round_{round}_att_4_b' : 'att_4_B', 
            f'round_{round}_att_5_a' : 'att_5_A', 
            f'round_{round}_att_5_b' : 'att_5_B', 
#            f'round_{round}_att_6_a' : 'att_6_A', 
#            f'round_{round}_att_6_b' : 'att_6_B', 
            f'choice_set_{round}' : 'choice', 
            f'likert_{round}_1' : 'utility_A',
            f'likert_{round}_2' : 'utility_B',
            f'inconsistency_{round}' :  'inconsistent'
        })
        long_df = pd.concat([long_df, df_temp])

    first_columns = ['ID', 'round']
    all_cols = long_df.columns

    new_order = first_columns + [c for c in all_cols if c not in first_columns]

    long_df = long_df[new_order]
    long_df = long_df.set_index(['ID', 'round'])
    long_df = long_df.sort_index()
    
    return long_df
