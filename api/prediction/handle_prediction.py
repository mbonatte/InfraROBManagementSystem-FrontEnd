import io
import numpy as np
import pandas as pd
from api.prediction.markov import MarkovContinous

def convert_to_markov(df, worst_IC, best_IC):
    column = df.keys()
    df_markov = pd.DataFrame(columns=['Initial','Time','Final'])
    road_sections = df[column[0]].unique()
    for road_section in road_sections:
        section = df[df[column[0]]==road_section]
        section = section.sort_values(by=column[1])
        for i in range(len(section)-1):
            if worst_IC > best_IC:
                if section.iloc[i][2] <= section.iloc[i+1][2]:
                    time_between = section.iloc[i+1][1] -  section.iloc[i][1]
                    df_markov.loc[len(df_markov)] = [section.iloc[i][2], time_between, section.iloc[i+1][2]]
    return df_markov.astype('int', errors = 'ignore')
    

def get_IC_through_time(csv_data, worst_IC, best_IC):
    buffer = io.StringIO(csv_data)
    df  = pd.read_csv(buffer, sep=';')
    data_markov_format = convert_to_markov(df, worst_IC, best_IC)
    print(data_markov_format)
    markov_model = MarkovContinous(worst_IC,
                                   best_IC,
                                   optimizer=True)
    
    markov_model.fit(data_markov_format['Initial'],
                     data_markov_format['Time'],
                     data_markov_format['Final'])

    response = {}
    response['Year'] = list(range(0, delta_time + 1))
    response['IC'] = markov_model.get_mean_over_time(delta_time,
                                                       initial_IC)

    
    return response
