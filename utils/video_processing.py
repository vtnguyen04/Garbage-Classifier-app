import cv2
import time
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from utils.model import predict_image
from utils.image_processing import preprocess_image

def process_video_frames(video_path, frame_interval_secs, model, target_size, class_info_dict, expected_class_names, confidence_threshold, progress_bar):
    results = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error: Could not open video file.")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_skip = int(fps * frame_interval_secs)
    if frame_skip < 1: frame_skip = 1

    print(f"Video Info: FPS={fps:.2f}, Total Frames={total_frames}, Frame Skip={frame_skip} (Interval: {frame_interval_secs}s)")

    frame_count = 0
    processed_frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            try:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(frame_rgb)

                img_batch = preprocess_image(img_pil, target_size)
                if img_batch is not None:
                    predicted_class_key, confidence, _ = predict_image(
                        model, img_batch, expected_class_names, confidence_threshold
                    )

                    timestamp = frame_count / fps
                    results.append({
                        "Frame": frame_count,
                        "Timestamp (s)": round(timestamp, 2),
                        "Predicted Class": class_info_dict[predicted_class_key]['display_name'],
                        "Confidence (%)": round(confidence, 2),
                        "Class Key": predicted_class_key
                    })
                    processed_frame_count += 1

            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")

        frame_count += 1
        if total_frames > 0:
            progress_bar.progress(frame_count / total_frames, text=f"Processing Video: Frame {frame_count}/{total_frames}")
        else:
             progress_bar.progress(processed_frame_count % 100 / 100.0, text=f"Processing Video: Frame {frame_count}")

    cap.release()
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Video processing finished. Processed {processed_frame_count} frames in {processing_time:.2f} seconds.")
    progress_bar.empty()
    return results, processing_time