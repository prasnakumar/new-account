import json
import logging
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# # Enable logging
# logging.basicConfig(level=logging.DEBUG)

credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']
BEDROOM = credential['BEDROOM']
NOTBEDROOM = credential['NOTBEDROOM']

def is_bedroom_image(image_path, subscription_key, endpoint):
    credentials = CognitiveServicesCredentials(subscription_key)
    computer_vision_client = ComputerVisionClient(endpoint, credentials)

    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        image_stream = BytesIO(image_data)

        analysis = analysis = computer_vision_client.describe_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.categories])
        print(analysis.tags)
        if 'bedroom' in analysis.tags:
            return True
        return False
    except Exception as e:
        print("Error:", str(e))
        return False


if __name__ == "__main__":
    image_path = "./a.png" 
    subscription_key = API_KEY
    endpoint = ENDPOINT

    is_bedroom = is_bedroom_image(image_path, subscription_key, endpoint)

    if is_bedroom:
        print("The image contains a bedroom.")
    else:
        print("The image does not contain a bedroom.")
