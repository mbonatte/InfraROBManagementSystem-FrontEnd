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
    

if __name__ == "__main__":
    unittest.main()