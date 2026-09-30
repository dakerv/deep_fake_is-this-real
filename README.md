# Deepfake Image Detection System

A three-class deepfake image detection system that uses **EfficientNet-B0 and transfer learning** to classify facial images as **Real, Face-Swapped, or Synthetic**.

The trained model is integrated into a web application built with **Flask, React, Vite, TypeScript, and Tailwind CSS**, allowing users to upload an image and receive a predicted category together with a confidence percentage.

---

## Overview

The increasing accessibility of generative artificial intelligence and face-manipulation technologies has made it increasingly difficult to distinguish authentic facial images from artificially generated or manipulated ones.

This project investigates the use of convolutional neural networks for automated facial-image classification. Rather than treating all manipulated images as a single category, the system performs **three-class classification**:

* **Real** — authentic facial images
* **Face-Swapped** — images in which a face has been replaced or manipulated using face-swapping techniques
* **Synthetic** — artificially generated facial images

The project consists of two main components:

1. **Machine Learning Model** — an EfficientNet-B0 classifier trained using transfer learning.
2. **Web Application** — a Flask backend and React-based frontend that provide access to the trained model.

The system is designed specifically for **still facial images** and is not intended to analyse video, audio, metadata, or other forms of digital media.

---

## Key Features

* Three-class deepfake image classification
* EfficientNet-B0 transfer-learning architecture
* Classification of:

  * Real images
  * Face-swapped images
  * Synthetic images
* Confidence percentage for each prediction
* Facial-content validation before classification
* Invalid image-file detection
* Flask-based inference backend
* React + Vite frontend
* TypeScript-based frontend implementation
* No user accounts required
* Images are processed for prediction without being stored by the application
* CPU-compatible inference

---

## Model

The detection model is based on **EfficientNet-B0**, a convolutional neural network architecture originally designed for efficient image classification.

Transfer learning was used to adapt the pretrained architecture to the project's three target classes.

The final classification layer was modified to produce three outputs:

```text
Real
Synthetic
Face-Swapped
```

### Training Configuration

| Parameter                | Configuration      |
| ------------------------ | ------------------ |
| Architecture             | EfficientNet-B0    |
| Learning approach        | Transfer learning  |
| Number of classes        | 3                  |
| Optimiser                | Adam               |
| Learning rate            | 0.0001             |
| Loss function            | Cross-Entropy Loss |
| Batch size               | 8                  |
| Training device          | CPU                |
| Best epoch               | 11                 |
| Best validation accuracy | 96.15%             |

---

## Dataset

The project uses three categories of facial images.

### Real

The real-image class was constructed from:

* **FFHQ real images**
* **Celeb-DF real images**

The sampled dataset allocated 3,000 images from each source, giving a target of 6,000 real images.

### Synthetic

The synthetic class uses the **StyleGAN3 Synthetic Face Image Dataset**, distributed through Kaggle.

The available source dataset contains approximately 29,999 images. A balanced subset was sampled for this project.

### Face-Swapped

The face-swapped class uses the dataset titled:

> **DeepFake(face swapped) images using FFHQ dataset**

The source dataset contains approximately 111,016 images, from which a balanced subset was sampled.

### Dataset Distribution

The sampled dataset was constructed with the following target distribution:

| Class        | Sampled Images |
| ------------ | -------------: |
| Real         |          6,000 |
| Synthetic    |          6,000 |
| Face-Swapped |          6,000 |
| **Total**    |     **18,000** |

The data was subsequently processed and divided into training, validation, and test sets.

---

## Preprocessing

Before training, the images were processed through a facial-image preprocessing pipeline.

The preprocessing stage includes:

1. Loading the source image
2. Detecting the face
3. Selecting the relevant facial region
4. Applying a margin around the detected face
5. Cropping the facial region
6. Resizing the resulting image to **224 × 224 pixels**
7. Organising the processed images into training, validation, and test directories

The dataset was divided using a:

* **70% training split**
* **15% validation split**
* **15% test split**

The final evaluation used **2,700 test images**, with 900 images representing each target class.

---

## Evaluation Results

The final model was selected based on validation performance.

**Best model: Epoch 11**

* Validation accuracy: **96.15%**
* Test accuracy: **97.44%**
* Correct test predictions: **2,631 / 2,700**

### Class-Specific Results

| Class        |   Correct | Recall | F1-Score |
| ------------ | --------: | -----: | -------: |
| Real         | 878 / 900 | 97.56% |   0.9622 |
| Synthetic    | 855 / 900 | 95.00% |   0.9623 |
| Face-Swapped | 898 / 900 | 99.78% |   0.9989 |

### Confusion Matrix

The confusion matrix below uses the class order **Real → Synthetic → Face-Swapped**:

| Actual / Predicted |    Real | Synthetic | Face-Swapped |
| ------------------ | ------: | --------: | -----------: |
| **Real**           | **878** |        22 |            0 |
| **Synthetic**      |      45 |   **855** |            0 |
| **Face-Swapped**   |       2 |         0 |      **898** |

The majority of classification errors occurred between the **real and synthetic** classes.

