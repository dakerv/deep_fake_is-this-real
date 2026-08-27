from flask import Flask, request

app = Flask(__name__) # creates flask application

@app.route("/") # Initial route named '/' sends GET request
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

    print(f"Received image: {image.filename}")

    return {
        "message": "Image received successfully!",
        "filename": image.filename 
    }

if __name__ == "__main__": # if we're running this file directly, start Flask server
    app.run(debug=True)