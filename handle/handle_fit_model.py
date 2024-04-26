import pandas as pd
from typing import List, Dict, Any

from ams.prediction.markov import MarkovContinous

from InfraROBManagementSystem.organization.organization import Organization

from handle.utils import convert_np_arrays_to_lists
from handle.handle_convert_to_markov import convert_to_markov
from handle.handle_convert import flatten_inspection_data
    
def get_fitted_markov_model(data: Dict[str, List[int]], worst_ic: int, best_ic: int) -> MarkovContinous:
    """
    Fit a Markov continuous model.
    """
    markov_model = MarkovContinous(worst_ic, best_ic, optimizer=True)
    markov_model.fit(data['Initial'], data['Time'], data['Final'])
    return markov_model

def get_fitted_model(institution: str, road_sections: List[Dict[str, Any]]) -> Dict[str, List[float]]:
    organization = Organization.set_organization(institution)

    merged_inspections = {}
    for section in road_sections:
        flattened = flatten_inspection_data(section['inspections'])
        section_names = [section['Section_Name']] * len(flattened['Date'])
        flattened['Section_Name'] = section_names

        for key, values in flattened.items():
            merged_inspections.setdefault(key, []).extend(values)

    inspection_df = pd.DataFrame(merged_inspections)

    fitted_thetas = {}
    for indicator in organization.single_performance_index:
        formatted_indicator = f"{indicator}_{institution}"
        markov_data = convert_to_markov(
            inspection_df[['Section_Name', 'Date', formatted_indicator]],
            worst_IC=organization.worst_IC,
            best_IC=organization.best_IC
        )
        
        model = get_fitted_markov_model(markov_data, organization.worst_IC, organization.best_IC)
        fitted_thetas[formatted_indicator] = model.theta

    return convert_np_arrays_to_lists(fitted_thetas)