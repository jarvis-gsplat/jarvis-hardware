import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve AWS credentials and region from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.getenv('AWS_DEFAULT_REGION')
aws_default_output = "json"  # Default output format can be json or text or table

if aws_access_key_id and aws_secret_access_key and aws_default_region:
    # Run the AWS CLI command interactively and provide inputs
    process = subprocess.Popen(
        ["aws", "configure"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Ensures strings are passed instead of bytes
    )

    # Simulate the interactive input for AWS configure (including default output format)
    input_data = f"{aws_access_key_id}\n{aws_secret_access_key}\n{aws_default_region}\n{aws_default_output}\n"
    stdout, stderr = process.communicate(input_data)

    if process.returncode == 0:
        print("AWS configure has been set.")
    else:
        print(f"Error: {stderr}")
else:
    print("Error: Missing AWS credentials or region in .env file.")
