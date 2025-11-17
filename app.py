import streamlit as st
from mqtt_control import send_color_rgb

st.set_page_config(page_title="Light Reactive Controller", layout="centered")

st.title("🎥💡 Light Reactive System")
st.write("Use this app to send RGB test colors to your ESP32 LED strip.")

st.markdown("---")
st.subheader("Manual Color Sender")

col1, col2 = st.columns([2, 1])

with col1:
    r = st.slider("Red (R)", 0, 255, 120)
    g = st.slider("Green (G)", 0, 255, 120)
    b = st.slider("Blue (B)", 0, 255, 120)

with col2:
    st.write("### Preview")
    st.markdown(
        f"<div style='width:100px;height:100px;border-radius:12px;background:rgb({r},{g},{b});'></div>",
        unsafe_allow_html=True
    )

if st.button("Send to LED Strip"):
    send_color_rgb(r, g, b)
    st.success(f"Sent RGB({r}, {g}, {b}) to your ESP32!")

st.markdown("---")
st.info("To sync color with your full screen, run **`screen_capture.py` locally** on your computer.")
