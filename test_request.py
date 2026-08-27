import requests

response = requests.post(
    "http://127.0.0.1:5000/predict"
)

print("Status code:", response.status_code)
print("Response:", response.json())