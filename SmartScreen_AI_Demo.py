import streamlit as st
import pandas as pd
import plotly.express as px
import cv2
import numpy as np
import os
import time
from datetime import datetime
from ultralytics import YOLO

# --- Streamlit Page Config ---
st.set_page_config(page_title="SmartScreen AI", layout="centered")
st.title("🚀 SmartScreen AI – Real-Time Detection")

# --- Load YOLO model ---
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # tiny YOLO for speed
model = load_model()

# --- CSV Logger ---
CSV_FILE = "detections.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp", "object", "confidence"]).to_csv(CSV_FILE, index=False)

# --- Capture Frame Function ---
def capture_frame():
    cap = cv2.VideoCapture(0)  # webcam
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb
    else:
        return None

# --- AI Detection Function ---
def detect_objects(frame):
    results = model(frame)
    detections = results[0].boxes.data.cpu().numpy()

    if len(detections) > 0:
        # Highest confidence detection
        top = detections[np.argmax(detections[:, 4])]
        x1, y1, x2, y2, conf, cls_id = top
        detected_object = model.names[int(cls_id)]
        confidence = float(conf)
        return detected_object, confidence
    else:
        return "No Object", 0.0

# --- Main App Loop ---
placeholder = st.empty()
chart_placeholder = st.empty()

# Continuous update loop
for i in range(50):  # ~50 frames (~25 sec demo)
    frame = capture_frame()
    if frame is None:
        st.error("Webcam not found.")
        break

    obj, conf = detect_objects(frame)

    # --- Display detection ---
    with placeholder.container():
        st.image(frame, caption=f"Detected: {obj} ({conf:.2f})", use_column_width=True)

        # Sci-fi alert if > 95%
        if conf > 0.95 and obj != "No Object":
            st.markdown(
                f"<h2 style='color:lime; text-shadow: 0 0 20px lime;'>⚡ ALERT: {obj} detected ({conf:.2f}) ⚡</h2>",
                unsafe_allow_html=True,
            )
            st.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg")

    # --- Log to CSV ---
    new_row = pd.DataFrame([[datetime.now(), obj, conf]], columns=["timestamp", "object", "confidence"])
    new_row.to_csv(CSV_FILE, mode='a', header=False, index=False)

    # --- Update live confidence chart ---
    df = pd.read_csv(CSV_FILE)
    fig = px.line(df, x="timestamp", y="confidence", color="object", title="Detection Confidence Over Time")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(0.5)  # half-second refresh
