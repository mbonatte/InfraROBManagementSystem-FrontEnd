import unittest
import os
import io
import random
import json

import numpy as np

from app import app
from werkzeug.datastructures import FileStorage

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        
        main_folder = os.getcwd()
        database_folder = main_folder + "/database"
        
        self.inspections_file_generic = open(database_folder+"/GenericDataBase.csv", 'rb')
        self.inspections_file_asfinag = open(database_folder+"/road_sections_inpections.csv", 'rb')
        self.properties_file_asfinag = open(database_folder+"/road_sections_properties.csv", 'rb')
        self.actions_file = open(database_folder+"/ActionsEffects.json", 'rb')

    def tearDown(self):
        self.ctx.pop()
        
        self.inspections_file_generic.close()
        self.inspections_file_asfinag.close()
        self.properties_file_asfinag.close()
        self.actions_file.close()

    def test_home(self):
        response = self.client.post("/", data={"content": "hello world"})
        assert response.status_code == 405
    
    def test_markov_generic_post(self):
        response = self.client.post('/markov')
        assert response.status_code == 400
        
        # Create a FormData-like dictionary
        data = {}
        
        # Add values to the data dictionary
        data['institution'] = json.dumps('Generic')
        data['worst_best_IC'] = json.dumps({'worst_IC': 5, 'best_IC': 1})
        data['time_block'] = json.dumps('year')
        data['time_horizon'] = json.dumps(50)
        
        
            
        data['inspectionsFile'] = self.inspections_file_generic
        
        response = self.client.post('/markov',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        
        IC = json.loads(response.data.decode('utf-8'))['IC']
        
        self.assertAlmostEqual(IC[-1], 2.264790029338461, places=6)
        
    def test_markov_asfinag_post(self):
        response = self.client.post('/markov')
        assert response.status_code == 400
        
        # Create a FormData-like dictionary
        data = {}
        
        # Add values to the data dictionary
        data['institution'] = json.dumps('ASFiNAG')
        data['worst_best_IC'] = json.dumps({'worst_IC': 5, 'best_IC': 1})
        data['time_block'] = json.dumps('year')
        data['time_horizon'] = json.dumps(50)
        
        data['inspectionsFile'] = self.inspections_file_asfinag
        data['propertiesFile'] = self.properties_file_asfinag
        
        response = self.client.post('/markov',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        
        #assert response.status_code == 200
        result = json.loads(response.data.decode('utf-8'))
        
        Cracking_ASFiNAG = result['Cracking_ASFiNAG']
        Longitudinal_Evenness_ASFiNAG = result['Longitudinal_Evenness_ASFiNAG']
        Skid_Resistance_ASFiNAG = result['Skid_Resistance_ASFiNAG']
        Surface_Defects_ASFiNAG = result['Surface_Defects_ASFiNAG']
        Transverse_Evenness_ASFiNAG = result['Transverse_Evenness_ASFiNAG']
        
        self.assertAlmostEqual(Cracking_ASFiNAG['IC'][-1], 4.804270142951769, places=6)
        self.assertAlmostEqual(Longitudinal_Evenness_ASFiNAG['IC'][-1], 2.9849168668620782, places=6)
        self.assertAlmostEqual(Skid_Resistance_ASFiNAG['IC'][-1], 2.00000, places=6)
        self.assertAlmostEqual(Surface_Defects_ASFiNAG['IC'][-1], 3.915245847527996, places=6)
        self.assertAlmostEqual(Transverse_Evenness_ASFiNAG['IC'][-1], 4.641938328960139, places=6)
       
    def test_maintenance_generic_post(self):
        response = self.client.post('/maintenance')
        assert response.status_code == 400
        
        # Create a FormData-like dictionary
        data = {}
        
        # Add values to the data dictionary
        data['institution'] = json.dumps('Generic')
        data['worst_best_IC'] = json.dumps({'worst_IC': 5, 'best_IC': 1})
        data['time_block'] = json.dumps('year')
        data['time_horizon'] = json.dumps(50)
        
        data['inspectionsFile'] = self.inspections_file_generic
        data['maintenanceFile'] = self.actions_file
        
        data['maintenanceScenario'] = json.dumps({"5": "Crack sealing"})
        
        random.seed(1)
        #set_seed(1)
        response = self.client.post('/maintenance',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        
        IC = json.loads(response.data.decode('utf-8'))['IC']
        
        self.assertAlmostEqual(IC[-1], 2.18, places=2)
    
    def test_maintenance_asfinag_post(self):
        response = self.client.post('/maintenance')
        assert response.status_code == 400
        
        # Create a FormData-like dictionary
        data = {}
        
        # Add values to the data dictionary
        data['institution'] = json.dumps('ASFiNAG')
        data['worst_best_IC'] = json.dumps({'worst_IC': 5, 'best_IC': 1})
        data['time_block'] = json.dumps('year')
        data['time_horizon'] = json.dumps(50)
        
        data['inspectionsFile'] = self.inspections_file_asfinag
        data['propertiesFile'] = self.properties_file_asfinag
        data['maintenanceFile'] = self.actions_file
        
        data['maintenanceScenario'] = json.dumps({})
        
        random.seed(1)
        response = self.client.post('/maintenance',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        
        IC = json.loads(response.data.decode('utf-8'))#['IC']
        
        self.assertAlmostEqual(IC['Transverse_Evenness_ASFiNAG']['IC'][-1], 4.64, places=2)
        self.assertAlmostEqual(IC['Surface_Defects_ASFiNAG']['IC'][-1], 3.93, places=2)
        self.assertAlmostEqual(IC['Skid_Resistance_ASFiNAG']['IC'][-1], 2.0, places=2)
        self.assertAlmostEqual(IC['Longitudinal_Evenness_ASFiNAG']['IC'][-1], 2.97, places=2)
        self.assertAlmostEqual(IC['Cracking_ASFiNAG']['IC'][-1], 4.81, places=2)
        self.assertAlmostEqual(IC['Bearing_Capacity_ASFiNAG']['IC'][-1], 3.67, places=2)

    def test_optimization_generic_post(self):
        response = self.client.post('/optimization')
        assert response.status_code == 400
        
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
        
        data['maintenanceFile'] =  FileStorage(io.BytesIO(bytes(json.dumps(actions), 'utf-8')), 'ActionsEffects.json')
        
        data['result_id'] = json.dumps('test')
        
        np.random.seed(1)
        response = self.client.post('/optimization',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        
        
        Performance = json.loads(response.data.decode('utf-8'))['Performance']
        Cost = json.loads(response.data.decode('utf-8'))['Cost']
        
        self.assertAlmostEqual(Performance[0], 97.3, places=4)
        self.assertAlmostEqual(Performance[-1],  79.4, places=4)
        
        self.assertAlmostEqual(Cost[0], 0, places=4)
        self.assertAlmostEqual(Cost[-1], 9.09681772796458, places=4)

if __name__ == "__main__":
    unittest.main()