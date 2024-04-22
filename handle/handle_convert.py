from InfraROBManagementSystem.convert.organization import Organization

def get_converted_IC(inspections, properties, organization_name):
    organization = Organization.set_organization(organization_name)
    organization(properties).transform_performace_indicators(inspections)
    return inspections