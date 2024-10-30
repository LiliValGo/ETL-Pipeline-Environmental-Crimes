# Import Libraries
import sys
import os
import logging
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data  
import pandas as pd

# Root directory is in sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up the logger
logger = logging.getLogger('etl_logger')
logger.setLevel(logging.INFO)

# Handler for writing to a log file in the etl-logging folder
file_handler = logging.FileHandler('etl-logging/etl_log.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler for printing to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Function ETL
def extract(filepath):
    logger.info('Starting extraction')
    try:
        df = extract_data(filepath)
        logger.info('Extraction completed')
        return df
    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        return pd.DataFrame()  
    
    
def transform(df):
    logger.info('Starting transformation')
    try:
        df_transformed = transform_data(df)
        logger.info('Transformation completed')
        return df_transformed
    except Exception as e:
        logger.error(f"Transformation failed: {e}", exc_info=True)
        return pd.DataFrame() 
    
     
def load(df):
    logger.info('Starting load')
    try:
        load_data(df)  
        logger.info('Data successfully loaded into the database')
    except Exception as e:
        logger.error(f"Load failed: {e}", exc_info=True)

# Main function of the ETL process 
def etl_process(filepath):
    try:
        logger.info('Starting ETL process')       
        df_environmental_crime = extract(filepath)
        if df_environmental_crime.empty:
            logger.error("No data extracted. Exiting ETL process.")
            return
        
        df_transformed = transform(df_environmental_crime)
        if df_transformed.empty:
            logger.error("No data after transformation. Exiting ETL process.")
            return
        
        load(df_transformed)
        
        logger.info('ETL process completed successfully')
    except Exception as e:
        logger.error('ETL process failed', exc_info=True)

# Execution of the ETL Process
if __name__ == "__main__":
    source_url = 'https://www.datos.gov.co/resource/9zck-qfvc.json'  
    etl_process(source_url)



