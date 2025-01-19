# Description:
Innovative hardware component of JARVIS, utilized to capture images and feed them to our backend. Utilized 4 cameras, connected to a Raspberry Pi 4. These cameras are all used to capture images at an interval, allowing the environment to be processed. A button is then utilized to send the images to an (s3) Amazon server. If there are issues, please consult the how_to_activate_aws.txt file in the repo. Following this, the images are retrieved by the server and processed to produce the necessary result.

# Requirements:

This requires a Raspberry pi and 4 cameras in order to work as currently coded. 
