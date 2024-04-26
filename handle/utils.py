import numpy as np

from ams.prediction.markov import MarkovContinous
from ams.performance.performance import Performance

from InfraROBManagementSystem.organization.ASFiNAG import ASFiNAG
from InfraROBManagementSystem.optimization.problem import InfraROBRoadProblem

    

def get_InfraROB_problem(thetas, actions, organization, initial_ICs, number_of_samples, time_horizon):
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
        number_of_samples = number_of_samples,
        initial_ICs = initial_ICs
        )
    return InfraROB_problem

def get_organization(road_properties, initial_ICs = {}):
    organization = ASFiNAG(road_properties)
    if initial_ICs:
        organization.age = organization._calculate_dates_difference_in_years(organization.date_asphalt_surface, initial_ICs['date'])
    return organization

def predict_all_indicators(problem, action_schedule):
    indicators = problem._get_performances(action_schedule)
    indicators = problem._calc_all_indicators([indicators])[0]
    
    def convert_to_list(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
    for key, value in indicators.items():
        indicators[key] = convert_np_arrays_to_lists(value)

    return indicators

def convert_np_arrays_to_lists(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_np_arrays_to_lists(value)
    elif isinstance(data, list):
        return [convert_np_arrays_to_lists(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.integer):
        return int(data)
    return data