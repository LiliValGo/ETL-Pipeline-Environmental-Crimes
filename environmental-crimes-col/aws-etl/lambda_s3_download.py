# Import Libraries 
import boto3

# A function to download files from s3 
def download_files_from_s3(s3, bucket_name, keys):
    crimes_response = s3.get_object(Bucket=bucket_name, Key=keys['crimes_key'])
    return {
        "crimes_response": crimes_response
    } 
 
