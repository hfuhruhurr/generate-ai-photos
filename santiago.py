import configparser
import requests
import json

# snag secret API key from non-public file
config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config.get("API", "key")

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}

IMAGES = [
    "https://i.natgeofe.com/k/271050d8-1821-49b8-bf0b-3a4a72b6384a/obama-portrait__3x2.jpg",
    "https://d3hjzzsa8cr26l.cloudfront.net/516e6836-d278-11ea-a709-979a0378f022.jpg",
    "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1239961811.jpg"
]

STEM_URL = "https://api.tryleap.ai/api/v1/images/models" 

def create_model(title):
    url = STEM_URL
    
    payload = {
        "title": title,
        "subjectKeyword": "@me"
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)
    
    model_id = json.loads(response.text)["id"]
    
    return model_id


def upload_image_samples(model_id):
	url = f"{STEM_URL}/{model_id}/samples/url"
	payload = {"images": IMAGES}
	response = requests.post(url, json=payload, headers=HEADERS)


def queue_training_job(model_id):
	url = f"{STEM_URL}/{model_id}/queue"
	response = requests.post(url, headers=HEADERS)
	data = json.loads(response.text)
	print(response.text)

	version_id = data["id"]
	status = data["status"]
	print(f"Version ID: {version_id}. Status: {status}")

	return version_id, status


def get_model_version(model_id, version_id):
	url = f"{STEM_URL}/{model_id}/versions/{version_id}"
	response = requests.get(url, headers=HEADERS)
	data = json.loads(response.text)
	
	version_id = data["id"]
	status = data["status"]
	print(f"Version ID: {version_id}. Status: {status}")

	return version_id, status


def generate_image(model_id, prompt):
	url = f"{STEM_URL}/{model_id}/inferences"

	payload = {
		"prompt": prompt,
		"steps": 50,
		"width": 512,
		"height": 512,
		"numberOfImages": 1,
		"seed": 4523184
	}

	response = requests.post(url, json=payload, headers=HEADERS)
	data = json.loads(response.text)

	inference_id = data["id"]
	status = data["status"]

	print(f"Inference ID: {inference_id}. Status: {status}")

	return inference_id, status


def get_inference_job(model_id, inference_id):
	url = f"{STEM_URL}/{model_id}/inferences/{inference_id}"
	response = requests.get(url, headers=HEADERS)
	data = json.loads(response.text)

	inference_id = data["id"]
	state = data["state"]
	
	image = None
	if len(data["images"]):
		image = data["images"][0]["uri"]

	print(f"Inference ID: {inference_id}. State: {state}")

	return inference_id, state, image 


