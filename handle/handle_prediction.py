import io
import numpy as np
import pandas as pd

from ams.prediction.markov import MarkovContinous
from ams.performance.performance import Performance

from InfraROBManagementSystem.convert.organization import Organization
from InfraROBManagementSystem.convert.ASFiNAG import ASFiNAG
from InfraROBManagementSystem.optimization.problem import InfraROBRoadProblem

from handle.handle_convert_to_markov import convert_to_markov
    

def get_fitted_markov_model(data_markov_format, worst_IC, best_IC):
    markov_model = MarkovContinous(worst_IC,
                                   best_IC,
                                   optimizer=True)
    
    markov_model.fit(data_markov_format['Initial'],
                     data_markov_format['Time'],
                     data_markov_format['Final'])
    return markov_model

def get_IC_through_time(inspections, institution, worst_IC, best_IC, time_block, time_horizon, asset_properties = None):
    response = {}
    if institution == 'Generic':
        buffer = io.StringIO(inspections)
        df  = pd.read_csv(buffer, sep=',')
        data_markov_format = convert_to_markov(df, worst_IC, best_IC, time_block)
        markov_model = get_fitted_markov_model(data_markov_format, worst_IC, best_IC)

        initial_IC = best_IC
        response['Year'] = list(range(0, time_horizon + 1))
        response['IC'] = list(markov_model.get_mean_over_time(time_horizon,
                                                           initial_IC))
    if institution == 'ASFiNAG':
        buffer = io.StringIO(inspections)
        df_inspections  = pd.read_csv(buffer, sep=',').to_dict(orient='list')
        buffer = io.StringIO(asset_properties)
        df_properties  = pd.read_csv(buffer, sep=',').to_dict(orient='list')
        organization = Organization.set_organization(institution)
        variables = {
                        'inspections': df_inspections,
                        'properties': df_properties,
                        'institution': institution,
                        'organization': organization,
                        'worst_IC': worst_IC,
                        'best_IC': best_IC,
                        'time_block': time_block,
                        'time_horizon': time_horizon,
                        'results': {}
                     }
        predict(variables)
        response = variables['results']

    
    return response

def get_IC_through_time_for_road(road, institution, worst_IC, best_IC, time_block, time_horizon, asset_properties = None):
    response = {}

    if institution == 'ASFiNAG':
        organization = Organization.set_organization(institution)
        variables = {
                        'institution': institution,
                        'organization': organization,
                        'worst_IC': worst_IC,
                        'best_IC': best_IC,
                        'time_block': time_block,
                        'time_horizon': time_horizon,
                        'results': {}
                     }
    
    markov_model = MarkovContinous(worst_IC, best_IC)

    PI_B = [0.0186, 0.0256, 0.0113, 0.0420]
    PI_CR = [0.0736, 0.1178, 0.1777, 0.3542]
    PI_E = [0.0671, 0.0390, 0.0489, 0.0743]
    PI_F = [0.1773, 0.2108, 0.1071, 0.0765]
    PI_R = [0.1084, 0.0395, 0.0443, 0.0378]
    
    if road['hasFOS']:
        PI_B = 1.1 * np.array(PI_B)
        PI_CR = 1.2 * np.array(PI_B)
    
    df_road = pd.DataFrame(road['inspections'])
    df_road.loc[:, 'Date'] = pd.to_datetime(df_road["Date"], format="%d/%m/%Y")
    
    df_road = df_road.sort_values(by='Date')
    
    thetas = {'Bearing_Capacity_ASFiNAG': PI_B,
              'Cracking_ASFiNAG':PI_CR,
              'Longitudinal_Evenness_ASFiNAG': PI_E,
              'Skid_Resistance_ASFiNAG': PI_F,
              'Transverse_Evenness_ASFiNAG': PI_R}
    
    for key, theta in thetas.items():
        initial_IC = df_road[key].iloc[-1]
        markov_model.theta = theta
        variables['results'][key] = {}
        variables['results'][key]['Time'] = [i for i in range(variables['time_horizon']+1)]
        variables['results'][key]['IC'] = list(markov_model.get_mean_over_time(variables['time_horizon'],
                                                                               initial_IC))
    
    #predict(variables)
        
        
    response = variables['results']
    return response



def predict(variables):
    df_predict = pd.DataFrame()
    df_predict['Time'] = np.arange(variables['time_horizon']+1)
    predict_single_performance_index(variables)
    #self.predict_combined_performance_index(df_predict)

def predict_single_performance_index(variables):
    indicators = variables['organization'].single_performance_index
    for indicator in indicators:
        # try:
            indicator = f"{indicator}_{variables['institution']}"
            model = fit_predict_model(variables, indicator)
            variables['results'][indicator] = {}
            variables['results'][indicator]['Time'] = [i for i in range(variables['time_horizon']+1)]
            variables['results'][indicator]['IC'] = list(model.get_mean_over_time(variables['time_horizon']))
        # except KeyError as e:
        #     print('Error: ',e)

def fit_predict_model(variables, indicator):
    organization = variables['organization']
    df_properties = variables['properties']
    df_inspections = variables['inspections']
    df_standardized = pd.DataFrame(organization(df_properties).transform_performace_indicators(df_inspections))
    df = convert_to_markov(df_standardized[['Section_Name','Date', indicator]],
                                        worst_IC=variables['worst_IC'],
                                        best_IC=variables['best_IC'])
                                        
    return get_fitted_markov_model(df, variables['worst_IC'], variables['best_IC'])


def get_InfraROB_problem(thetas, actions, organization, number_of_samples, time_horizon):
    # Create one performance model for each indicator
    performance_models = {}    
    for key, theta in thetas.items():
        markov = MarkovContinous(worst_IC=5, best_IC=1)
        markov.theta = theta
        filtered_actions = InfraROBRoadProblem.extract_indicator(key, actions)
        performance_models[key] = Performance(markov, filtered_actions)

    InfraROB_problem = InfraROBRoadProblem(
        performance_models = performance_models, 
        organization = organization, 
        time_horizon = time_horizon, 
        number_of_samples = number_of_samples
        )
    return InfraROB_problem

def predict_all_indicators(problem, action_schedule):
    indicators = problem._get_performances(action_schedule)
    indicators = problem._calc_all_indicators([indicators])[0]
    
    def convert_to_list(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
    for key, value in indicators.items():
        indicators[key] = convert_to_list(value)

    return indicators

def handle_PMS_prediction(road_properties, thetas, actions, action_schedule={}, number_of_samples = 100, time_horizon = 50):
    organization = ASFiNAG(road_properties)
    road_category = organization.properties['Street_Category']
    
    filtered_thetas = [theta['thetas'] for theta in thetas if theta["Street_Category"] == road_category][0]
    
    InfraROB_problem = get_InfraROB_problem(filtered_thetas, actions, organization, number_of_samples, time_horizon)
    
    indicators = predict_all_indicators(InfraROB_problem, action_schedule)

    return indicators
        

    