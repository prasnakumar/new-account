import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def get_area_of_interest(subscription_key, endpoint, input_image_path, output_image_path):
    analyze_url = f"{endpoint}/vision/v3.1/analyze"


    params = {"visualFeatures": "Objects"}


    with open(input_image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {"Content-Type": "application/octet-stream", "Ocp-Apim-Subscription-Key": subscription_key}

    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)


    response_json = response.json()


    if "objects" in response_json:
        objects = response_json["objects"]

  
        with Image.open(BytesIO(image_data)) as img:
            draw = ImageDraw.Draw(img)


            font_size = 90
            font = ImageFont.truetype("arial.ttf", font_size)

            # Loop through all the detected objects and draw rectangles with labels
            for obj in objects:
              
                if  "bed".lower() == obj["object"].lower():
                    rectangle = obj["rectangle"]
                    left, top, width, height = rectangle["x"], rectangle["y"], rectangle["w"], rectangle["h"]

    
                    draw.rectangle([left, top, left + width, top + height], outline="red", width=8)

  
                    label = obj["object"]
                    draw.text((left+20, top + 10), label, fill="red", font=font)
                    print("BED FOUND");
                elif "parent" in obj  and  "bed".lower() == obj["parent"]["object"].lower():
                    rectangle = obj["rectangle"]
                    left, top, width, height = rectangle["x"], rectangle["y"], rectangle["w"], rectangle["h"]

    
                    draw.rectangle([left, top, left + width, top + height], outline="red", width=8)

  
                    label = obj["parent"]["object"]
                    draw.text((left+20, top + 10), label, fill="red", font=font)
                    print("BED FOUND");



            



            img.save(output_image_path, format="PNG")

credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']


CUSTOM_FOLDER = "custom_folder"
subscription_key = API_KEY
endpoint = ENDPOINT 
input_image_path = "./sample2.png" 
output_image_path = "output_image.png" 


get_area_of_interest(subscription_key, endpoint, input_image_path, output_image_path)
