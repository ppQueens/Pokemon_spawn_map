import os
import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(local_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    file = os.path.split(local_file)[1]
    try:
        s3.upload_file(local_file, os.environ['S3_BUCKET_NAME'], file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        url = 'https://{0}.s3.eu-central-1.amazonaws.com/{1}'.format(os.environ['S3_BUCKET_NAME'], file)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
