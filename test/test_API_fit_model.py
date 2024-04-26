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
        response = self.client.post('/fit_model', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.data.decode())

    def test_missing_key_field(self):
        data = {
            'road_sections': []  # Missing 'institution' key
        }
        response = self.client.post('/fit_model', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.data.decode())

    def test_processing_error_key(self):
        data = {
            'institution': 'ASFiNAG',
            'road_sections': [{}]
        }
        response = self.client.post('/fit_model', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing key inspections', response.data.decode())
    
    def test_processing_error_index_out_of_range(self):
        data = {
            'institution': 'ASFiNAG',
            'road_sections': [{'inspections': []}]
        }
        response = self.client.post('/fit_model', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('list index out of range', response.data.decode())

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
                        'Cracking_ASFiNAG': 1,
                        'Surface_Defects_ASFiNAG': 1,
                        'Transverse_Evenness_ASFiNAG': 1,
                        'Longitudinal_Evenness_ASFiNAG': 1,
                        'Skid_Resistance_ASFiNAG': 1,
                        'Bearing_Capacity_ASFiNAG': 1},
                        {'Date': '12/01/2010',
                        'Cracking_ASFiNAG': 2,
                        'Surface_Defects_ASFiNAG': 2,
                        'Transverse_Evenness_ASFiNAG': 2,
                        'Longitudinal_Evenness_ASFiNAG': 2,
                        'Skid_Resistance_ASFiNAG': 2,
                        'Bearing_Capacity_ASFiNAG': 2},
                        {'Date': '12/01/2022',
                        'Cracking_ASFiNAG': 5,
                        'Surface_Defects_ASFiNAG': 5,
                        'Transverse_Evenness_ASFiNAG': 5,
                        'Longitudinal_Evenness_ASFiNAG': 5,
                        'Skid_Resistance_ASFiNAG': 5,
                        'Bearing_Capacity_ASFiNAG': 5}
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
                        'Cracking_ASFiNAG': 2,
                        'Surface_Defects_ASFiNAG': 2,
                        'Transverse_Evenness_ASFiNAG': 2,
                        'Longitudinal_Evenness_ASFiNAG': 2,
                        'Skid_Resistance_ASFiNAG': 2,
                        'Bearing_Capacity_ASFiNAG': 2},
                        {'Date': '12/01/2022',
                        'Cracking_ASFiNAG': 4,
                        'Surface_Defects_ASFiNAG': 4,
                        'Transverse_Evenness_ASFiNAG': 4,
                        'Longitudinal_Evenness_ASFiNAG': 4,
                        'Skid_Resistance_ASFiNAG': 4,
                        'Bearing_Capacity_ASFiNAG': 4}
                    ]
                }
            ]
        }

        
        
        response = self.client.post('/fit_model',
                               data=json.dumps(data),
                                    follow_redirects=True
                               )
        

        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(result['Bearing_Capacity_ASFiNAG'], [0.2, 0.0, 30.0, 30.0, 30.00000001490116])
        

if __name__ == "__main__":
    unittest.main()