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
    df = df.replace(renaming_specs['treatment'])
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

def make_long(df, renaming_specs):
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
                      'treatment_status',
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
                      f'inconsistency_{round}']].copy()
        df_temp['round'] = round
        df_temp = df_temp.rename(columns={
            f'round_{round}_att_1_a' : renaming_specs["new_names"][0], 
            f'round_{round}_att_1_b' : renaming_specs["new_names"][1],
            f'round_{round}_att_2_a' : renaming_specs["new_names"][2], 
            f'round_{round}_att_2_b' : renaming_specs["new_names"][3], 
            f'round_{round}_att_3_a' : renaming_specs["new_names"][4], 
            f'round_{round}_att_3_b' : renaming_specs["new_names"][5], 
            f'round_{round}_att_4_a' : renaming_specs["new_names"][6], 
            f'round_{round}_att_4_b' : renaming_specs["new_names"][7], 
            f'round_{round}_att_5_a' : renaming_specs["new_names"][8], 
            f'round_{round}_att_5_b' : renaming_specs["new_names"][9], 
#            f'round_{round}_att_6_a' : renaming_specs["new_names"][10], 
#            f'round_{round}_att_6_b' : renaming_specs["new_names"][11],
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

def make_dummy(df, renaming_specs):
    # Create dummy variables for each attribute level
    attribute_cols = renaming_specs['new_names']
    df_with_dummies = pd.get_dummies(df, columns=attribute_cols)

    return df_with_dummies

def make_ready_for_regression(df_with_dummies):
    A_columns = [c for c in list(df_with_dummies.columns) if "_A" in c] + ["inconsistent", "treatment_status"]
    B_columns = [c for c in list(df_with_dummies.columns) if "_B" in c] + ["inconsistent", "treatment_status"]
    new_columns = [col.replace( '_A', '') for col in A_columns]

    df_A = df_with_dummies[A_columns].copy()
    df_A.columns = new_columns
    df_A["package"] = "A"
    df_B = df_with_dummies[B_columns].copy()
    df_B.columns = new_columns
    df_B["package"] = "B"
    total = pd.concat([df_A, df_B])

    return total

def frequencies(conjoint_reg):
    
    frequency_table =  {}
    groups = ['att_1', 'att_2','att_3', 'att_4', 'att_5'] #add 6
    for group in groups:
        total = sum(dict(conjoint_reg.filter(like=group).sum()).values())
        frequency_table[group] = {key.replace(f'{group}_', '') : (value / total).round(2) for key, value in dict(conjoint_reg.filter(like=group).sum()).items()}
    frequency_table = pd.DataFrame(frequency_table).sum(axis=1)
    frequency_table = pd.DataFrame(frequency_table, columns=["frequency"])

    frequency_table = frequency_table.rename_axis("Attribute_level")
    return frequency_table

def standardize(df, column):
    df[column] = (df[column] - df[column].mean()) / df[column].std()

    return df