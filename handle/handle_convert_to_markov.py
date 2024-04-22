import pandas as pd

def convert_to_markov(df, worst_IC, best_IC, time_block='year'):
    """
    Converts a DataFrame into a Markov transition DataFrame based on specified columns.
    
    Parameters:
        df (pd.DataFrame): Input data frame with 'Date' and IC values.
        worst_IC (float): The worst IC threshold.
        best_IC (float): The best IC threshold.
        time_block (str): Time unit to normalize time differences ('month' or 'year').
        
    Returns:
        pd.DataFrame: DataFrame with Markov transition data.
    """
    if worst_IC < best_IC:
        raise ValueError("Not implemented yet")
    
    try:
        convert_sec_to_time_block = {'month': 3.8052e-7, 'year': 3.171e-8}[time_block]
    except KeyError:
        raise ValueError("time_block must be 'month' or 'year'")
    
    df.loc[:, 'Date'] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    
    df_markov = pd.DataFrame(columns=['Initial','Time','Final'])
    road_sections = df.iloc[:, 0].unique()
    
    for road_section in road_sections:
        section = df[df.iloc[:, 0] == road_section].sort_values(by=df.columns[1])
        for i in range(len(section)-1):
            if section.iloc[i, 2] <= section.iloc[i + 1, 2]:
                time_between = (section.iloc[i + 1, 1] - section.iloc[i, 1]).total_seconds()
                time_between = round(time_between * convert_sec_to_time_block)
                df_markov.loc[len(df_markov)] = [section.iloc[i, 2], time_between, section.iloc[i + 1, 2]]
    
    return df_markov.astype('int', errors = 'ignore')
    