# 🧊 HoloCube – 3D Hologram Cube Controlled by Hand Gestures

This project lets you control a 3D **hologram-like cube** using only your **hand gestures** through your **webcam**. It combines real-time hand tracking with 3D graphics to create an immersive virtual interaction experience — just like controlling a hologram in sci-fi movies.

---

## 🚀 Demo

(https://www.linkedin.com/posts/dharma-prabhas-518b09320_python-opencv-computervision-activity-7295797574358245376-x2PJ?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFFSg6QBNtEY68jOUXc53FQ4tXitIGPLI_U)

---

## ✋ What It Does

- Detects your **hand and fingers** using your webcam
- Tracks hand **movements and gestures**
- Rotates a **3D cube** in real time using your hand’s position and orientation
- Gives a **hologram-like feel** with glowing edges and motion

---

## 🧠 How It Works (Beginner Friendly)

1. **Webcam** captures your live video.
2. **MediaPipe** (an AI toolkit by Google) detects your hand.
3. It looks at the **wrist**, **thumb tip**, and **index finger tip**.
4. These positions are used to calculate how much to rotate the cube:
   - Move hand up/down → Rotate on X-axis
   - Move hand left/right → Rotate on Y-axis
   - Pinch your thumb and index → Rotate on Z-axis
5. **OpenGL** draws and updates the cube based on your hand!

---

## 🛠️ Technologies Used

| Tool         | Purpose                          |
|--------------|----------------------------------|
| Python       | Programming language             |
| OpenCV       | Webcam and image processing      |
| MediaPipe    | AI-powered hand tracking         |
| PyOpenGL     | 3D rendering with OpenGL         |
| Pygame       | Creating display window & events |
| NumPy        | Math calculations                |

---

## 📦 Installation

### ✅ Prerequisites

Make sure you have **Python 3.7+** installed. Then, run this command to install all dependencies:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate opencv-python mediapipe numpy

