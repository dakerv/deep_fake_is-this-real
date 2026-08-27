import requests

IMAGE_PATH = "/deep_fake_is-this-real/dataset/test/real/02262.jpg"

with open(IMAGE_PATH, "rb") as image_file:
    response = requests.post(
    "http://127.0.0.1:5000/predict",
    files={
        "image": image_file
    }
)

print("Status code:", response.status_code)
print("Response:", response.json())