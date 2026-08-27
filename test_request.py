import requests

IMAGE_PATH = "dataset/test/real/real_8672.png"

with open(IMAGE_PATH, "rb") as image_file:
    response = requests.post(
    "http://127.0.0.1:5000/predict",
    files={
        "image": image_file
    }
)

print("Status code:", response.status_code)
print("Response:", response.json())