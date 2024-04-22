from InfraROBManagementSystem.convert.organization import Organization

def flatten_section_data(data):
    properties = {key:[] for key in data[0].keys() if key != 'inspections'}
    inspections = {key:[] for key in data[0]['inspections'][0].keys()}
    inspections['Section_Name'] = []
    
    for section in data:
        for key in properties.keys():
            properties[key].append(section[key])
        for inspection in section['inspections']:
            for key in inspections.keys():
                if key != "Section_Name":
                    inspections[key].append(inspection[key])
            inspections['Section_Name'].append(section['Section_Name'])
    
    return  properties, inspections

def get_converted_IC(road_section, organization_name):
    properties, inspections = flatten_section_data(road_section)
    organization = Organization.set_organization(organization_name)
    organization(properties).transform_performace_indicators(inspections)
    return inspections