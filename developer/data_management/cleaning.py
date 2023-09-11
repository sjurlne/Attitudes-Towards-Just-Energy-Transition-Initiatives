"""Function(s) for cleaning the data set(s)."""
import pandas as pd
import numpy as np
import math

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

    df['LocationLatitude'] = df['LocationLatitude'].astype(float)
    df['LocationLongitude'] = df['LocationLongitude'].astype(float)
    df = coal_prox_indicator(df)
    df = city_prox_indicator(df)
    
    df = df.replace(renaming_specs['utility'])
    df = df.replace(renaming_specs['treatment'])
    df = df.replace(renaming_specs['trust'])
    df['genderFilter'] = df['genderFilter'] .replace(renaming_specs['gender'])
    df = df.replace(renaming_specs['policy_overview'])

    df['district'] = df['district'].replace(renaming_specs['district'])

    # geolocation relevant
    #df['coal_region'] = df['state']
    #df['coal_region'] = df['state'].replace(renaming_specs['coal_region'])

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
    #df = _coal_region(df)
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
    df['SC0'] = df['SC0'].fillna(5)
    df['high_income'] = (df['SC0'].astype(int, errors='ignore') > 5).astype(int)
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
                      'coal_prox',
                      'high_income',
                      'aware',
                      'urban',
                      'genderFilter',
                      'ageFilter',
                      'district',
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
    attribute_cols.append('district')
    df_with_dummies = pd.get_dummies(df, columns=attribute_cols)

    return df_with_dummies

def make_ready_for_regression(df_with_dummies, renaming_specs):
    vars_to_keep = renaming_specs['keep']
    A_columns = [c for c in list(df_with_dummies.columns) if "_A" in c] + vars_to_keep
    B_columns = [c for c in list(df_with_dummies.columns) if "_B" in c] + vars_to_keep
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

def make_long_descriptive(df, renaming_specs):
    vars_to_keep = renaming_specs['keep_descriptive']
    df = df.copy()
    A_columns = [c for c in list(df.columns) if "_A" in c] + vars_to_keep
    B_columns = [c for c in list(df.columns) if "_A" in c] + vars_to_keep
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
        '1' : [27.287517, 95.751477],
        '2' : [25.037752, 87.373761],
        '3' : [24.548647, 87.443779],
        '4' : [23.575851, 87.325296],
        '5' : [23.445079, 87.143132],
        '6' : [23.677697, 87.363157],
        '7' : [23.682152, 87.146260],
        '8' : [23.851652, 86.969975],
        '9' : [23.807820, 86.732851],
        '10' : [23.683085, 86.486627],
        '11' : [23.771554, 86.412535],
        '12' : [23.775896, 86.015363],
        '13' : [23.771473, 85.877080],
        '14' : [24.149130, 86.860477],
        '15' : [24.114265, 86.306799],
        '16' : [23.768901, 85.888556],
        '17' : [23.604326, 85.699821],
        '18' : [23.650260, 85.539991],
        '19' : [23.796200, 85.596535],
        '20' : [23.847373, 85.428889],
        '21' : [23.872281, 85.540571],
        '22' : [23.726677, 85.495022],
        '23' : [23.656667, 85.381336],
        '24' : [23.896400, 85.228915],
        '25' : [23.715208, 85.049809],
        '26' : [23.934183, 85.007813],
        '27' : [23.649937, 84.595527],
        '28' : [24.139321, 84.062995],
        '29' : [20.939208, 85.151544],
        '30' : [24.158834, 82.675149],
        '31' : [23.909456, 82.263674],
        '32' : [22.821391, 82.611755],
        '33' : [22.839616, 82.889254],
        '34' : [23.194206, 83.205632],
        '35' : [23.426914, 83.342806],
        '36' : [23.424925, 82.454474],
        '37' : [23.280041, 81.806704],
        '38' : [23.377800, 81.165452],
        '39' : [23.525660, 80.646948],
        '40' : [22.345591, 82.606193],
        '41' : [22.247135, 83.016019],
        '42' : [22.097075, 83.340930],
        '43' : [21.771074, 83.878586],
        '44' : [17.301741, 80.658494],
        '45' : [17.221380, 80.154848],
        '46' : [17.947081, 80.714797],
        '47' : [17.568518, 80.349386],
        '48' : [18.210918, 80.137139],
        '49' : [18.496900, 79.770093],
        '50' : [19.035322, 79.256833],
        '51' : [19.231001, 79.351393],
        '52' : [17.947966, 79.437091],
        '53' : [19.811458, 79.307934],
        '54' : [20.020555, 79.330957],
        '55' : [19.908344, 79.269055],
        '56' : [20.075125, 79.060184],
        '57' : [19.965048, 79.092092],
        '58' : [19.771579, 79.151852],
        '59' : [20.177642, 78.809595],
        '60' : [19.849756, 78.631139],
        '61' : [21.243727, 79.194690],
        '62' : [21.372038, 78.909259],
        '63' : [21.959186, 79.331323],
        '64' : [22.213886, 78.915332],
        '65' : [22.176780, 78.743598],
        '66' : [22.185255, 78.631074],
        '67' : [22.131219, 78.157579],
        '68' : [11.566912, 79.471791],
        '69' : [21.423798, 73.170243],
        '70' : [21.709576, 73.233760],
        '71' : [21.730270, 72.201700],
        '72' : [23.569893, 68.889212],
        '73' : [23.716086, 68.780059],
        '74' : [24.771589, 70.390926],
        '75' : [25.549808, 71.140310],
        '76' : [25.928480, 71.352955],
        '77' : [27.052643, 74.045848],
        '78' : [27.840332, 73.201115],
        '79' : [27.531098, 72.510852],
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
    data_clean['coal_prox'] = data_clean[matching_columns].lt(100).any(axis=1).astype(int)

    return data_clean

def city_prox_indicator(data_clean):

    city_data = {
        "Mumbai": [19.073, 72.883],
        "Delhi": [28.652, 77.231],
        "Bengaluru": [12.972, 77.594],
        "Hyderabad": [17.384, 78.456],
        "Ahmedabad": [23.026, 72.587],
        "Chennai": [13.088, 80.278],
        "Kolkata": [22.563, 88.363],
        "Surat": [21.196, 72.83],
        "Pune": [18.52, 73.855],
        "Kanpur": [26.465, 80.35],
        "Jaipur": [26.92, 75.788],
        "Lucknow": [26.839, 80.923]
    }

    for name, coordinates in city_data.items():
        data_clean[f'city_prox_{name}'] = data_clean.apply(lambda row: calculate_distance(row['LocationLatitude'], row['LocationLongitude'], coordinates[0], coordinates[1]), axis=1)

    matching_columns = [col for col in data_clean.columns if col.startswith("city_prox_")]

    # Check if any value in the matching columns is smaller than 100
    data_clean['urban'] = data_clean[matching_columns].lt(15).any(axis=1).astype(int)

    return data_clean