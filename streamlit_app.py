import streamlit as st
import os
import tempfile
from pathlib import Path
import numpy as np
import requests
import tensorflow as tf

from utils.model import predict_image
from utils.image_processing import preprocess_image, load_image_from_url, load_uploaded_image
from utils.video_processing import process_video_frames
from data.class_info import CLASS_INFO, EXPECTED_CLASS_NAMES
from ui.components import (
    setup_page, display_sidebar, display_model_info, 
    display_prediction, display_probability_details, display_video_results
)

APP_DIR = Path(__file__).parent
MODEL_PATH = APP_DIR / "saved_models" / "model.keras"
TARGET_SIZE = (299, 299)

def main():
    setup_page()
    
    input_method, confidence_threshold, frame_interval_secs = display_sidebar(frame_interval_option=True)
    
    st.title("♻️ Smart Garbage Classifier")
    st.markdown("Upload an image, provide a URL, or upload a video to classify common garbage items.")
    st.markdown("---")
    
    # model = load_keras_model(MODEL_PATH)

    from utils.model import download_and_load_keras_model, predict_image, MODEL_DOWNLOAD_URL, CACHE_DIR, LOCAL_MODEL_FILENAME

    model = download_and_load_keras_model(MODEL_DOWNLOAD_URL, CACHE_DIR, LOCAL_MODEL_FILENAME)

    display_model_info(MODEL_PATH, TARGET_SIZE, EXPECTED_CLASS_NAMES, CLASS_INFO)
    
    if not model:
        st.error("Model loading failed. Cannot proceed. Please check model path and logs.")
        return
    
    if input_method in ["Upload Image", "Image URL"]:
        handle_image_input(input_method, model, confidence_threshold)
    elif input_method == "Upload Video":
        handle_video_input(model, confidence_threshold, frame_interval_secs)
    
    st.markdown("---")
    st.markdown("Built with Streamlit, TensorFlow/Keras, and OpenCV.")

def handle_image_input(input_method, model, confidence_threshold):
    img_pil = None
    
    if input_method == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"], key="file_uploader")
        if uploaded_file:
            img_pil = load_uploaded_image(uploaded_file)
    else:  # Image URL
        image_url = st.text_input("Enter Image URL:", key="url_input")
        if image_url:
            with st.spinner('Fetching image from URL...'):
                img_pil = load_image_from_url(image_url)
    
    if img_pil:
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.subheader("🖼️ Input Image")
            st.image(img_pil, caption='Input Image', use_column_width=True)
        with col2:
            with st.spinner('🧠 Classifying Image...'):
                img_batch = preprocess_image(img_pil, TARGET_SIZE)
                if img_batch is not None:
                    _, _, prediction_probs = predict_image(
                        model, img_batch, EXPECTED_CLASS_NAMES, confidence_threshold
                    )
                    if prediction_probs is not None:
                        display_prediction(
                            prediction_probs, CLASS_INFO, EXPECTED_CLASS_NAMES, confidence_threshold
                        )
                        display_probability_details(prediction_probs, EXPECTED_CLASS_NAMES, CLASS_INFO)
                    else:
                        st.error("Prediction failed.")
                else:
                    st.error("Image preprocessing failed.")
    elif input_method == "Upload Image" and st.session_state.get("file_uploader") is None:
        st.info("☝️ Upload an image file.")
    elif input_method == "Image URL" and not st.session_state.get("url_input"):
        st.info("☝️ Enter an image URL.")

def handle_video_input(model, confidence_threshold, frame_interval_secs):
    uploaded_video_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv"],
        key="video_uploader"
    )
    
    if uploaded_video_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_video_file.name.split('.')[-1]) as tfile:
            tfile.write(uploaded_video_file.read())
            temp_video_path = tfile.name
        
        st.subheader("🎬 Input Video")
        st.video(temp_video_path)
        
        if st.button("Analyze Video Frames", key="analyze_button"):
            st.subheader("📈 Analysis Results")
            progress_bar = st.progress(0.0, text="Initializing Video Analysis...")
            try:
                video_results, processing_time = process_video_frames(
                    temp_video_path,
                    frame_interval_secs,
                    model,
                    TARGET_SIZE,
                    CLASS_INFO,
                    EXPECTED_CLASS_NAMES,
                    confidence_threshold,
                    progress_bar
                )
                
                if video_results is not None:
                    st.success(f"Video analysis complete! Processed {len(video_results)} frames in {processing_time:.2f} seconds.")
                    display_video_results(video_results)
            
            except Exception as e:
                st.error(f"An error occurred during video analysis: {e}")
                print(f"Video analysis error: {e}")
            finally:
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                    print(f"Temporary video file deleted: {temp_video_path}")
        else:
            st.info("Click 'Analyze Video Frames' to start processing.")
    else:
        st.info("☝️ Upload a video file to begin.")

if __name__ == "__main__":
    main()