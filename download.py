import boto3
from botocore.exceptions import NoCredentialsError

# Initialize an S3 client
s3_client = boto3.client('s3')

def download_file_from_s3(bucket_name, object_name, file_name=None):
    # If the file name is not specified, use the object name as the file name
    if file_name is None:
        file_name = object_name

    try:
        # Download the file from S3
        s3_client.download_file(bucket_name, object_name, file_name)
        print(f"File {object_name} downloaded successfully to {file_name}")
    except FileNotFoundError:
        print(f"The local file path {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    file_name = 'downloads.jarvis'  # Local file path for the download
    bucket_name = 'jarvis-zipped-images'
    object_name = 'jarviszips'  # The object name in S3

    download_file_from_s3(bucket_name, object_name, file_name)
