# Import libraries 
import pandas as pd
import psycopg2
import configparser
import os

# A function to save the given DataFrame as a JSON file 
def load_data(df, output_path=None):
    if output_path:
        try:
            df.to_json(output_path, orient='records', indent=4)
            print(f"JSON file saved in {output_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
        return  

    # Database configuration for loading into PostgreSQL
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

    user = config.get('database', 'user')
    password = config.get('database', 'password')
    host = config.get('database', 'host')
    port = config.get('database', 'port')
    database = config.get('database', 'database')

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        cursor = connection.cursor()

        # Create the table if it doesn't exist 
        create_table_query = '''
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
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created or verified successfully.")

        # Insert the Data into 'environmental_crime' table 
        for i, row in df.iterrows():
            insert_query = '''
            INSERT INTO environmental_projects.environmental_crime (fecha_hecho, cod_depto, departamento, cod_municipio, 
            municipio, delito, zona, cantidad_delitos) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        print("Data successfully insertted into the database.")

    except Exception as e:
        print(f"Error connecting or inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")

