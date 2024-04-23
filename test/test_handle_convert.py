import unittest
from handle.handle_convert import get_converted_IC

class TestFlaskApp(unittest.TestCase):
    def test_get_converted_IC(self):
        data = [
            {
                'Section_Name': 'Road_1_1',
                'Construction_Type': 'AS_N',
                'Road_Category': 'primary',
                'street_category': 'highway',
                'date_asphalt_surface': '01/01/2000',
                'total_pavement_thickness': 20,
                'asphalt_surface_thickness': 2,
                'inspections': [
                    {'Date': '12/01/2015',
                    'Cracking': 4.72e-05,
                    'Surface_Defects': 1.23E-16,
                    'Transverse_Evenness': 1.20E-05,
                    'Longitudinal_Evenness': 0.994939625,
                    'Skid_Resistance': 0.755056374,
                    'Skid_Resistance_Tech': 'SFC',
                    'Bearing_Capacity': 0.5},
                    {'Date': '12/01/2020',
                    'Cracking': 0.006267501,
                    'Surface_Defects': 1.048573308,
                    'Transverse_Evenness': 0.644422995,
                    'Longitudinal_Evenness': 1.017088364,
                    'Skid_Resistance': 0.747573698,
                    'Skid_Resistance_Tech': 'SFC',
                    'Bearing_Capacity': 0.694100299}
                ]
            },
            {
                'Section_Name': 'Road_1_2',
                'Construction_Type': 'AS_N',
                'Road_Category': 'primary',
                'street_category': 'highway',
                'date_asphalt_surface': '01/01/2013',
                'total_pavement_thickness': 20,
                'asphalt_surface_thickness': 2,
                'inspections': [
                    {'Date': '12/01/2017',
                    'Cracking': 0.006267501,
                    'Surface_Defects': 1.048573308,
                    'Transverse_Evenness': 0.644422995,
                    'Longitudinal_Evenness': 1.017088364,
                    'Skid_Resistance': 0.747573698,
                    'Skid_Resistance_Tech': 'SFC',
                    'Bearing_Capacity': 0.694100299}
                ]
            }
        ]
        
        institution = 'ASFiNAG'
        result = get_converted_IC(data,
                                  institution,
                                    )
        
        self.assertEqual(result[0]['inspections'][0]['Skid_Resistance_ASFiNAG'],1)
        self.assertEqual(result[0]['inspections'][0]['Transverse_Evenness_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Longitudinal_Evenness_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Surface_Defects_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Cracking_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Bearing_Capacity_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Safety_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Comfort_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Surface_Structural_ASFiNAG'], 3)
        self.assertEqual(result[0]['inspections'][0]['Functional_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Structural_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Global_ASFiNAG'], 2)


if __name__ == "__main__":
    unittest.main()