import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def preprocess_image(img_pil, target_size):
    try:
        img_resized = img_pil.resize(target_size, Image.Resampling.LANCZOS)
        img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
        img_array = img_array / 255.0
        img_batch = np.expand_dims(img_array, axis=0)
        return img_batch
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def load_image_from_url(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        img_pil = Image.open(BytesIO(response.content)).convert('RGB')
        return img_pil
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image from URL: {e}")
        return None
    except Exception as e:
        st.error(f"Error opening image from URL: {e}")
        return None

def load_uploaded_image(uploaded_file):
    try:
        img_pil = Image.open(uploaded_file).convert('RGB')
        return img_pil
    except Exception as e:
        st.error(f"Error opening uploaded file: {e}")
        return None