# Import libraries
import boto3

# A function to connect s3 client
def get_s3_client_and_bucket():
    s3 = boto3.client('s3')
    bucket_name = 'data-environmental' 
    return {"s3": s3, "bucket_name": bucket_name}
