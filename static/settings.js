// settings.js

PREDICTION_THETAS = [
        {
            "street_category": "highway",
            "thetas": {
                "Bearing_Capacity": [
                    0.0186,
                    0.0256,
                    0.0113,
                    0.042
                ],
                "Cracking": [
                    0.0736,
                    0.1178,
                    0.1777,
                    0.3542
                ],
                "Longitudinal_Evenness": [
                    0.0671,
                    0.039,
                    0.0489,
                    0.0743
                ],
                "Skid_Resistance": [
                    0.1773,
                    0.2108,
                    0.1071,
                    0.0765
                ],
                "Transverse_Evenness": [
                    0.1084,
                    0.0395,
                    0.0443,
                    0.0378
                ],
                "Surface_Defects": [
                    0.1,
                    0.1,
                    0.1,
                    0.1
                ]
            }
        },
        {
            "street_category": "country_road",
            "thetas": {
                "Bearing_Capacity": [
                    0.0186,
                    0.0256,
                    0.0113,
                    0.042
                ],
                "Cracking": [
                    0.0736,
                    0.1178,
                    0.1777,
                    0.3542
                ],
                "Longitudinal_Evenness": [
                    0.0671,
                    0.039,
                    0.0489,
                    0.0743
                ],
                "Skid_Resistance": [
                    0.1773,
                    0.2108,
                    0.1071,
                    0.0765
                ],
                "Transverse_Evenness": [
                    0.1084,
                    0.0395,
                    0.0443,
                    0.0378
                ],
                "Surface_Defects": [
                    0.1,
                    0.1,
                    0.1,
                    0.1
                ]
            }
        }
    ]

PREDICTION_SETTINGS = {
        "number_of_samples": 100,
        "time_horizon": 50
    }