import json
import unittest
import os
import numpy as np
import random

from handle.handle_maintenance import get_IC_through_time_maintenance, get_IC_through_time_maintenance_road

class Test_get_IC_through_time_maintenance(unittest.TestCase):
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
       
    def test_maintenance_generic_post(self):
        random.seed(1)
        result = get_IC_through_time_maintenance(
            inspections = self.inspections_file_generic.read().decode('utf-8'),
            institution = 'Generic',
            maintenance_data = json.loads(self.actions_file.read().decode('utf-8')),
            maintenance_scenario = {"5": "Crack sealing"},
            worst_IC = 5,
            best_IC = 1,
            time_block = 'year',
            time_horizon = 50,
            asset_properties = self.properties_file_asfinag.read().decode('utf-8')
        )
        
        self.assertAlmostEqual(result['IC'][-1], 2.18, places=2)
    
    def test_maintenance_asfinag_post(self):
        random.seed(1)
        IC = get_IC_through_time_maintenance(
            inspections = self.inspections_file_asfinag.read().decode('utf-8'),
            institution = 'ASFiNAG',
            maintenance_data = json.loads(self.actions_file.read().decode('utf-8')),
            maintenance_scenario = {},
            worst_IC = 5,
            best_IC = 1,
            time_block = 'year',
            time_horizon = 50,
            asset_properties = self.properties_file_asfinag.read().decode('utf-8')
        )
        
        self.assertAlmostEqual(IC['Transverse_Evenness_ASFiNAG']['IC'][-1], 4.66, places=2)
        self.assertAlmostEqual(IC['Surface_Defects_ASFiNAG']['IC'][-1], 3.92, places=2)
        self.assertAlmostEqual(IC['Skid_Resistance_ASFiNAG']['IC'][-1], 2.0, places=2)
        self.assertAlmostEqual(IC['Longitudinal_Evenness_ASFiNAG']['IC'][-1], 2.97, places=2)
        self.assertAlmostEqual(IC['Cracking_ASFiNAG']['IC'][-1], 4.79, places=2)
        self.assertAlmostEqual(IC['Bearing_Capacity_ASFiNAG']['IC'][-1], 3.67, places=2)


if __name__ == "__main__":
    unittest.main()