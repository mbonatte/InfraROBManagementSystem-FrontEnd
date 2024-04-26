import unittest
import random
import json

import numpy as np

from app import app

class TestAPINetworkOptimization(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

        self.json_request = {}
        
        self.json_request['road_optimization'] = {
            "road_1": {
                "Performance": [
                    20,
                    40,
                    60,
                    80,
                    100
                ],
                "Cost": [
                    50,
                    40,
                    30,
                    20,
                    10
                ],
                "Actions_schedule": [
                    {
                        '5': 'Crack sealing', 
                        '9': 'Crack sealing',
                        '37': 'rebuild'
                    },
                    {
                        "37": "rebuild"
                    },
                    {
                        "26": "Crack sealing"
                    },
                    {
                        "40": "Crack sealing"
                    },
                    {}
                ]
            },
            "road_2": {
                "Performance": [
                    20,
                    40,
                    60,
                    80,
                    100
                ],
                "Cost": [
                    50,
                    40,
                    30,
                    20,
                    10
                ],
                "Actions_schedule": [
                    {
                        '5': 'Crack sealing', 
                        '9': 'Crack sealing',
                        '37': 'rebuild'
                    },
                    {
                        "37": "rebuild"
                    },
                    {
                        "26": "Crack sealing"
                    },
                    {
                        "40": "Crack sealing"
                    },
                    {}
                ]
            }
        }
        
        
        self.json_request['optimization_settings'] = {
                "optimization_algorithm": {
                    "name": "NSGA2",
                    "pop_size": 10,
                    "eliminate_duplicates": True

                },
                "optimization_termination": {
                    "name": 'n_gen',
                    'n_max_gen': 1
                }
            }

    def tearDown(self):
        self.ctx.pop()
    
    def test_PMS_prediction(self):
        np.random.seed(1)
        random.seed(1)
        response = self.client.post('/optimization_network',
                                    data=json.dumps(self.json_request),
                                    follow_redirects=True
                                    )
        
        result = json.loads(response.data.decode('utf-8'))
        
        np.testing.assert_array_almost_equal(result['Cost'], [70.0, 70.0, 60.0, 60.0, 40.0, 30.0, 20.0], decimal=6)
        np.testing.assert_array_almost_equal(result['Performance'], [50.0, 50.0, 60.0, 60.0, 80.0, 90.0, 100.0], decimal=6)

        self.assertEqual(list(result['Actions_schedule'][0].values()), [{'37': 'rebuild'}, {'26': 'Crack sealing'}])
        self.assertEqual(list(result['Actions_schedule'][0].keys()), ['road_1', 'road_2'])


if __name__ == "__main__":
    unittest.main()