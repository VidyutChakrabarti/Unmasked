import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import dlib
import tempfile
import os
from tensorflow.keras.applications.inception_v3 import preprocess_input


# Custom CSS for styling
st.markdown("""
<style>
.prediction {
    font-size: 24px !important;
    font-weight: bold !important;
    text-align: center !important;
    padding: 10px !important;
    border-radius: 5px !important;
    margin-top: 20px !important;
}
.real {
    color: green !important;
    border: 2px solid green !important;
}
.fake {
    color: red !important;
    border: 2px solid red !important;
}
.gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}
.gallery img {
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

def load_model():
    model_path = 'deepfake_detection_model.h5'
    return tf.keras.models.load_model(model_path)

model = load_model()

# Constants
IMG_SIZE = (299, 299)
MOTION_THRESHOLD = 20
FRAME_SKIP = 2
MAX_FRAMES = 10
no_of_frames = MAX_FRAMES
detector = dlib.get_frontal_face_detector()

# Function to extract faces from a frame
def extract_faces_from_frame(frame, detector):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_frame)
    resized_faces = []
    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        crop_img = frame[y1:y2, x1:x2]
        if crop_img.size != 0:
            resized_face = cv2.resize(crop_img, IMG_SIZE)
            resized_faces.append(resized_face)
    return resized_faces

# Function to process video frames
def process_frame(video_path, detector, frame_skip):
    prev_frame = None
    frame_count = 0
    motion_frames = []
    all_faces = []
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue
        faces = extract_faces_from_frame(frame, detector)
        all_faces.extend(faces)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is None:
            prev_frame = gray_frame
            frame_count += 1
            continue
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        motion_score = np.sum(frame_diff)
        if motion_score > MOTION_THRESHOLD and faces:
            motion_frames.extend(faces)
        prev_frame = gray_frame
        frame_count += 1
    cap.release()
    return motion_frames, all_faces

# Function to select well-distributed frames
def select_well_distributed_frames(motion_frames, all_faces, no_of_frames):
    if len(motion_frames) >= no_of_frames:
        interval = len(motion_frames) // no_of_frames
        return [motion_frames[i * interval] for i in range(no_of_frames)]
    needed_frames = no_of_frames - len(motion_frames)
    if len(motion_frames) + len(all_faces) < no_of_frames:
        return motion_frames + all_faces
    interval = max(1, len(all_faces) // needed_frames)
    additional_faces = [all_faces[i * interval] for i in range(needed_frames)]
    combined_frames = motion_frames + additional_faces
    interval = max(1, len(combined_frames) // no_of_frames)
    return [combined_frames[i * interval] for i in range(no_of_frames)]

# Function to extract frames
def extract_frames(no_of_frames, video_path):
    motion_frames, all_faces = process_frame(video_path, detector, FRAME_SKIP)
    return select_well_distributed_frames(motion_frames, all_faces, no_of_frames)

# Function to predict video
def predict_video(model, video_path):
    frames = extract_frames(no_of_frames, video_path)
    original_frames = frames
    if len(frames) < MAX_FRAMES:
        while len(frames) < MAX_FRAMES:
            frames.append(np.zeros((299, 299, 3), dtype=np.float32))
    frames = frames[:MAX_FRAMES]
    frames = np.array(frames)
    frames = preprocess_input(frames)
    input_data = np.expand_dims(frames, axis=0)
    prediction = model.predict(input_data)
    probability = prediction[0][0]
    if probability >= 0.6:
        predicted_label = 'FAKE'
    else:
        predicted_label = 'REAL'
        probability = 1 - probability
    return original_frames, predicted_label, probability

# Apply custom title style
st.markdown('<h1 class="title">Deepfake Detection</h1>', unsafe_allow_html=True)

# Create layout
left_column, right_column = st.columns(2)

# Left column - File uploader and submission form
with left_column:
    st.markdown("Upload a video to determine if it is REAL or FAKE based on the deepfake detection model.")
    with st.form(key = "video_form"):
        st.header("Upload Video")
        uploaded_file = st.file_uploader("Upload Video", type=["mp4"], label_visibility="hidden")
        if uploaded_file is not None:
            st.video(uploaded_file)
        submit = st.form_submit_button("Analyze Video", use_container_width=True)

# Process uploaded file
if uploaded_file is not None and submit:
    # File validation
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        st.error("File size exceeds 10 MB limit!")
        st.stop()
    if not uploaded_file.name.endswith('.mp4'):
        st.error("Only .mp4 files are allowed!")
        st.stop()

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file_path = temp_file.name
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

    # Process video
    with st.spinner('Analyzing video...'):
        frames, predicted_label, confidence = predict_video(model, temp_file_path)
        os.remove(temp_file_path)

    # Right column - Display results
with right_column:
    if uploaded_file is None or not submit:
        st.subheader("Extracted Frames")
        with st.container(border=True):
            cols = st.columns(2)
            for i in range(4):
                    with cols[i % 2]:
                        st.image("placeholder_image.png", use_column_width=True)
            
    else: 
        st.subheader("Extracted Frames")
        with st.container(border=True):
            st.markdown('<div class="gallery">', unsafe_allow_html=True)
            cols = st.columns(4)
            for idx, frame in enumerate(frames):
                with cols[idx % 4]:
                    st.image(frame, channels="BGR", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Display prediction and confidence
            st.subheader("Results")
            # Define CSS for styling
            st.markdown("""
                <style>
                    .prediction-box {
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        padding: 10px;
                        border-radius: 10px;
                        color: white;
                        margin-top: 10px;
                    }
                    .real {
                        background-color: #4CAF50;
                    }
                    .fake {
                        background-color: #E74C3C;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Prediction display with formatted styling
            prediction_class = "real" if predicted_label == "REAL" else "fake"
            st.markdown(f"""
                <div class="prediction-box {prediction_class}">
                    {predicted_label}
                </div>
            """, unsafe_allow_html=True)
