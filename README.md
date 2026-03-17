# Lane-Detection-System
# 🚗 Lane Detection System using OpenCV

## 📌 Overview

This project implements a **real-time lane detection system** using classical computer vision techniques in Python and OpenCV.
It processes video input to detect road lane markings and overlays them on the original frames.

The system is designed as a **foundational ADAS (Advanced Driver Assistance System)** module.

---

## 🎯 Features

* Real-time lane detection from video
* Adaptive edge detection (Canny)
* Dynamic Region of Interest (ROI)
* Lane line averaging and smoothing
* Noise filtering using slope thresholds
* Works on different resolutions
* Handles slight curves and varying lighting conditions

---

## 🛠️ Tech Stack

* Python
* OpenCV (cv2)
* NumPy

---

## ⚙️ How It Works

### 1. Frame Preprocessing

* Convert image to grayscale
* Apply histogram equalization (for better contrast)
* Apply Gaussian blur

### 2. Edge Detection

* Use **Canny Edge Detection** with adaptive thresholds

### 3. Region of Interest (ROI)

* Focus only on road region using a polygon mask

### 4. Line Detection

* Detect line segments using **Hough Transform**

### 5. Lane Estimation

* Separate left and right lanes based on slope
* Average lines using linear regression
* Smooth results using previous frame data

### 6. Overlay

* Draw detected lanes on original frame

---

## ▶️ Usage

### 1. Install dependencies

```bash
pip install opencv-python numpy
```

### 2. Run the script

```bash
python lane_detection.py
```

### 3. Input video

Replace video path in code:

```python
cap = cv2.VideoCapture("test2.mp4")
```

---

## 📂 Project Structure

```
lane-detection/
│
├── lane_detection.py
├── nD_11.mp4
└── README.md
```

---

## 📈 Output

* Displays processed video with detected lane lines
* Press **'q'** to exit the video window

---

## ⚠️ Limitations

* Assumes lanes are approximately straight
* Struggles with:

  * Sharp curves
  * Night/rain conditions
  * Poor or missing lane markings
* Not suitable for complex urban environments

---

## 🚀 Future Improvements

* Bird’s Eye View transformation
* Curved lane detection (polynomial fitting)
* Deep learning-based lane detection (YOLO / LaneNet)
* Steering angle prediction
* Integration with real-time camera feed

---

## 🎓 Learning Outcomes

* Image processing fundamentals
* Edge detection and feature extraction
* Hough Transform
* Real-time video processing
* Basics of ADAS systems

---

## 📌 Applications

* Autonomous driving systems
* Driver assistance systems (ADAS)
* Road analysis and monitoring

---

## 👨‍💻 Author

Rachit Goyal
B.Tech CSE

---

## ⭐ Acknowledgment

This project is built for educational purposes and demonstrates fundamental computer vision techniques for lane detection.

---
