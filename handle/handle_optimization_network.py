import numpy as np

from ams.optimization.problem import NetworkProblem
from ams.optimization.multi_objective_optimization import Multi_objective_optimization

from handle.utils import convert_np_arrays_to_lists

   
def get_optimization_output(roads_optimization, res):
    X = res.X               # Design space values
    F = np.array(res.F).T   # Objective spaces
    
    # Sort based on the first objective (performance)
    sort_indices = np.argsort(F[0])

    sorted_F = F[:, sort_indices]
    sorted_X = X[sort_indices]
    
    # Create the output dictionary
    optimization_output = {
        'Performance': np.round(sorted_F[0], 2).tolist(),
        'Cost': np.round(sorted_F[1], 2).tolist(),
        'Actions_schedule': []
    }

    # Extract the actions schedules for each road
    actions_schedules = [road['Actions_schedule'] for road in roads_optimization.values()]    
    
    # Extract schedules using sorted indices
    sorted_X = X[sort_indices]
    for x in sorted_X:
        schedule = [actions_schedules[i][road_index] for i, road_index in enumerate(x)]
        optimization_output['Actions_schedule'].append(schedule)

    # Extract dummy data directly using numpy operations
    dummy_F = np.round(np.array(res.pop.get("F")).T, 2)
    optimization_output['Dummies'] = {
        'Performance': dummy_F[0].tolist(),
        'Cost': dummy_F[1].tolist()
    }
    
    return convert_np_arrays_to_lists(optimization_output)


def handle_PMS_network_optimization(road_optimization,
                            optimization_algorithm = {"name": "NSGA2", "pop_size": 10, "eliminate_duplicates": True},
                            optimization_termination = {"name": "n_gen", "n_max_gen": 5}):
    
    network_problem = NetworkProblem(road_optimization)
        
    optimizer = Multi_objective_optimization()
    optimizer.verbose = False
    optimizer.set_problem(network_problem)
    
    optimizer._set_algorithm(optimization_algorithm)
    optimizer._set_termination(optimization_termination)

    
    optimal_solutions = optimizer.minimize()

    optimization_output = get_optimization_output(road_optimization, optimal_solutions)
    
    return optimization_output