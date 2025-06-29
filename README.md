# SmartMedia-Gest 🎛️🖐️

SmartMedia-Gest is a gesture-controlled media assistant built using Python, OpenCV, and MediaPipe. It allows users to control system **volume**, **screen brightness**, and **media playback** (play/pause/next) using simple hand gestures captured via webcam.

---

## ✨ Features

- ✋ **Hand Gesture Recognition** using MediaPipe
- 🔊 **Volume Control** using finger distance (index + thumb)
- 💡 **Brightness Control** using palm gestures (Windows only)
- ⏯️ **Media Playback Controls**:
  - 👍 **Thumb + Index** → Play/Pause
  - ✌️ **Thumb + Middle** → Next Short
  - 🤟 **Thumb + Ring** → Previous Short
- 🎥 Real-time webcam processing
- 🖥️ Lightweight and easy to use

---

## 🖐️ Gesture Mappings

| Gesture | Action           |
|--------|------------------|
| 👍 Thumb + Index | Play / Pause       |
| ✌️ Thumb + Middle | Next Short        |
| 🤟 Thumb + Ring   | Previous Short    |
| ✋ Palm             | Brightness Control (optional) |
| ✌️ Index + Thumb Distance | Volume Control |

---



## 🚀 Getting Started

### 🔁 Clone the Repository

```bash
git clone https://github.com/Ayushi22-coder/SmartMedia-Gest.git
cd SmartMedia-Gest

Create a Virtual Environment (Recommended)
python -m venv venv
Activate the environment:
Windows:
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Run the Application
trail.py

 Dependencies
1.opencv-python – Webcam and image processing

2.mediapipe – Hand tracking and landmark detection

3.numpy – Numerical operations

4.keyboard – Simulating key presses

5.pycaw – Controlling system volume (Windows)

6.screen-brightness-control – Brightness adjustment (Windows)

