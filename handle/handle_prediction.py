from handle.utils import get_organization, get_InfraROB_problem, predict_all_indicators
    
def handle_PMS_prediction(road_properties, thetas, actions, 
                          action_schedule={},
                          initial_ICs = {},
                          number_of_samples = 100, 
                          time_horizon = 50):
    organization = get_organization(road_properties, initial_ICs)
    road_category = organization.properties['street_category']
    
    filtered_thetas = [theta['thetas'] for theta in thetas if theta["street_category"] == road_category][0]
    
    InfraROB_problem = get_InfraROB_problem(filtered_thetas, actions, organization, initial_ICs, number_of_samples, time_horizon)
    
    indicators = predict_all_indicators(InfraROB_problem, action_schedule)

    return indicators
        

    