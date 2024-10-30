# Import libraries
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd

# Set up s3 client
s3 = boto3.client('s3')  # Default AWS account

# A function to upload a file to s3
def upload_s3_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        s3.upload_file(file_name, bucket, object_name)
        print(f"file {file_name} successfully uploaded to {bucket}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} wasn't found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False

# A function to download and read JSON file from s3 as a DataFrame 
def load_s3_file_as_df(bucket, object_name):
    try:
        # Download the file from S3
        response = s3.get_object(Bucket=bucket, Key=object_name)
        # Read the JSON file content as a DataFrame 
        df = pd.read_json(response['Body'])
        print(f"File {object_name} downloaded and converted to DataFrame.")
        return df
    except Exception as e:
        print(f"An error occurred while downloading or reading the file: {e}")
        return None

# Upload JSON file to s3
json_file = './data/environmental_crime.json'
bucket_s3_name = 'data-environmental'
name_s3_space = 'environmental/environmental_crime.json'
upload_s3_file(json_file, bucket_s3_name, name_s3_space)

# Download and read JSON file as a DataFrame
df_crimes_col = load_s3_file_as_df(bucket_s3_name, name_s3_space)

# Print downloaded DataFrame 
print(df_crimes_col)
