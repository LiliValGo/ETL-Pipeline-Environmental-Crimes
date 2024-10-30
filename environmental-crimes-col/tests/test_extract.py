# Import libraries 
import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
import requests
import sys
import os
from etl.extract import extract_data  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# A function to sumulate data extraction for testing

class TestExtractData(unittest.TestCase):

    @patch('etl.extract.requests.get')  # Mocking the requests.get function
    def test_extract_data_success(self, mock_get):
        # Simulate a successful response from requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '[{"crime": "deforestation", "location": "Amazon"}]'
        
        # Executing the function
        df = extract_data('https://example.com')

        # Check of the expected result 
        expected_df = pd.DataFrame([{"crime": "deforestation", "location": "Amazon"}])
        pd.testing.assert_frame_equal(df, expected_df)

    @patch('etl.extract.requests.get')
    def test_extract_data_failure(self, mock_get):
        # Simulate an error in requests.get
        mock_get.side_effect = requests.RequestException("Error fetching data")
        
        # Execute of the function and check that it returns an empty DataFrame 
        df = extract_data('https://example.com')
        expected_df = pd.DataFrame()  

        pd.testing.assert_frame_equal(df, expected_df)

if __name__ == '__main__':
    unittest.main()
