import cv2
from collections import deque
import requests
import shutil 
import os.path

import boto3
from botocore.exceptions import NoCredentialsError

camera_indices = [0, 2, 4]

cameras = [cv2.VideoCapture(idx) for idx in camera_indices]

if any(not cap.isOpened() for cap in cameras):
    print("Error: One or more cameras could not be opened.")
    for cap in cameras:
        cap.release()
    cv2.destroyAllWindows()
    exit()

frame_queues = {idx: deque(maxlen=70) for idx in camera_indices}

try:
    while True:
        for idx, cap in enumerate(cameras):
            ret, frame = cap.read()
            if ret:
                frame_queues[camera_indices[idx]].append(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Process interrupted. Saving frames...")


for idx, queue in frame_queues.items():
    for i, frame in enumerate(queue):
        filename = f'uploads/camera_{idx}_photo_{i+1}.jpg'
        cv2.imwrite(filename, frame)
        print(f'Photo saved: {filename}')

archived = shutil.make_archive('uploads', 'zip', 'uploads')

# Initialize an S3 client
s3_client = boto3.client('s3')

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    # If the object name is not specified, use the file name as the object name
    if object_name is None:
        object_name = file_name

    try:
        # Upload the file to S3
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded successfully to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")

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


# Example usages
file_name = 'uploads.zip'
bucket_name = 'jarvis-zipped-images'
object_name = 'jarviszips'  # Optional: if you want to rename the file in S3

upload_file_to_s3(file_name, bucket_name, object_name)
download_file_from_s3(bucket_name, object_name, file_name=None)

for cap in cameras:
    cap.release()
cv2.destroyAllWindows()


