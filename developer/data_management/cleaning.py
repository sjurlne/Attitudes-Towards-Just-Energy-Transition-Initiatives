"""Function(s) for cleaning the data set(s)."""
import pandas as pd
import numpy as np
import math

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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

    df = coal_prox_indicator(df)
    
    df = df.replace(renaming_specs['utility'])
    df = df.replace(renaming_specs['treatment'])
    df = df.replace(renaming_specs['trust'])
    
    df = df.replace(renaming_specs['policy_overview'])

    df['district'] = df['district'].replace(renaming_specs['district'])

    df['coal_region'] = df['state']
    df['coal_region'] = df['state'].replace(renaming_specs['coal_region'])

    for category in list(renaming_specs['attributes'].keys()):
        if category == 'soc_distributive':
            columns_to_replace = df.filter(like='att_2').columns
            
            # Replace values in selected columns
            df[columns_to_replace] = df[columns_to_replace].replace(renaming_specs['attributes'][category])

        else:    
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
            df[variable_specs[group]["names"]] = df[variable_specs[group]["names"]].astype('category', errors='ignore')

        elif variable_specs[group]["type"] == 'numerical':
            df[variable_specs[group]["names"]] = df[variable_specs[group]["names"]].astype('int', errors='ignore')

        else:
            continue

    
    df['ID'] = range(1, len(df) + 1)
    #df = df.set_index("ID")

    # Add group indicators
    df = _inconsistency(df)
    df = _trust_ID(df)
    df = _coal_region(df)
    df = _high_income(df)
    df = _awareness(df)

    return df

### GROUP IDS:

def _trust_ID(df):
    df['trust_average'] = df[['trust_in_governement_1', 'trust_in_governement_2', 'trust_in_governement_3']].astype(int).mean(axis=1)
    average = df['trust_average'].mean(axis=0)
    df['trust_ID'] = df['trust_average'] > 4#> average

    return df

def _inconsistency(df):
    """Looks for inconsistency between preferred package and  choices and likert rating"""
    
    for round in range(1,7):
        df[f'likert_choice_{round}_A'] = df[f'likert_{round}_1'] >= df[f'likert_{round}_2']
        df[f'likert_choice_{round}_B'] = df[f'likert_{round}_1'] <= df[f'likert_{round}_2']
    
        df[f'inconsistency_{round}'] = ((df[f'likert_choice_{round}_A'] == 0) & (df[f'choice_set_{round}'] == 'A')) | ((df[f'likert_choice_{round}_B'] == 0) & (df[f'choice_set_{round}'] == 'B'))
    
    return df

def _coal_region(df):
    df['coal_region'] = (df['coal_region'] == 1).astype(int)
    return df

def _high_income(df):
    df['high_income'] = (df['SC0'] > 5).astype(int)
    return df

def _awareness(df):
    df['aware'] = (df['q_main_energy_ov'] == '1') & (df['q_coal_sub_ov'] == '1') & (df['q_elec_sub_ov'] == '1')
    df['aware'] = df['aware'].astype(int)
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
                      'trust_in_governement_1',
                      'trust_in_governement_2',
                      'trust_in_governement_3',
                      'trust_average',
                      'trust_ID',
                      'coal_region',
                      'coal_prox',
                      'high_income',
                      'aware',
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
    A_columns = [c for c in list(df_with_dummies.columns) if "_A" in c] + ["inconsistent", "treatment_status", "trust_ID", "coal_region", "coal_prox", "high_income", "aware"]
    B_columns = [c for c in list(df_with_dummies.columns) if "_B" in c] + ["inconsistent", "treatment_status", "trust_ID", "coal_region", "coal_prox", "high_income", "aware"]
    new_columns = [col.replace( '_A', '') for col in A_columns]

    df_A = df_with_dummies[A_columns].copy()
    df_A.columns = new_columns
    df_A["package"] = "A"
    df_B = df_with_dummies[B_columns].copy()
    df_B.columns = new_columns
    df_B["package"] = "B"
    total = pd.concat([df_A, df_B])
    
    total = total.reset_index()
    total = total.set_index(['ID', 'round', 'package'])

    total = _set_support_dummy(total)
    total = standardize(total, 'utility')

    return total

