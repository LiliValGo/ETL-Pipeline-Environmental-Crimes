# Import libraries 
import json
import boto3
from datetime import datetime
from lambda_s3_config import get_s3_client_and_bucket
from lambda_s3_keys import get_file_keys
from lambda_s3_download import download_files_from_s3

s3_client = boto3.client('s3')

# A function to serialize datetime objects to JSON 
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def lambda_handler(event, context):
    # Step 1: Get the client s3 and bucket name 
    s3_data = get_s3_client_and_bucket()
    s3 = s3_data['s3']
    bucket_name = s3_data['bucket_name']
    
    # Step 2: 
    # Get the keys from s3 files 
    keys = get_file_keys()

    # Check that `keys` is a dictionary 
    if not isinstance(keys, dict):
        raise TypeError(f"A dictionary was expected for`keys`, but a different type was received {type(keys)}")
    
    # Check that `keys` contains the required key 'crimes_key'
    if 'crimes_key' not in keys:
        raise KeyError("La clave 'crimes_key' no está presente en `keys`")

    # Step 3: Loading s3 files 
    response = download_files_from_s3(s3, bucket_name, keys)
    
    # Reading the s3 file content  
    file_content = response['crimes_response']['Body'].read().decode('utf-8')
    
    # Step 4: Save s3 processed content
    processed_file_key = f"processed/{keys['crimes_key']}_processed_{datetime.now().isoformat()}.txt"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=processed_file_key,
        Body=file_content
    )
    
    # Step 5: Get the current time
    now = datetime.now()
    current_time = now.isoformat()

    # Step 6: Return only the link to the processed file
    s3_file_url = f"https://{bucket_name}.s3.amazonaws.com/{processed_file_key}"
    
    # Response with the time and link to the processed file
    combined_response = {
        "current_time": current_time,
        "s3_file_url": s3_file_url
    }

    # Serialize the response using the custom serializer for datetime
    return {
        'statusCode': 200,
        'body': json.dumps(combined_response, default=custom_serializer)
    }
