# Import libraries 
import pandas as pd
from etl.extract import df_environmental_crime 
import os

# A function to transform the DataFrame 
def transform_data(df):
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'], 
                                        errors='coerce', format='%Y-%m-%dT%H:%M:%S.%f')
    df.rename(columns={'descripcion_conducta': 'delito', 'cod_muni': 'cod_municipio', 'cantidad': 'cantidad_delitos'}, 
              inplace=True)
    df.columns = df.columns.str.upper()
    return df

df_environmental_crime = transform_data(df_environmental_crime)


# Save the transformed DataFrame as a JSON file
folder_path = './data'  
filename = 'environmental_crime.json'
file_path = os.path.join(folder_path, filename)
df_environmental_crime.to_json(file_path, orient='records', indent=4)
print(f"Archivo JSON guardado en {file_path}")
