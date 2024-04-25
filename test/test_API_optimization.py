import unittest
import random
import json

import numpy as np

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
                "number_of_samples": 1,
                "time_horizon": 50
            }
        
        self.json_request['optimization_settings'] = {
                "optimization_algorithm": {
                    "name": "NSGA2",
                    "pop_size": 1,
                    "eliminate_duplicates": True

                },
                "optimization_termination": {
                    "name": 'n_gen',
                    'n_max_gen': 1
                }
            }

    def tearDown(self):
        self.ctx.pop()
    
    def test_PMS_optimization(self):
        np.random.seed(1)
        random.seed(1)
        response = self.client.post('/optimization',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(result['Actions_schedule'][0], {'37': 'action_2', '5': 'action_2', '9': 'action_2'})
        self.assertAlmostEqual(result['Cost'][0],  12.79, places=6)
        self.assertAlmostEqual(result['Performance'][0], 190.45, places=6)

        self.assertAlmostEqual(result['Dummies']['Cost'][0],  12.79, places=6)
        self.assertAlmostEqual(result['Dummies']['Performance'][0], 190.45, places=6)

        self.assertAlmostEqual(len(result['Prediction'][0]['Time']), 51, places=6)
        
        self.assertEqual(list(result['Prediction'][0]['IC'].keys()), [
            'Bearing_Capacity',
            'Comfort',
            'Cracking',
            'Functional',
            'Global',
            'Longitudinal_Evenness',
            'Safety',
            'Skid_Resistance',
            'Structural',
            'Surface_Defects',
            'Surface_Structural',
            'Transverse_Evenness']
        )

        self.assertEqual(result['Prediction'][0]['IC']['Global'][0], 1.102087)

    def test_PMS_optimization_last_inspection(self):
        self.json_request["initial_ICs"] = {
                    "date": "01/01/2020",
                    "Cracking":	5,
                    "Surface_Defects": 5,
                    "Transverse_Evenness": 5,
                    "Longitudinal_Evenness": 5,
                    "Skid_Resistance": 5,
                    "Bearing_Capacity": 5
                }
        
        np.random.seed(1)
        random.seed(1)
        response = self.client.post('/optimization',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertAlmostEqual(result['Performance'][0], 255, places=6)
        
        self.assertEqual(result['Prediction'][0]['IC']['Global'][0], 5)


if __name__ == "__main__":
    unittest.main()