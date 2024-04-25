import numpy as np

from ams.optimization.multi_objective_optimization import Multi_objective_optimization

from handle.utils import get_organization, get_InfraROB_problem, predict_all_indicators, convert_np_arrays_to_lists

# def get_pareto_curve_all_roads(thetas, organization_name='ASFiNAG', number_of_samples = 100, time_horizon = 50):
#     import json
#     from pathlib import Path
#     import pandas as pd
#     from handle.handle_convert import get_converted_IC
#     MAIN_FOLDER = Path(__file__).parent.parent.resolve()
    
#     path_properties = MAIN_FOLDER / './database/road_sections_properties.csv'
#     road_properties = pd.read_csv(path_properties).to_dict('records')
    
#     path = MAIN_FOLDER / 'database/ActionsEffects.json'
#     with open(path, "r") as file:
#         maintenance_data = json.load(file)
    
#     optimization_outputs = {}
    
#     for road in enumerate(road_properties):
#         converted_inspections = get_converted_IC(road, organization_name)
#         initial_ICs = converted_inspections[0]['inspections'][-1]
        
#         organization = get_organization(road_properties, initial_ICs)
#         road_category = organization.properties['street_category']
        
#         filtered_thetas = [theta['thetas'] for theta in thetas if theta["street_category"] == road_category][0]
        
#         InfraROB_problem = get_InfraROB_problem(filtered_thetas, maintenance_data, organization, initial_ICs, number_of_samples, time_horizon)

#         optimization = Multi_objective_optimization()
#         optimization.set_problem(InfraROB_problem)

#         optimization._set_algorithm(optimization_algorithm)
#         optimization._set_termination(optimization_termination)
        
#         res = optimization.minimize()
#         optimization_output = get_optimization_output(optimization, res)
#         optimization_outputs[road['Section_Name']] = optimization_output
    
#     optimization_outputs = convert_np_arrays_to_lists(optimization_outputs)
    
#     # Writing to optimization_output.json
#     path = MAIN_FOLDER / 'database/optimization_output_.json'
#     with open(path, "r+") as file:
#         data = json.load(file)
#         data.update(optimization_outputs)
#         file.seek(0)
#         file.write(json.dumps(data,
#                               indent=4))
    
#     return optimization_outputs
    
def get_optimization_output(optimization, res):
    problem = optimization.problem
    performance_model = problem.performance_models
    
    X = res.X               # Design space values
    F = res.F               # Objective spaces
    opt = res.opt           # The solutions as a Population object.
    pop = res.pop           # The final Population
    history = res.history   # The history of the algorithm. (only if save_history has been enabled during the algorithm initialization)
 
    F = np.array(F).T
    sort = np.argsort(F)[0] # Sort the performance
    
    optimization_output = {}
    
    optimization_output['Performance'] = np.round(F[0][sort], 2)
    optimization_output['Cost'] = np.round(F[1][sort], 2)
    optimization_output['Actions_schedule'] = [problem._decode_solution(item) for item in X[sort]]
    
    optimization_output['Prediction'] = []
    
    for actions_schedule in optimization_output['Actions_schedule']:
        result = {}
        result['Time'] = list(range(0, problem.time_horizon + 1))
        result['IC'] = predict_all_indicators(problem, actions_schedule)
        
        optimization_output['Prediction'].append(result)
    
    optimization_output['Dummies'] = {}
    optimization_output['Dummies']['Performance'] = np.round(np.array(pop.get("F")).T[0], 2)
    optimization_output['Dummies']['Cost'] = np.round(np.array(pop.get("F")).T[1], 2)
    
    return convert_np_arrays_to_lists(optimization_output)


def handle_PMS_optimization(road_properties, thetas, actions, 
                            initial_ICs = {},
                            number_of_samples = 100, 
                            time_horizon = 50,
                            optimization_algorithm = {"name": "NSGA2", "pop_size": 10, "eliminate_duplicates": True},
                            optimization_termination = {"name": "n_gen", "n_max_gen": 5}):
    
    organization = get_organization(road_properties, initial_ICs)
    road_category = organization.properties['street_category']
    
    filtered_thetas = [theta['thetas'] for theta in thetas if theta["street_category"] == road_category][0]
    
    InfraROB_problem = get_InfraROB_problem(filtered_thetas, actions, organization, initial_ICs, number_of_samples, time_horizon)
    
    optimizer = Multi_objective_optimization()
    optimizer.set_problem(InfraROB_problem)

    optimizer._set_algorithm(optimization_algorithm)
    optimizer._set_termination(optimization_termination)
    
    optimal_solutions = optimizer.minimize()

    optimization_output = get_optimization_output(optimizer, optimal_solutions)
    
    return optimization_output