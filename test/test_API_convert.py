import unittest
import json

from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
    
    def test_missing_fields(self):
        data = {}  # Empty data
        response = self.client.post('/convert', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.data.decode())

    def test_missing_field(self):
        data = {
            'institution': 'ASFiNAG',
            # Missing 'road_sections' key
        }
        response = self.client.post('/convert', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.data.decode())
    
    def test_processing_key(self):
        data = {
            'institution': 'ASFiNAG',
            'road_sections': [{}]
        }
        response = self.client.post('/convert', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing key inspections', response.data.decode())
    
    def test_processing_error_index_out_of_range(self):
        data = {
            'institution': 'ASFiNAG',
            'road_sections': [{'inspections': []}]
        }
        response = self.client.post('/convert', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.data.decode())

    def test_convert_post_ASFiNAG(self):
        # Create a FormData-like dictionary
        data = {
            'institution': 'ASFiNAG',
            'road_sections': [
                {
                    'Section_Name': 'Road_1_1',
                    'Construction_Type': 'AS_N',
                    'Road_Category': 'primary',
                    'street_category': 'highway',
                    'date_asphalt_surface': '01/01/2000',
                    'total_pavement_thickness': 20,
                    'asphalt_surface_thickness': 2,
                    'inspections': [
                        {'Date': '12/01/2005',
                        'Cracking': 4.72e-05,
                        'Surface_Defects': 1.23E-16,
                        'Transverse_Evenness': 1.20E-05,
                        'Longitudinal_Evenness': 0.994939625,
                        'Skid_Resistance': 0.755056374,
                        'Skid_Resistance_Tech': 'SFC',
                        'Bearing_Capacity': 0.5},
                        {'Date': '12/01/2022',
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
                    'date_asphalt_surface': '01/01/1990',
                    'total_pavement_thickness': 20,
                    'asphalt_surface_thickness': 2,
                    'inspections': [
                        {'Date': '12/01/2010',
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
        }

        
        
        response = self.client.post('/convert',
                               data=json.dumps(data),
                                follow_redirects=True
                               )

        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(result[0]['inspections'][0]['Skid_Resistance_ASFiNAG'],1)
        self.assertEqual(result[0]['inspections'][0]['Transverse_Evenness_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Longitudinal_Evenness_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Surface_Defects_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Cracking_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Bearing_Capacity_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Safety_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Comfort_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Surface_Structural_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Functional_ASFiNAG'], 2)
        self.assertEqual(result[0]['inspections'][0]['Structural_ASFiNAG'], 1)
        self.assertEqual(result[0]['inspections'][0]['Global_ASFiNAG'], 2)

    # def test_convert_post_COST_354(self):
        # Create a FormData-like dictionary
        # data = {}

        # data['inspectionsFile'] = self.inspections_file_asfinag
        # data['propertiesFile'] = self.properties_file_asfinag

        # data['institution'] = json.dumps('COST_354')
        
        # response = self.client.post('/convert',
        #                        data=data,
        #                        content_type='multipart/form-data',
        #                        follow_redirects=True,
        #                        )
        # result = json.loads(response.data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()