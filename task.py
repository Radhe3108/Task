import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time

def generate_old_age_image(input_image_path):
    try:
        # Step 1: Upload the image to Fotor and get the session ID
        upload_url = "https://www.fotor.com/images/create"
        image_files = {'image': open(input_image_path, 'rb')}
        upload_response = requests.post(upload_url, files=image_files)

        # Parse the HTML response to extract the session ID
        soup = BeautifulSoup(upload_response.content, 'html.parser')
        session_id_input = soup.find('input', {'name': 'session_id'})

        if session_id_input:
            session_id = session_id_input.get('value')
            if session_id:
                # Step 2: Apply the aging effect and get the aged image URL
                aging_url = f"https://www.fotor.com/showresult?pid=editor&tb=index&editorgp=filters&session_id={session_id}&designId=none&cid=&version=180&smallphto=none&ext=&t=<?xml%20version='1.0'%20encoding='UTF-8'?>%20"
                aging_response = requests.get(aging_url)

                # Parse the HTML response to extract the aged image URL
                aging_soup = BeautifulSoup(aging_response.content, 'html.parser')
                aged_image_url = aging_soup.find('img', {'class': 'aged-image'})['src']

                # Step 3: Download the aged image
                aged_image_response = requests.get(aged_image_url)
                aged_image = Image.open(BytesIO(aged_image_response.content))

                # Step 4: Save the aged image locally
                aged_image.save('aged_image.jpg')

                print("Old age image generated successfully!")
            else:
                print("Session ID not found in response.")
        else:
            print("Input field with name 'session_id' not found in response.")

    except Exception as e:
        print(f"Error: {e}")

# Specify the path to the input image
input_image_path = "input_image.jpg"

# Generate the old age image
generate_old_age_image(input_image_path
