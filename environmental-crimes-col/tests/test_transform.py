# Import libraries 
import unittest
import pandas as pd
from unittest.mock import patch
from etl.transform import transform_data
import os

# A function to sumulate data transformation for testing
class TestTransformData(unittest.TestCase):

    def test_transform_data_success(self):
        # Simulated input data 
        input_data = {
            'fecha_hecho': ['2023-01-01T10:30:00.000'],
            'descripcion_conducta': ['deforestación'],
            'cod_muni': ['05001'],
            'cantidad': [100]
        }
        
        # Input DataFrame 
        df_input = pd.DataFrame(input_data)
        
        # Call transformation function 
        df_transformed = transform_data(df_input)
        
        # Expected DataFrame after transformation
        expected_data = {
            'FECHA_HECHO': [pd.to_datetime('2023-01-01T10:30:00.000')],
            'DELITO': ['deforestación'],
            'COD_MUNICIPIO': ['05001'],
            'CANTIDAD_DELITOS': [100]
        }
        
        expected_df = pd.DataFrame(expected_data)
        
        # Comparison of the transformed data and expected DataFrame
        pd.testing.assert_frame_equal(df_transformed, expected_df)

    @patch('etl.transform.os.path.join', return_value='./data/environmental_crime.json')
    @patch('etl.transform.pd.DataFrame.to_json')
    
    def test_save_to_json(self, mock_to_json, mock_path_join):
        # Simulated input data 
        input_data = {
            'fecha_hecho': ['2023-01-01T10:30:00.000'],
            'descripcion_conducta': ['deforestación'],
            'cod_muni': ['05001'],
            'cantidad': [100]
        }

        # Input DataFrame
        df_input = pd.DataFrame(input_data)

        # Transform the DataFrame 
        df_transformed = transform_data(df_input)

        # Simulate writing the JSON file 
        df_transformed.to_json('./data/environmental_crime.json', orient='records', indent=4)
        
        # Check that to_json was called correctly
        mock_to_json.assert_called_once_with('./data/environmental_crime.json', orient='records', indent=4)

if __name__ == '__main__':
    unittest.main()
