import numpy as np
from InfraROBManagementSystem.organization.organization import Organization

from handle.utils import convert_np_arrays_to_lists

def flatten_inspection_data(inspections):
    flattened_inspections = {key:[] for key in inspections[0].keys()}
    for inspection in inspections:
        for key in flattened_inspections.keys():
            flattened_inspections[key].append(inspection[key])
    return  flattened_inspections

def unflatten_inspection_data(inspections):
    # Determine the number of inspections by looking at the length of the list of any attribute
    num_inspections = len(next(iter(inspections.values())))
    
    # Create a list of dictionaries, each dictionary representing one inspection
    inspection_list = []
    for i in range(num_inspections):
        # Create a dictionary for each inspection by extracting the ith value from each attribute list
        inspection_dict = {key: inspections[key][i] for key in inspections}
        inspection_list.append(inspection_dict)
    
    return inspection_list



def get_converted_IC(road_sections, organization_name):
    organization = Organization.set_organization(organization_name)
    
    for road_section in road_sections:
        properties = {key:road_section[key] for key in road_section.keys() if key != 'inspections'}
        flattened_inspections = flatten_inspection_data(road_section['inspections'])
        organization(properties).transform_performance_indicators(flattened_inspections)
        road_section['inspections'] = unflatten_inspection_data(flattened_inspections)
    
    return convert_np_arrays_to_lists(road_sections)