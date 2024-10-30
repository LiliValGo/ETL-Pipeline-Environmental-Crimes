# Import libraries
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from etl.load import load_data  # Asegúrate de importar correctamente
import os

# A function to sumulate data load for testing

class TestLoadData(unittest.TestCase):

    @patch("etl.load.pd.DataFrame.to_json")
    def test_load_data_to_json(self, mock_to_json):
        # Create a sample DataFrame
        df = pd.DataFrame({
            'fecha_hecho': ['2023-01-01'],
            'cod_depto': [5],
            'departamento': ['Antioquia'],
            'cod_municipio': [5001],
            'municipio': ['Medellín'],
            'delito': ['deforestación'],
            'zona': ['rural'],
            'cantidad_delitos': [10]
        })
        
        # Set a simulated output path
        output_path = './data/test_environmental_crime.json'
        
        # Call the function with `output_path`
        load_data(df, output_path=output_path)

        # Check that to_json was called correctly
        mock_to_json.assert_called_once_with(output_path, orient='records', indent=4)

    @patch('etl.load.psycopg2.connect')
    @patch('etl.load.configparser.ConfigParser.get')
    def test_load_data_to_database(self, mock_config_get, mock_connect):
        # Set up credentials
        mock_config_get.side_effect = lambda section, key: {
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost',
            'port': '5432',
            'database': 'test_db'
        }[key]
        
        # Create a sample DataFrame
        df = pd.DataFrame({
            'fecha_hecho': ['2023-01-01'],
            'cod_depto': [5],
            'departamento': ['Antioquia'],
            'cod_municipio': [5001],
            'municipio': ['Medellín'],
            'delito': ['deforestación'],
            'zona': ['rural'],
            'cantidad_delitos': [10]
        })
        
        # Simulate the conection 
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_connect.return_value = mock_conn

        # call the function to load the data into the database 
        load_data(df)

        # Check that the table was created 
        mock_cursor.execute.assert_any_call('''
        CREATE TABLE IF NOT EXISTS environmental_projects.environmental_crime (
        fecha_hecho DATE,
        cod_depto INTEGER,
        departamento VARCHAR(255),
        cod_municipio INTEGER,
        municipio VARCHAR(255),
        delito VARCHAR(500),
        zona VARCHAR(100),
        cantidad_delitos INTEGER
        );
        ''')

        # Check that the data was inserted 
        insert_query = '''
            INSERT INTO environmental_projects.environmental_crime (fecha_hecho, cod_depto, departamento, cod_municipio, 
            municipio, delito, zona, cantidad_delitos) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
        mock_cursor.execute.assert_any_call(insert_query, ('2023-01-01', 5, 'Antioquia', 5001, 'Medellín', 'deforestación', 'rural', 10))

        # Check that the `commit` was called
        mock_conn.commit.assert_called()

        # Check that the conection and cursor was closed 
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