Of the 69 incorrect predictions:

* 22 real images were classified as synthetic.
* 45 synthetic images were classified as real.
* 2 face-swapped images were classified as real.

Therefore, **67 of the 69 errors involved real-synthetic confusion**.

---

## System Architecture

The application follows a frontend-backend-machine-learning architecture.

```text
┌──────────────────────┐
│       User           │
└──────────┬───────────┘
           │
           │ Upload Image
           ▼
┌──────────────────────┐
│   React Frontend     │
│   + Vite + TypeScript│
└──────────┬───────────┘
           │
           │ HTTP Request
           ▼
┌──────────────────────┐
│    Flask Backend     │
│                      │
│ • Input validation   │
│ • Face detection     │
│ • Image preprocessing│
└──────────┬───────────┘
           │
           │ Processed Image
           ▼
┌──────────────────────┐
│   EfficientNet-B0    │
│   PyTorch Model      │
└──────────┬───────────┘
           │
           │ Prediction
           ▼
┌──────────────────────┐
│   Flask Response     │
│                      │
│ • Class              │
│ • Confidence         │
│ • Probabilities      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   React Frontend     │
│                      │
│ Likely Real          │
│ Likely Swapped       │
│ Likely Synthetic     │
└──────────────────────┘
```

---

## Application Workflow

The complete prediction workflow is:

```text
Image Upload
     ↓
File Validation
     ↓
Face Detection
     ↓
Image Preprocessing
     ↓
224 × 224 Tensor
     ↓
EfficientNet-B0
     ↓
Softmax Probabilities
     ↓
Highest-Probability Class
     ↓
Prediction + Confidence
     ↓
Frontend Result
```

The application uses user-facing terminology such as:

* **Likely Real**
* **Likely Swapped**
* **Likely Synthetic**

The term **“likely”** is intentional. The model provides a probabilistic machine-learning prediction rather than absolute proof that an image is authentic or manipulated.

---

## Input Validation

The backend performs several checks before an image is passed to the model.

These include:

* Checking that an image was submitted
* Checking that a file was actually selected
* Verifying that the uploaded file can be opened as an image
* Checking for a detectable face

If no face is detected, the system returns an appropriate error instead of attempting to classify the image.

This is particularly important because the model was trained specifically for facial-image classification.

---

## Technologies Used

### Machine Learning

* **Python**
* **PyTorch**
* **Torchvision**
* **EfficientNet-B0**
* **MTCNN / OpenCV Haar Cascade** for facial detection during preprocessing and application input validation
* **Pillow**
* **NumPy**

### Backend

* **Flask**
* Python

### Frontend

* **React**
* **Vite**
* **TypeScript**
* **Tailwind CSS**

### Development Environment

The system was developed and tested on:

* **CPU:** Intel Core i5-8265U
* **RAM:** 8 GB
* **GPU:** Intel UHD Graphics 620
* **Operating System:** Windows
* **Node.js:** v24.11.0
* **npm:** v11.10.0

Training was performed on the CPU without a dedicated GPU.

---

## Project Structure

The repository is organised approximately as follows:

```text
deep_fake_is-this-real/
│
├── models/
│   └── ...
│
├── models (experiment two)/
│   ├── efficientnet_b0.pth
│   └── ...
│
├── raw_data/
│   ├── real/
│   ├── synthetic/
│   └── swapped/
│
├── cropped_faces/
│   ├── real/
│   ├── synthetic/
│   └── swapped/
│
├── dataset/
│   ├── train/
│   │   ├── real/
│   │   ├── synthetic/
│   │   └── swapped/
│   ├── val/
│   │   ├── real/
│   │   ├── synthetic/
│   │   └── swapped/
│   └── test/
│       ├── real/
│       ├── synthetic/
│       └── swapped/
│
├── src/
│   ├── ...
│   ├── dataset_loader.py
│   ├── test_model2.py
│   └── ...
│
├── frontend/
│   └── ...
│
├── requirements.txt
├── package.json
└── README.md
```

> **Note:** Dataset images and model checkpoints may be excluded from the public repository depending on repository size, licensing, and dataset redistribution restrictions.

---

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd deep_fake_is-this-real
```

### 2. Create a Python Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policies prevent activation, the environment can also be activated through Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If the requirements file does not contain all application dependencies, install the required packages manually:

```bash
pip install torch torchvision flask pillow numpy opencv-python
```

---

## Running the Backend

Navigate to the backend directory if required by the repository structure and activate the Python virtual environment.

Then run:

```bash
python app.py
```

The Flask server should start locally.

The backend is configured to load the Experiment Two EfficientNet-B0 checkpoint:

```text
models (experiment two)/efficientnet_b0.pth
```

The prediction endpoint is:

```text
POST /predict
```

---

## Running the Frontend

Open a separate terminal and navigate to the frontend directory.

Install the frontend dependencies:

```bash
npm install
```

Then start the development server:

```bash
npm run dev
```

Vite will provide a local development URL in the terminal.

Open that address in a web browser to access the application.

---

## Making a Prediction

Once both the backend and frontend are running:

1. Open the web application.
2. Select an image containing a visible face.
3. Submit the image for analysis.
4. The frontend sends the image to the Flask backend.
5. The backend validates the image.
6. The image is passed through the trained EfficientNet-B0 model.
7. The predicted class and confidence are returned.
8. The frontend displays the result.

Example result categories:

```text
Likely Real
Confidence: 97.4%
```

or:

```text
Likely Synthetic
Confidence: 91.8%
```

The displayed confidence is model output and should not be interpreted as absolute certainty.

---

## Model Output

The backend returns a response containing the predicted class, confidence, and class probabilities.

Conceptually, the response follows this structure:

```json
{
  "prediction": "real",
  "confidence": 0.974,
  "probabilities": {
    "real": 0.974,
    "synthetic": 0.018,
    "swapped": 0.008
  }
}
```

The exact values depend on the submitted image.

---

## Training

The training pipeline uses:

```text
Dataset
   ↓
