# Import libraries 
import pandas as pd
import requests
from io import StringIO

# A function to extract data 
def extract_data(filepath):
    try:
        response = requests.get(filepath)
        response.raise_for_status() 
        df_source = pd.read_json(StringIO(response.text))
    except Exception as e:
        print(f"Error reading json file: {e}")
        df_source = pd.DataFrame()
    return df_source

# Save the JSON data into a DataFrame file 
df_environmental_crime = extract_data('https://www.datos.gov.co/resource/9zck-qfvc.json')

