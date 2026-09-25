<div align="center">

# 🤟 Sign Language Detector (ML)

**Real-time American Sign Language (A–Z) recognition using computer vision and classical ML**

*MediaPipe hand tracking · Random Forest classifier · OpenCV live inference · Flask web UI*

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-00A98F?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20UI-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

</div>

---

## 📖 Overview

This project detects and classifies **hand-sign letters** from a live webcam feed. It uses **MediaPipe** to extract 21 hand landmarks per frame, normalizes them into a feature vector, and feeds that vector into a **Random Forest** classifier (scikit-learn) trained to recognize sign-language letters. A lightweight **Flask** app wraps the whole pipeline — image collection, dataset creation, training, and live inference — behind a simple browser UI, in addition to the standalone scripts.

The end-to-end pipeline has four stages, each its own script:

1. **Collect** — capture labeled hand images from your webcam
2. **Build dataset** — extract hand landmarks from those images with MediaPipe
3. **Train** — fit a Random Forest classifier on the landmark features
4. **Infer** — run the trained model live on webcam video, drawing a bounding box and predicted letter over the detected hand

---

## ✨ Features

- 🖐️ **Real-time hand landmark detection** via MediaPipe Hands
- 🌲 **Random Forest classifier** trained on normalized (x, y) landmark coordinates, evaluated with a held-out test split and accuracy score
- 🎥 **Live webcam inference** with an on-screen bounding box and predicted letter overlay (`inference_classifier.py`)
- 🧰 **Cross-platform camera handling** in `collect_imgs.py` — automatically tries multiple OpenCV backends (AVFoundation, V4L2, GStreamer, etc.) depending on OS, with troubleshooting hints if the camera fails to open
- 🌐 **Flask web app** (`app.py`) with pages for Home, Train, and Inference, and routes that kick off each pipeline stage as a subprocess
- 📦 **Pre-trained model included** (`model.p`) so you can run inference immediately without retraining
- 🔤 Ships pre-configured for the full alphabet mapping (**A–Z**) in the inference labels

---

## 🧱 Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3 |
| **Computer Vision** | OpenCV (`cv2`) |
| **Hand Tracking / Landmarks** | MediaPipe |
| **Machine Learning** | scikit-learn (`RandomForestClassifier`) |
| **Data Handling** | NumPy, Pickle |
| **Web Interface** | Flask, Bootstrap 5 |
| **Visualization** | Matplotlib |

---

## 📂 Project Structure

```
sign_language_detector-ML-/
├── app.py                    # Flask web app — orchestrates the pipeline via the browser
├── collect_imgs.py           # Stage 1: capture labeled hand images from webcam
├── create_dataset.py         # Stage 2: extract MediaPipe landmarks → data.pickle
├── train_classifier.py       # Stage 3: train Random Forest on data.pickle → model.p
├── inference_classifier.py   # Stage 4: real-time webcam inference using model.p
├── model.p                   # Pre-trained Random Forest model (included)
├── templates/
│   ├── index.html            # Landing page
│   ├── train.html            # Training dashboard page
│   └── inference.html        # Live inference page
└── LICENSE.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A working webcam
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Pratham-0105/sign_language_detector-ML-.git
cd sign_language_detector-ML-

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install opencv-python mediapipe scikit-learn numpy matplotlib flask
```

> This repo doesn't ship a `requirements.txt` yet — the command above installs everything imported across the scripts. Feel free to freeze it into one with `pip freeze > requirements.txt` once installed.

### Usage

**Option A — Run the scripts directly**

```bash
# Step 1: Collect training images (press "q" to start capturing each class, ESC to quit)
python collect_imgs.py

# Step 2: Build the landmark dataset from collected images
python create_dataset.py

# Step 3: Train the classifier
python train_classifier.py

# Step 4: Run live inference (press "q" to quit)
python inference_classifier.py
```

**Option B — Use the Flask web app**

```bash
python app.py
```

Then open **http://localhost:5001** in your browser to trigger data collection, dataset creation, training, and inference from the UI.

> A pre-trained `model.p` is already included, so you can skip straight to **Step 4 / the Inference page** if you just want to see it in action.

---

## 🧠 How It Works

1. **`collect_imgs.py`** opens the webcam and saves `dataset_size` images per class into `./data/<class_id>/`, trying several OpenCV camera backends automatically for cross-platform compatibility.
2. **`create_dataset.py`** runs MediaPipe Hands over every collected image, extracts the 21 hand landmarks, normalizes each point relative to the hand's bounding box (`x - min(x)`, `y - min(y)`), and serializes the resulting feature vectors and labels to `data.pickle`.
3. **`train_classifier.py`** loads `data.pickle`, splits it into train/test sets (80/20, stratified), fits a `RandomForestClassifier`, prints the test-set accuracy, and saves the trained model to `model.p`.
4. **`inference_classifier.py`** reopens the webcam, detects the hand landmarks per frame, feeds the same normalized feature vector into the loaded model, and overlays the predicted letter (mapped via `labels_dict`, A–Z) with a bounding box on the live video.

---

## 🗺️ Roadmap

- [ ] Add a `requirements.txt` / `pyproject.toml` for reproducible installs
- [ ] Support two-hand / dynamic gesture sequences, not just static single-hand signs
- [ ] Stream inference results into the Flask UI instead of a separate OpenCV window
- [ ] Add model evaluation artifacts (confusion matrix, per-class accuracy) to the repo
- [ ] Package a `requirements-lock` and Docker setup for easier environment reproduction

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE.md](LICENSE.md) file for details.

---

<div align="center">

Made with 🤟 using Python, OpenCV & MediaPipe

</div>
