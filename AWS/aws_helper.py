import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def copy_s3_folder(src_bucket_name, src_prefix, dest_bucket_name, dest_prefix):
    """
    Copy objects from one S3 bucket folder to another S3 bucket folder.

    Parameters:
    - src_bucket_name: Name of the source S3 bucket.
    - src_prefix: Prefix (folder) in the source bucket from which to copy objects.
    - dest_bucket_name: Name of the destination S3 bucket.
    - dest_prefix: Prefix (folder) in the destination bucket to which to copy objects.
    """
    # Create an S3 client
    s3 = boto3.client('s3')

    # List objects in the source bucket folder
    response = s3.list_objects_v2(Bucket=src_bucket_name, Prefix=src_prefix)

    # Copy each object to the destination bucket folder
    for obj in response.get('Contents', []):
        src_key = obj['Key']
        dest_key = src_key.replace(src_prefix, dest_prefix, 1)
        s3.copy_object(CopySource={'Bucket': src_bucket_name, 'Key': src_key},
                       Bucket=dest_bucket_name,
                       Key=dest_key)

    print("Folder copied successfully.")

# Example usage:
# copy_s3_folder('source-bucket', 'source-folder/', 'destination-bucket', 'destination-folder/')

    
    
def lambda_handler(event, context):
    s3_bucket = os.getenv("S3_bucket", "data_academy_error")
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    if 'year' in event.keys():
        year = event["year"]
        if 'month' in event.keys() and event['month'] in months:
            month = event["month"]
            download_file(month, year)
            upload_to_aws(f"/tmp/data_{month}_{year}.parquet", s3_bucket, f'data_{month}_{year}.parquet')
        else:
            for count, month in enumerate(months):
                download_file(month, year)
                upload_to_aws(f"/tmp/data_{month}_{year}.parquet", s3_bucket, f'data_{month}_{year}.parquet')

    else:
        raise ValueError("Year missing")

    return {
        'message': "Upload to S3 complete"
    }