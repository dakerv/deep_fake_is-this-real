from flask import Flask, request
import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
from torchvision.models import efficientnet_b0
import torch.nn as nn

NUM_CLASSES = 3
DEVICE = "cpu"

model = efficientnet_b0(
    weights=None
)

model.classifier[1] = nn.Linear(
    1280,
    NUM_CLASSES
)

checkpoint = torch.load( # loading the best saved model
    "../models/efficientnet_b0.pth",
    map_location=DEVICE
)

model.load_state_dict( # loading the weights from the best saved model
    checkpoint["model_state_dict"]
)

model.to(DEVICE)
model.eval() # no learning, just predictions

inference_transform = transforms.Compose( # transformations from validation and evaluation, with added resizing of images.
    [
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ]
)

app = Flask(__name__) # creates flask application

@app.route("/") # Initial route named '/' sends GET request by default because we didn't specify
def home():
    return "Deepfake Detection Backend is running!" # message received when someone visits

@app.route("/predict", methods=['POST']) # route which is /predict, POST is a request
def predict(): 
    print("\nPrediction request received")

    if "image" not in request.files:
        return {
            "error": "No image was provided"
        }, 400

    image = request.files["image"] # request helps us ask for something in order to do something

    if image.filename == "": # in case user didn't select a file but clicked button to show prediction.
        return {
        "error": "No image was selected"
    }, 400

    print(f"Received image: {image.filename}")

    try:
        image = Image.open(image).convert("RGB")

    except UnidentifiedImageError: # send an error instead of crushing if image is unsuitable in any way
        return {
            "error": "The uploaded file is not a valid image"
        }, 400

    image_tensor = inference_transform(image)

    image_tensor = image_tensor.unsqueeze(0) # unsqueeze to add a batch dimension explaining that we're predicting only one image, not 8 like during training. so from [3, 256, 256] to [1, 3, 256, 256]

    image_tensor = image_tensor.to(DEVICE)

    with torch.no_grad(): # don't calculate gradients

        outputs = model(image_tensor) # images enters model and prediction is made, three scores, one for each class

        probabilities = torch.softmax(outputs, dim=1) # converts those scores into values that behave like probabilities

        predicted_class = torch.argmax( # which class has the highest probability? 0, 1, 2 for each class respectively
            probabilities,
            dim=1
        ).item()

        confidence = probabilities[0][predicted_class].item() # gets the probability corresponding to the class the model selected

        class_names = [
            "real",
            "synthetic",
            "swapped"
        ]

        prediction = class_names[predicted_class]

    return {
    "prediction": prediction,
    "confidence": confidence
    }

if __name__ == "__main__": # if we're running this file directly, start Flask server
    app.run(debug=True)