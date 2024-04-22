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
    
    def test_convert_post_ASFiNAG(self):
        # Create a FormData-like dictionary
        data = {
            'institution': 'ASFiNAG',
            'road_section': [
                {
                    'Section_Name': 'Road_1_1',
                    'Construction_Type': 'AS_N',
                    'Road_Category': 'primary',
                    'Street_Category': 'highway',
                    'Age': '01/01/2013',
                    'Total_Pavement_Thickness': 20,
                    'Asphalt_Thickness': 2,
                    'inspections': [
                        {'Date': '12/01/1993',
                        'Cracking': 4.72e-05,
                        'Surface_Defects': 1.23E-16,
                        'Transverse_Evenness': 1.20E-05,
                        'Longitudinal_Evenness': 0.994939625,
                        'Skid_Resistance': 0.755056374,
                        'Skid_Resistance_Tech': 'SFC',
                        'Bearing_Capacity': 0.5},
                        {'Date': '12/01/1994',
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
                    'Street_Category': 'highway',
                    'Age': '01/01/2013',
                    'Total_Pavement_Thickness': 20,
                    'Asphalt_Thickness': 2,
                    'inspections': [
                        {'Date': '12/01/1994',
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
        
        self.assertEqual(result['Global_ASFiNAG'][0], 2)

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