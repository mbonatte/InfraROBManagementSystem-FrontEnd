import unittest
import os
import io
import random
import json

import numpy as np

from handle.handle_prediction import get_IC_through_time, get_IC_through_time_for_road

class TestFlaskApp(unittest.TestCase):
    def setUp(self):        
        main_folder = os.getcwd()
        database_folder = main_folder + "/database"
        
        self.inspections_file_generic = open(database_folder+"/GenericDataBase.csv", 'rb')
        self.inspections_file_asfinag = open(database_folder+"/road_sections_inpections.csv", 'rb')
        self.properties_file_asfinag = open(database_folder+"/road_sections_properties.csv", 'rb')
        self.actions_file = open(database_folder+"/ActionsEffects.json", 'rb')

    def tearDown(self):
        self.inspections_file_generic.close()
        self.inspections_file_asfinag.close()
        self.properties_file_asfinag.close()
        self.actions_file.close()
   

    def test_optimization_generic_post(self):
        # response = self.client.post('/optimization')
        # assert response.status_code == 400
        
        # Create a FormData-like dictionary
        data = {}
        
        # Add values to the data dictionary
        data['institution'] = json.dumps('Generic')
        data['worst_best_IC'] = json.dumps({'worst_IC': 5, 'best_IC': 1})
        data['time_block'] = json.dumps('year')
        data['time_horizon'] = json.dumps(50)
        
        data['inspectionsFile'] = self.inspections_file_generic
        data['maintenanceFile'] = self.actions_file
        
        actions = [{"name": 'action_1',
                   "time_of_reduction": {
                                        "2":[5, 5, 5],
                                        "3":[5, 5, 5]
                                    },
                   "reduction_rate":    {
                                        "2":[0.1, 0.1, 0.1],
                                        "3":[0.1, 0.1, 0.1]
                                    },
                   "cost": 3.70
                   },
                   {"name": 'action_2',
                   "time_of_reduction": {
                                        "2":[5, 5, 5],
                                        "3":[5, 5, 5]
                                    },
                   "reduction_rate": {
                                    "2":[0.1, 0.1, 0.1],
                                    "3":[0.1, 0.1, 0.1]
                                    },
                   "cost": 3.70
                   },
        ]
        
        # data['maintenanceFile'] =  FileStorage(io.BytesIO(bytes(json.dumps(actions), 'utf-8')), 'ActionsEffects.json')
        
        # data['result_id'] = json.dumps('test')
        
        # np.random.seed(1)
        # response = self.client.post('/optimization',
                               # data=data,
                               # content_type='multipart/form-data',
                               # follow_redirects=True,
                               # )
        
        
        # Performance = json.loads(response.data.decode('utf-8'))['Performance']
        # Cost = json.loads(response.data.decode('utf-8'))['Cost']
        
        # self.assertAlmostEqual(Performance[0], 100.10000000000007, places=4)
        # self.assertAlmostEqual(Performance[-1], 71.99999999999995, places=4)
        
        # self.assertAlmostEqual(Cost[0], 10.511947937896857, places=4)
        # self.assertAlmostEqual(Cost[-1], 34.60242103797455, places=4)

if __name__ == "__main__":
    unittest.main()