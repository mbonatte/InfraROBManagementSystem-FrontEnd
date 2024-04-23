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

    def test_markov_generic_post(self):
        random.seed(1)
        result = get_IC_through_time(
            inspections = self.inspections_file_generic.read().decode('utf-8'),
            institution = 'Generic',
            worst_IC = 5,
            best_IC = 1, 
            time_block = 'year',
            time_horizon = 50)
        
        self.assertAlmostEqual(result['IC'][-1], 2.264790029338461, places=6)
        
    # def test_markov_asfinag_post(self):
    #     random.seed(1)
    #     result = get_IC_through_time(
    #         inspections = self.inspections_file_asfinag.read().decode('utf-8'),
    #         institution = 'ASFiNAG',
    #         worst_IC = 5,
    #         best_IC = 1, 
    #         time_block = 'year',
    #         time_horizon = 50,
    #         asset_properties = self.properties_file_asfinag.read().decode('utf-8'))
        
    #     Cracking_ASFiNAG = result['Cracking_ASFiNAG']
    #     Longitudinal_Evenness_ASFiNAG = result['Longitudinal_Evenness_ASFiNAG']
    #     Skid_Resistance_ASFiNAG = result['Skid_Resistance_ASFiNAG']
    #     Surface_Defects_ASFiNAG = result['Surface_Defects_ASFiNAG']
    #     Transverse_Evenness_ASFiNAG = result['Transverse_Evenness_ASFiNAG']
    #     Bearing_Capacity_ASFiNAG = result['Bearing_Capacity_ASFiNAG']
        
    #     self.assertAlmostEqual(Cracking_ASFiNAG['IC'][-1], 4.804270142951769, places=6)
    #     self.assertAlmostEqual(Longitudinal_Evenness_ASFiNAG['IC'][-1], 2.9849168668620782, places=6)
    #     self.assertAlmostEqual(Skid_Resistance_ASFiNAG['IC'][-1], 2.00000, places=6)
    #     self.assertAlmostEqual(Surface_Defects_ASFiNAG['IC'][-1], 3.915245847527996, places=6)
    #     self.assertAlmostEqual(Transverse_Evenness_ASFiNAG['IC'][-1], 4.641938328960139, places=6)
    #     self.assertAlmostEqual(Bearing_Capacity_ASFiNAG['IC'][-1], 3.629129444416678, places=6)

if __name__ == "__main__":
    unittest.main()