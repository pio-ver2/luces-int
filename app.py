import streamlit as st
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import threading

# =========================
# MQTT SETTINGS
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "phio/lights"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Global flag to STOP auto mode
stop_auto = False


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
    img = cv2.resize(frame, (80, 80))
    avg_color = img.mean(axis=0).mean(axis=0)
    b, g, r = avg_color
    return int(r), int(g), int(b)


# =========================
# AUTO MODE VIDEO LOOP
# =========================
def run_auto_mode(video_bytes, frame_placeholder, color_placeholder, message_box):
    global stop_auto
    stop_auto = False

    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture("temp_video.mp4")

    message_box.info("Procesando video... presiona un Mood para detener Auto Mode")

    while cap.isOpened() and not stop_auto:
        ret, frame = cap.read()
        if not ret:
            message_box.success("Video terminado ✔")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        r, g, b = get_dominant_color(frame)
        send_rgb(r, g, b)

        frame_placeholder.image(frame, caption=f"Frame actual • RGB = {r}, {g}, {b}")
        color_placeholder.markdown(
            f"<div style='width:100%;height:50px;background:rgb({r},{g},{b});border-radius:8px;'></div>",
            unsafe_allow_html=True
        )

        time.sleep(0.04)

    cap.release()


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Luces", layout="centered")

st.title("✨ Luces — Control de Ambiente ✨")
st.write("### Modo Automático + Modo Manual (Moods)")

st.write("---")

# =========================
# AUTO MODE SECTION
# =========================

st.subheader("🎥 Modo Automático (Video → LEDs)")

video_file = st.file_uploader("Sube un video", type=["mp4", "mov", "avi"])

colA1, colA2 = st.columns(2)

auto_active = st.session_state.get("auto_active", False)

if colA1.button("▶ Activar Auto Mode"):
    if video_file is None:
        st.warning("Sube un video primero.")
    else:
        st.session_state.auto_active = True
        st.session_state.manual_active = False
        stop_auto = False  # reset flag

        frame_placeholder = st.empty()
        color_placeholder = st.empty()
        message_box = st.empty()

        # background thread so UI doesn’t freeze
        threading.Thread(
            target=run_auto_mode,
            args=(video_file.read(), frame_placeholder, color_placeholder, message_box),
            daemon=True
        ).start()

if colA2.button("⛔ Detener Auto Mode"):
    st.session_state.auto_active = False
    stop_auto = True
    st.info("Modo Automático detenido.")


st.write("---")

# =========================
# MANUAL MOODS SECTION
# =========================
st.subheader("🎭 Modo Manual (Moods)")

st.write("Selecciona un mood. Esto **detiene Auto Mode automáticamente**.")

col1, col2, col3 = st.columns(3)

# Each mood button stops auto mode AND sends palette
def mood_button(col, num, label):
    global stop_auto
    if col.button(label):
        stop_auto = True
        st.session_state.manual_active = True
        st.session_state.auto_active = False
        send_mood(num)
        st.success(f"Mood {num} activado ✨")


mood_button(col1, 1, "Mood 1 💗")
mood_button(col2, 2, "Mood 2 🔥")
mood_button(col3, 3, "Mood 3 🌊")

col4, col5, col6 = st.columns(3)
mood_button(col4, 4, "Mood 4 🌿")
mood_button(col5, 5, "Mood 5 🌞")
mood_button(col6, 6, "Mood 6 💜")