def make_long_descriptive(df):
    df = df.copy()
    A_columns = [c for c in list(df.columns) if "_A" in c] + ["inconsistent", "treatment_status", "trust_ID", "coal_region", "coal_prox", "high_income", "aware"]
    B_columns = [c for c in list(df.columns) if "_A" in c] + ["inconsistent", "treatment_status", "trust_ID", "coal_region", "coal_prox", "high_income", "aware"]
    new_columns = [col.replace( '_A', '') for col in A_columns]

    df_A = df[A_columns].copy()
    df_A.columns = new_columns
    df_A["package"] = "A"
    df_B = df[B_columns].copy()
    df_B.columns = new_columns
    df_B["package"] = "B"
    df = pd.concat([df_A, df_B])

    df = df.reset_index()
    df = df.set_index(['ID', 'round', 'package'])

    df = _set_support_dummy(df)

    return df

def _set_support_dummy(df):

    df['support'] = df['utility'] >= 5
    df['unsupport'] = df['utility'] <= 3

    return df

def frequencies(conjoint_reg):
    
    frequency_table =  {}
    groups = ['att_1', 'att_2','att_3', 'att_4', 'att_5']
    for group in groups:
        total = sum(dict(conjoint_reg.filter(like=group).sum()).values())
        frequency_table[group] = {key.replace(f'{group}_', '') : (value / total).round(2) for key, value in dict(conjoint_reg.filter(like=group).sum()).items()}
    frequency_table = pd.DataFrame(frequency_table).sum(axis=1)
    frequency_table = pd.DataFrame(frequency_table, columns=["frequency"])

    frequency_table = frequency_table.rename_axis("Attribute_level")
    return frequency_table

def standardize(df, column):
    df[f'{column}_standardized'] = (df[column] - df[column].mean()) / df[column].std()

    return df

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    rad1 = math.radians(lat1)  # φ, λ in radians φ1
    rad2 = math.radians(lat2) #φ2
    diff1 = math.radians(lat2 - lat1)
    diff2 = math.radians(lon2 - lon1)

    a = math.sin(diff1/2) * math.sin(diff1/2) + \
        math.cos(rad1) * math.cos(rad2) * \
        math.sin(diff2/2) * math.sin(diff2/2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c  # in meters

    d = d / 1000
    d = round(d, 2)
    return d

def coal_prox_indicator(data_clean):

    #https://www.globaldata.com/data-insights/mining/india--five-largest-coal-mines-in-2090702/#:~:text=The%20five%20largest%20coal%20mines,mmtpa%20of%20ROM%20in%202021.
    coal_mines = {
        'Gevra OC Mine' : [22.337439, 82.546566],
        'Bhubaneswari OCP Mine' : [20.965332, 85.162714],
        'Dipka OC Project': [22.327948, 82.557578],
        'Kusmunda OC Mine' : [22.330294, 82.669243],
        'Lakhanpur OCP Mine' : [21.765555, 83.820422]
    }

    #https://www.power-technology.com/features/feature-the-top-10-biggest-thermal-power-plants-in-india/?cf-view
    coal_plants = {
        'Mundra Thermal Power Station, Gujarat' : [22.824412, 69.547972],
        'Mundra Ultra Mega Power Plant, Gujarat' : [22.815815, 69.525399],
        'Sasan Ultra Mega Power Plant, Madhya Pradesh' : [23.983091, 82.618795],
        'Tiroda Thermal Power Plant, Maharashtra' : [21.413246, 79.966920],
        'Talcher Super Thermal Power Station, Odisha' : [21.096245, 85.073762],
        'Rihand Thermal Power Station, Uttar Pradesh' : [24.027386, 82.790051],
        'Sipat Thermal Power Plant, Chhattisgarh' : [22.136485, 82.289925],
        'Chandrapur Super Thermal Power Station, Maharashtra' : [20.005170, 79.293512],
        'NTPC Dadri, Uttar Pradesh' : [28.597505, 77.607886],
    }

    for name, coordinates in coal_mines.items():
        data_clean[f'coal_mine_prox_{name}'] = data_clean.apply(lambda row: calculate_distance(row['LocationLatitude'], row['LocationLongitude'], coordinates[0], coordinates[1]), axis=1)

    for name, coordinates in coal_plants.items():
        data_clean[f'coal_plant_prox_{name}'] = data_clean.apply(lambda row: calculate_distance(row['LocationLatitude'], row['LocationLongitude'], coordinates[0], coordinates[1]), axis=1)


    matching_columns = [col for col in data_clean.columns if col.startswith("coal_mine") or col.startswith("coal_plant")]

    # Check if any value in the matching columns is smaller than 100
    data_clean['coal_prox'] = data_clean[matching_columns].lt(50).any(axis=1).astype(int)

    return data_clean