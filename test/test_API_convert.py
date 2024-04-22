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
        
        self.inspections_file_asfinag = open(database_folder+"/road_sections_inpections.csv", 'rb')
        self.properties_file_asfinag = open(database_folder+"/road_sections_properties.csv", 'rb')
        self.actions_file = open(database_folder+"/ActionsEffects.json", 'rb')

    def tearDown(self):
        self.ctx.pop()
        
        self.inspections_file_asfinag.close()
        self.properties_file_asfinag.close()
        self.actions_file.close()

    def test_home(self):
        response = self.client.post("/", data={"content": "hello world"})
        assert response.status_code == 405
    
    def test_convert_post_ASFiNAG(self):
        # Create a FormData-like dictionary
        data = {}

        data['inspectionsFile'] = self.inspections_file_asfinag
        data['propertiesFile'] = self.properties_file_asfinag

        data['institution'] = json.dumps('ASFiNAG')
        
        response = self.client.post('/convert',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True,
                               )
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(result['Global_ASFiNAG'][-1], 4)

    def test_convert_post_COST_354(self):
        # Create a FormData-like dictionary
        data = {}

        data['inspectionsFile'] = self.inspections_file_asfinag
        data['propertiesFile'] = self.properties_file_asfinag

        data['institution'] = json.dumps('COST_354')
        
        # response = self.client.post('/convert',
        #                        data=data,
        #                        content_type='multipart/form-data',
        #                        follow_redirects=True,
        #                        )
        # result = json.loads(response.data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()