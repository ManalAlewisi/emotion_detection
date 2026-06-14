# 😊 Emotion Detection System

A real-time facial emotion detection system built with Python, OpenCV, and DeepFace.

## 📸 Demo

| Image 1 | Image 2 | Image 3 |
|---------|---------|---------|
| ![](https://github.com/ManalAlewisi/emotion_detection/blob/main/result1.jpg) | ![](https://github.com/ManalAlewisi/emotion_detection/blob/main/result2.jpg) | ![](https://github.com/ManalAlewisi/emotion_detection/blob/main/result3.jpg) |

## 🔍 Features

- Detect emotions from static images
- Real-time emotion detection via camera
- Visual emotion bars displayed next to the face
- Automatically saves result image
- Supports 7 emotions: Happy, Sad, Angry, Fear, Disgust, Surprise, Neutral

## 🛠️ Requirements

- Python 3.8+
- OpenCV
- DeepFace
- TensorFlow
- tf-keras
- NumPy < 2

## ⚙️ Installation

```bash
pip install deepface opencv-python tf-keras
pip install "numpy<2"
```

## 🚀 Usage

```bash
python emotion_detector.py
```

Then choose:
- **1** → Analyze an image (enter image path, type `q` to quit)
- **2** → Real-time camera detection (press `q` to quit, `s` to save screenshot)

## 📁 Project Structure
```
emotion_detection/
│
├── emotion_detector.py   # Main script
├── README.md             # Project documentation
└── results/
  ├── result1.jpg       # Demo result 1
  ├── result2.jpg       # Demo result 2
  └── result3.jpg       # Demo result 3
```
## 🧠 Model

This project uses [DeepFace](https://github.com/serengil/deepface) library which uses a lightweight CNN trained on FER-2013 dataset for emotion recognition.

## 📌 Notes

- For best results, use clear front-facing images
- Camera support depends on available hardware
- If you get a NumPy error, run: `pip install "numpy<2"`
