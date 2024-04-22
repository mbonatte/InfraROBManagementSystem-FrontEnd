import unittest
from handle.handle_convert import get_converted_IC

class TestFlaskApp(unittest.TestCase):
    def test_get_converted_IC(self):
        institution = 'ASFiNAG'
        
        df_inspections  = {
            'Section_Name': ['Road_1_1', 'Road_1_2'],
            'Date': ['12/01/1993', '12/01/1994'],
            'Cracking': [4.72e-05, 0.006267501],
            'Surface_Defects':	[1.23E-16, 1.048573308],
            'Transverse_Evenness':	[1.20E-05, 0.644422995],
            'Longitudinal_Evenness':	[0.994939625, 1.017088364],
            'Skid_Resistance':[0.755056374, 0.747573698],
            'Skid_Resistance_Tech':	['SFC', 'SFC'],
            'Bearing_Capacity': [0.5, 0.694100299],
            }
        
        properties_data  = {
            'Section_Name': ['Road_1_1', 'Road_1_2'],
            'Construction_Type': ['AS_N', 'AS_N'],
            'Road_Category': ['primary', 'primary'],
            'Street_Category':	['highway', 'highway'],
            'Age':	['01/01/2013', '01/01/2013'],
            'Total_Pavement_Thickness':	[20, 20],
            'Asphalt_Thickness':[2, 2], 
            }

        result = get_converted_IC(df_inspections,
                                    properties_data,
                                    institution,
                                    )
        
        self.assertEqual(result['Global_ASFiNAG'][0], 2)
                                        

if __name__ == "__main__":
    unittest.main()