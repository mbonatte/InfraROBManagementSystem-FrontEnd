import unittest
import random
import json

from app import app

class TestAPIPrediction(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

        self.json_request = {}
        self.json_request['prediction_thetas'] = [{
                    "street_category": "highway",
                    "thetas": {
                        "Bearing_Capacity": [0.0186, 0.0256, 0.0113, 0.0420],
                        "Cracking":[0.0736, 0.1178, 0.1777, 0.3542],
                        "Longitudinal_Evenness": [0.0671, 0.0390, 0.0489, 0.0743],
                        "Skid_Resistance": [0.1773, 0.2108, 0.1071, 0.0765],
                        "Transverse_Evenness": [0.1084, 0.0395, 0.0443, 0.0378],
                        "Surface_Defects": [0.1, 0.1, 0.1, 0.1]
                        }
                }]
        
        self.json_request['actions_effect'] =[
                {
                    "name": "rebuild",
                    "cost": 50,
                    "Cracking": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    },
                    "Surface_Defects": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    },
                    "Skid_Resistance": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    },
                    "Transverse_Evenness": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    },
                    "Longitudinal_Evenness": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    },
                    "Bearing_Capacity": {
                        "improvement": {
                            "2": [1, 1, 1],
                            "3": [2, 2, 2],
                            "4": [3, 3, 3],
                            "5": [4, 4, 4]
                        }
                    }
                },
                {
                    "name": "Crack sealing",
                    "Bearing_Capacity": {
                        "time_of_reduction":   {
                            "2":[2, 2, 2],
                            "3":[1, 1, 1]
                        },
                        "reduction_rate":  {
                            "2":[0.2, 0.2, 0.2],
                            "3":[0.2, 0.2, 0.2]
                        }
                    },
                    "Cracking": {
                        "time_of_reduction":   {
                            "2":[2, 2, 2],
                            "3":[2, 2, 2],
                            "4":[1, 1, 1]
                        },
                        "reduction_rate":  {
                            "2":[0.2, 0.2, 0.2],
                            "3":[0.1, 0.1, 0.1],
                            "4":[0.1, 0.1, 0.1]
                        }
                    },
                    "Transverse_Evenness": {
                        "time_of_reduction":    {
                            "2":[2, 2, 2],
                            "3":[1, 1, 1]},
                        "reduction_rate":  {
                            "2":[0.2, 0.2, 0.2],
                            "3":[0.2, 0.2, 0.2]
                            }
                    },
                    "cost": 3.70
                },
                {
                    "name": "action_2",
                    "cost": 5,
                    "Bearing_Capacity": {
                        "time_of_reduction": {
                            "2": [5, 5, 5],
                            "3": [5, 5, 5]
                        },
                        "reduction_rate":    {
                            "2": [0.1, 0.1, 0.1],
                            "3": [0.1, 0.1, 0.1]
                        }
                    },
                    "Transverse_Evenness": {
                        "time_of_reduction": {
                            "2": [5, 5, 5],
                            "3": [5, 5, 5]
                        },
                        "reduction_rate":    {
                            "2": [0.1, 0.1, 0.1],
                            "3": [0.1, 0.1, 0.1]
                        }
                    }
                }
            ]
        
        self.json_request['road_properties'] = {
                "Section_Name": "road_1_1",
                "asphalt_surface_thickness": 3,
                "total_pavement_thickness": 3,
                "street_category": "highway",
                "date_asphalt_surface": "01/01/2013",
            }
        
        self.json_request['prediction_settings'] = {
                "number_of_samples": 100,
                "time_horizon": 50
            }

    def tearDown(self):
        self.ctx.pop()
    
    def test_PMS_prediction(self):
        random.seed(1)
        response = self.client.post('/prediction',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertAlmostEqual(result['Transverse_Evenness'][-1], 3.54, places=6)
        self.assertAlmostEqual(result['Surface_Defects'][-1],  4.61, places=6)
        self.assertAlmostEqual(result['Skid_Resistance'][-1], 4.86, places=6)
        self.assertAlmostEqual(result['Longitudinal_Evenness'][-1], 3.38, places=6)
        self.assertAlmostEqual(result['Cracking'][-1], 4.65, places=6)
        self.assertAlmostEqual(result['Bearing_Capacity'][-1], 2.04, places=6)
        
        self.assertAlmostEqual(result['Surface_Structural'][10], 2.084, places=6)
        self.assertAlmostEqual(result['Surface_Structural'][-1], 5, places=6)
        self.assertAlmostEqual(result['Structural'][-1], 3.52, places=6)
        
        self.assertAlmostEqual(result['Comfort'][-1], 4.961457142857145, places=6)
        self.assertAlmostEqual(result['Safety'][-1], 5, places=6)
        self.assertAlmostEqual(result['Functional'][-1], 5, places=6)
        
        self.assertAlmostEqual(result['Global'][-1], 5, places=6)

    def test_PMS_prediction_last_inspection(self):
        self.json_request["initial_ICs"] = {
                    "date": "12/01/2100",
                    "Cracking":	1,
                    "Surface_Defects": 1,
                    "Transverse_Evenness": 1,
                    "Longitudinal_Evenness": 1,
                    "Skid_Resistance": 5,
                    "Bearing_Capacity": 2
                }
        
        random.seed(1)
        response = self.client.post('/prediction',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertAlmostEqual(result['Transverse_Evenness'][-1], 3.54, places=6)
        self.assertAlmostEqual(result['Surface_Defects'][-1],  4.61, places=6)
        self.assertAlmostEqual(result['Skid_Resistance'][-1], 5, places=6)
        self.assertAlmostEqual(result['Longitudinal_Evenness'][-1], 3.38, places=6)
        self.assertAlmostEqual(result['Cracking'][-1], 4.65, places=6)
        self.assertAlmostEqual(result['Bearing_Capacity'][-1], 2.99, places=6)
        
        self.assertAlmostEqual(result['Surface_Structural'][10], 2.084, places=6)
        self.assertAlmostEqual(result['Surface_Structural'][-1], 5, places=6)
        self.assertAlmostEqual(result['Structural'][-1], 3.995, places=6)
        
        self.assertAlmostEqual(result['Comfort'][-1], 4.961457142857145, places=6)
        self.assertAlmostEqual(result['Safety'][-1], 5, places=6)
        self.assertAlmostEqual(result['Functional'][-1], 5, places=6)
        
        self.assertAlmostEqual(result['Global'][-1], 5, places=6)

    def test_PMS_prediction_with_maintenance(self):
        self.json_request['action_schedule'] = {
                "5": 'Crack sealing',
                "10": 'Crack sealing',
                "20": 'action_2',
                "30": 'rebuild',
            }
        random.seed(1)
        response = self.client.post('/prediction',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertAlmostEqual(result['Transverse_Evenness'][-1], 2.43, places=6)
        self.assertAlmostEqual(result['Surface_Defects'][-1],  2.91, places=6)
        self.assertAlmostEqual(result['Skid_Resistance'][-1], 3.8, places=6)
        self.assertAlmostEqual(result['Longitudinal_Evenness'][-1], 2.09, places=6)
        self.assertAlmostEqual(result['Cracking'][-1], 3.12, places=6)
        self.assertAlmostEqual(result['Bearing_Capacity'][-1], 1.43, places=6)
        
        self.assertAlmostEqual(result['Surface_Structural'][-1], 3.311, places=6)
        self.assertAlmostEqual(result['Structural'][-1], 2.3705, places=6)
        
        self.assertAlmostEqual(result['Comfort'][-1], 2.1942314285714286, places=6)
        self.assertAlmostEqual(result['Safety'][-1], 3.943, places=6)
        self.assertAlmostEqual(result['Functional'][-1], 4.062423142857143, places=6)
        
        self.assertAlmostEqual(result['Global'][-1], 4.062423142857143, places=6)

if __name__ == "__main__":
    unittest.main()