Face Detection / Cropping
   ↓
224 × 224 Images
   ↓
Train / Validation / Test Split
   ↓
EfficientNet-B0
   ↓
Transfer Learning
   ↓
Cross-Entropy Loss
   ↓
Adam Optimiser
   ↓
Validation Evaluation
   ↓
Best Model Checkpoint
```

The final experiment used:

```text
Batch size:       8
Learning rate:    0.0001
Optimiser:        Adam
Loss:             Cross-Entropy Loss
Epochs:           12
Device:           CPU
Best epoch:       11
```

The training configuration was constrained partly by the available 8 GB RAM system.

---

## Evaluation

The final model can be evaluated using the project's test script.

From the project root:

```powershell
python src\test_model2.py
```

The evaluation script loads:

```text
dataset/test/
```

and the Experiment Two model:

```text
models (experiment two)/efficientnet_b0.pth
```

It reports:

* Number of test images
* Model checkpoint information
* Test accuracy
* Confusion matrix
* Classification report
* Precision
* Recall
* F1-score

---

## Limitations

The current system has several limitations.

### Dataset Generalisation

The model learns from the visual characteristics represented in its training datasets. Its performance may therefore differ when presented with images generated or manipulated using techniques that are not represented in the training data.

### Synthetic Image Diversity

The synthetic category is primarily represented by StyleGAN3-generated images. Other generative architectures may produce different visual characteristics.

### Face-Swapping Diversity

The face-swapped category is based on a particular face-swapping dataset. More advanced or visually subtle face-swapping techniques may present different challenges.

### Image-Only Detection

The system analyses still images and does not currently perform video or audio deepfake detection.

### Computational Resources

Training was performed using CPU-based hardware with 8 GB of RAM and no dedicated GPU. This limited the practical size and complexity of some experiments.

### Confidence Interpretation

The confidence value represents the model's predicted probability distribution and should not be interpreted as definitive proof of authenticity.

---

## Future Development

Possible future improvements include:

* Expanding the training dataset
* Incorporating multiple synthetic-image generation methods
* Incorporating additional face-swapping techniques
* Improving real-versus-synthetic classification
* Evaluating additional neural network architectures
* Performing cross-dataset evaluation
* Training with GPU acceleration
* Improving facial detection and localisation
* Supporting multiple faces within a single image
* Extending the system to video deepfake detection
* Investigating multimodal detection involving audio and video
* Adding model explainability techniques
* Improving confidence calibration
* Evaluating the model against previously unseen generation and manipulation methods

---

## Academic Context

This project was developed as a **final-year Information Technology project at the University of Ghana, Legon**.

The project investigates the application of convolutional neural networks and transfer learning to the problem of automated deepfake image classification.

### Project Title

**Deepfake Image Detection Using Convolutional Neural Networks and Generation Pattern Analysis**

---

## Important Note on Results

The reported **97.44% test accuracy** represents the performance of the final Experiment Two model on the project's designated test set of 2,700 images.

It should not be interpreted as a universal measure of deepfake detection accuracy across all existing datasets, generation techniques, image qualities, or manipulation methods.

The model's performance is dependent on the data distributions, preprocessing procedures, architecture, and experimental conditions used in this project.

---

## License

This project is intended primarily for **academic and educational purposes**.

The source code may be used for learning and research subject to the terms of the repository license.

The datasets used by this project may have their own licensing and usage restrictions. Users should obtain the datasets directly from their respective sources and comply with their applicable terms rather than redistributing the datasets through this repository.

---

## Acknowledgements

This project makes use of publicly available datasets and open-source machine-learning and software-development technologies.

Special acknowledgement is given to the creators and distributors of the datasets used for the real, synthetic, and face-swapped image categories, as well as the developers of PyTorch, Torchvision, EfficientNet, Flask, React, Vite, and the other open-source technologies used to implement the system.

---

## Author

**Vanessa Elinam Daker**

University of Ghana, Legon
Department of Computer Science

---

## Project Status

**Completed academic prototype**

The current version represents the final evaluated implementation developed for the project. Further development may improve dataset diversity, generalisation, model explainability, and support for additional forms of manipulated media.
