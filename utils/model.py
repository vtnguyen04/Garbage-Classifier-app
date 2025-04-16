import tensorflow as tf
import numpy as np
import streamlit as st
from pathlib import Path
import requests
import time
MODEL_DOWNLOAD_URL = "https://huggingface.co/iuQuynhThu/Garbage/resolve/main/model.keras"
# Tên file để lưu model cục bộ trong môi trường Streamlit Cloud
LOCAL_MODEL_FILENAME = "downloaded_model.keras"
CACHE_DIR = Path("./model_cache") # Thư mục để lưu file tải về

@st.cache_resource(ttl=3600) # Cache model trong 1 giờ, hoặc bỏ ttl để cache vô hạn
def download_and_load_keras_model(model_url: str, save_dir: Path, model_filename: str) -> tf.keras.Model | None:
    """
    Downloads the model if not present locally, then loads and returns it.
    Caches the loaded model object.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    local_model_path = save_dir / model_filename

    # 1. Download model if it doesn't exist locally
    if not local_model_path.exists():
        st.info(f"Model file not found locally. Downloading from {model_url}...")
        try:
            # Use requests with streaming for large files
            with requests.get(model_url, stream=True) as r:
                r.raise_for_status()  # Check if the request was successful
                total_size_in_bytes = int(r.headers.get('content-length', 0))
                block_size = 1024 * 8 # 8 Kibibytes
                downloaded_size = 0

                progress_bar = st.progress(0.0, text="Starting model download...")
                start_time = time.time()

                with open(local_model_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=block_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size_in_bytes > 0:
                            progress = min(1.0, downloaded_size / total_size_in_bytes)
                            elapsed_time = time.time() - start_time
                            speed_mb_s = (downloaded_size / (1024*1024)) / elapsed_time if elapsed_time > 0 else 0
                            progress_bar.progress(progress, text=f"Downloading... {int(progress*100)}% ({downloaded_size/(1024*1024):.1f}/{total_size_in_bytes/(1024*1024):.1f} MB @ {speed_mb_s:.2f} MB/s)")
                        else:
                            # Show progress in MB if total size is unknown
                            progress_bar.progress(0.0, text=f"Downloading... {downloaded_size/(1024*1024):.1f} MB")

                progress_bar.progress(1.0, text="Model download complete!")
                st.success(f"Model saved locally to {local_model_path}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading model: {e}")
            # Clean up partial download if it exists
            if local_model_path.exists():
                local_model_path.unlink()
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred during download: {e}")
            if local_model_path.exists():
                local_model_path.unlink()
            return None

    # 2. Load the model from the local file
    try:
        st.info(f"Loading model from {local_model_path}...")
        model = tf.keras.models.load_model(local_model_path)
        st.success("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"Error loading model from file: {e}")
        return None


# @st.cache_resource
# def load_keras_model(model_path):
#     if not Path(model_path).is_file():
#         st.error(f"Model file not found at: {model_path}")
#         return None
#     try:
#         model = tf.keras.models.load_model(model_path)
#         print(f"Model loaded successfully from {model_path}")
#         return model
#     except Exception as e:
#         st.error(f"Error loading model: {e}")
#         return None

def predict_image(model, img_batch, expected_class_names, confidence_threshold):
    if img_batch is not None:
        try:
            predictions = model.predict(img_batch)
            prediction_probs = predictions[0]
            
            predicted_index = np.argmax(prediction_probs)
            confidence = np.max(prediction_probs) * 100
            
            if confidence >= confidence_threshold:
                if predicted_index < len(expected_class_names):
                    predicted_class_key = expected_class_names[predicted_index]
                else:
                    predicted_class_key = 'unknown'
            else:
                predicted_class_key = 'unknown'
                
            return predicted_class_key, confidence, prediction_probs
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 'unknown', 0, None
    return 'unknown', 0, None