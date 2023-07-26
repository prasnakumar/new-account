import requests
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

credential=json.load(open('credential.json'))
API_KEY=credential['API_KEY']
ENDPOINT=credential['ENDPOINT']
BEDROOM=credential['BEDROOM']
NOTBEDROOM=credential['NOTBEDROOM']

def is_bedroom_image_from_url(image_url, subscription_key, endpoint):

    credentials = CognitiveServicesCredentials(subscription_key)
    computer_vision_client = ComputerVisionClient(endpoint, credentials)

    try:

        if not image_url.lower().startswith(('http://', 'https://')):
            raise ValueError("Invalid image URL format. The URL should start with 'http://' or 'https://'.")

        analysis = computer_vision_client.describe_image(image_url, visual_features=[VisualFeatureTypes.categories])
        print(analysis.tags)
        if 'bedroom' in analysis.tags:
            return True
        return False
    except Exception as e:
        print("Error:", str(e))
        return False

# Example usage:
if __name__ == "__main__":
    image_url = BEDROOM
    subscription_key = API_KEY
    endpoint = ENDPOINT

    is_bedroom = is_bedroom_image_from_url(image_url, subscription_key, endpoint)

    if is_bedroom:
        print("The image contains a bedroom.")
    else:
        print("The image does not contain a bedroom.")
