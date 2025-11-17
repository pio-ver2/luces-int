# ✨ Luces — LED Strip Controller with Video & Mood Modes

This project controls an ESP32-based LED strip in **two modes**:

## 🎥 1. Modo Automático (Video → LEDs)
- Upload a video file (.mp4, .mov, .avi)
- The app reads each frame
- Detects the **dominant RGB color**
- Sends that color to the ESP32 via MQTT
- The LED strip updates in real time

Perfect for ambience, mood lighting, or reactive visual effects.

---

## 🎭 2. Modo Manual (Moods)
Choose between **6 predefined moods** (romantic, horror, chill, etc.).

Each mood triggers:
- A custom LED palette (multiple alternating colors)
- A custom LED pattern defined in the ESP32 code

Manual mode **instantly overrides** Automatic mode.

---

## 🧠 How It Works

### Streamlit App (`app.py`)
- Handles video upload
- Extracts colors with OpenCV
- Sends RGB or mood messages to MQTT
- Provides Interactive UI for Auto / Manual modes

### ESP32 Firmware
Receives MQTT messages from the app:
- If the JSON contains `"r","g","b"` → **Auto mode** (solid color)
- If it contains `"mode":"manual"` and `"mood":X` → **Manual palette**

LED strip is controlled using the Adafruit NeoPixel library.

---

## 🔌 Hardware Setup (Wokwi or Real ESP32)

### ESP32 Pins
- Data to LED strip → **GPIO 5**
- VCC → **5V**
- GND → **GND**

### Wokwi Diagram Requirements
Your `diagram.json` must include:

