import streamlit as st
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import tempfile

# =========================
# MQTT SETTINGS
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "phio/lights"

# MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)


# =========================
# SEND COLOR TO MQTT
# =========================
def send_color(r, g, b):
    payload = {"r": int(r), "g": int(g), "b": int(b)}
    mqtt_client.publish(MQTT_TOPIC, str(payload))


# =========================
# COLOR EXTRACTION (AUTO MODE)
# =========================
def dominant_color(frame):
    frame_small = cv2.resize(frame, (64, 64))
    data = frame_small.reshape((-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    k = 1
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    r, g, b = centers[0]
    return int(r), int(g), int(b)


# =========================
# MANUAL MOOD PRESETS
# =========================
mood_presets = {
    "Romantic": [
        (255, 0, 80),
        (255, 120, 160),
        (255, 200, 220),
        (180, 0, 50),
        (255, 40, 120),
    ],
    "Scary": [
        (5, 0, 0),
        (50, 0, 0),
        (20, 0, 0),
        (80, 10, 10),
        (150, 0, 0),
    ],
    "Happy": [
        (255, 220, 0),
        (255, 120, 0),
        (255, 255, 80),
        (255, 180, 40),
        (255, 240, 120),
    ],
    "Chill": [
        (0, 80, 180),
        (0, 120, 255),
        (80, 200, 255),
        (40, 140, 200),
        (0, 60, 140),
    ],
    "Party": [
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 0),
        (0, 255, 100),
        (255, 100, 0),
    ],
    "Warm Cozy": [
        (255, 120, 60),
        (200, 80, 40),
        (255, 160, 100),
        (180, 60, 20),
        (255, 200, 140),
    ],
}


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Luces INT", layout="wide")

st.title("🌈 Luces-INT – Control Your ESP32 Lights")

mode = st.radio("Choose Mode:", ["Automatic", "Manual"], horizontal=True)

st.markdown("---")

# =============== AUTO MODE ===============
if mode == "Automatic":
    st.subheader("🎥 Upload Video for Auto Color Detection")

    video_file = st.file_uploader("Upload MP4 video", type=["mp4"])

    if video_file is not None:
        st.video(video_file)  # video player

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_file.write(video_file.read())
        tmp_path = tmp_file.name

        if st.button("Start Auto Lighting"):
            st.warning("Processing… keep Wokwi simulation open!", icon="⚡")

            cap = cv2.VideoCapture(tmp_path)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert BGR → RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                r, g, b = dominant_color(frame)
                send_color(r, g, b)

            cap.release()
            st.success("Video finished! Lights updated 🎉")

# =============== MANUAL MODE ===============
else:
    st.subheader("🎨 Pick a Mood")

    chosen = st.selectbox("Mood:", list(mood_presets.keys()))

    colors = mood_presets[chosen]
    st.write(f"Palette ({chosen}):", colors)

    if st.button("Apply Mood"):
        st.info("Sending mood to LED strip…", icon="✨")

        # Alternate colors along LED strip
        for i, (r, g, b) in enumerate(colors):
            send_color(r, g, b)

        st.success("Mood applied 💡✨")

