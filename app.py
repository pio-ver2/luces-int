import streamlit as st
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# =========================
# MQTT SETTINGS
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "phio/lights"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)


# =========================
# SEND COLOR (AUTO MODE)
# =========================
def send_rgb(r, g, b):
    payload = {
        "r": int(r),
        "g": int(g),
        "b": int(b)
    }
    client.publish(MQTT_TOPIC, str(payload).replace("'", '"'))


# =========================
# SEND MOOD (MANUAL MODE)
# =========================
def send_mood(mood_number):
    payload = {
        "mode": "manual",
        "mood": int(mood_number)
    }
    client.publish(MQTT_TOPIC, str(payload).replace("'", '"'))


# =========================
# COLOR FROM FRAME
# =========================
def get_dominant_color(frame):
    img = cv2.resize(frame, (100, 100))
    avg_color = img.mean(axis=0).mean(axis=0)
    b, g, r = avg_color
    return int(r), int(g), int(b)


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Luces", layout="centered")

st.title("✨ Luces — Control de Ambiente con Video o Moods ✨")

mode = st.radio(
    "Selecciona un modo:",
    ["Automático", "Manual"],
    horizontal=True
)

st.write("---")

# ======================================================
# AUTO MODE
# ======================================================
if mode == "Automático":
    st.subheader("🎥 Modo Automático (Video → Colores de LEDs)")

    video_file = st.file_uploader("Sube un video", type=["mp4", "mov", "avi"])

    if video_file is not None:
        st.video(video_file)

        if st.button("▶ Comenzar lectura de colores"):
            st.info("Procesando video…")

            # Convert uploaded file to OpenCV
            bytes_data = video_file.read()
            with open("temp_video.mp4", "wb") as f:
                f.write(bytes_data)

            cap = cv2.VideoCapture("temp_video.mp4")

            frame_placeholder = st.empty()
            color_placeholder = st.empty()

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.success("Video terminado ✔")
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                r, g, b = get_dominant_color(frame)
                send_rgb(r, g, b)

                frame_placeholder.image(frame, caption=f"Frame actual • RGB = {r}, {g}, {b}")
                color_placeholder.markdown(
                    f"<div style='width:100%;height:50px;background:rgb({r},{g},{b});'></div>",
                    unsafe_allow_html=True
                )

                time.sleep(0.05)

            cap.release()


# ======================================================
# MANUAL MODE
# ======================================================
if mode == "Manual":
    st.subheader("🎭 Modo Manual (Moods)")

    st.write("Selecciona un mood para las luces:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Mood 1 💗"):
            send_mood(1)
            st.success("Mood 1 enviado!")

    with col2:
        if st.button("Mood 2 🔥"):
            send_mood(2)
            st.success("Mood 2 enviado!")

    with col3:
        if st.button("Mood 3 🌊"):
            send_mood(3)
            st.success("Mood 3 enviado!")

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("Mood 4 🌿"):
            send_mood(4)
            st.success("Mood 4 enviado!")

    with col5:
        if st.button("Mood 5 🌞"):
            send_mood(5)
            st.success("Mood 5 enviado!")

    with col6:
        if st.button("Mood 6 💜"):
            send_mood(6)
            st.success("Mood 6 enviado!")
