# 🌱 Smart Garbage Classifier

> An intelligent waste classification system powered by deep learning to promote sustainable recycling practices.

[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.5+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.10+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Models-yellow?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/)

<div align="center">
  <img src="/api/placeholder/800/400" alt="Smart Garbage Classifier Demo" />
</div>

## 🚀 Overview

The Smart Garbage Classifier leverages computer vision and deep learning technology to accurately identify and categorize waste materials in real-time. Built with TensorFlow/Keras and wrapped in an intuitive Streamlit interface, this application helps individuals and organizations make informed recycling decisions, ultimately contributing to environmental sustainability.

---

## 📂 Project Structure

```
Garbage-Classifier-app./
├── app.py                   # Main application file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── data/                   # Data-related modules
│   ├── __init__.py
│   └── class_info.py        # Class information dictionary
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── model.py             # Model loading and prediction from Hugging Face
│   ├── image_processing.py  # Image preprocessing functions
│   └── video_processing.py  # Video processing functions
└── ui/                     # UI-related components
    ├── __init__.py
    └── components.py        # UI components and styling
```

---

## ⚙️ Installation & Configuration

### Prerequisites
- Python 3.8+
- Git
- Hugging Face account (for model access)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git@github.com:vtnguyen04/Garbage-Classifier-app.git
   cd Garbage-Classifier-app
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Hugging Face access:**
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```
   Follow the prompts to enter your Hugging Face token.

5. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

6. **Access the web interface:**
   Open your browser and navigate to `http://localhost:8501`

---

## ✨ Core Features

<table>
  <tr>
    <td width="50%">
      <h3>🖼️ Multi-format Input</h3>
      <ul>
        <li>Upload images directly from your device</li>
        <li>Analyze images from URLs</li>
        <li>Process videos for temporal waste analysis</li>
        <li>Live webcam classification (where available)</li>
      </ul>
    </td>
    <td width="50%">
      <h3>⚡ Real-time Processing</h3>
      <ul>
        <li>Instant classification results</li>
        <li>Dynamic confidence scoring</li>
        <li>Minimal latency on standard hardware</li>
        <li>Batch processing capabilities</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🔍 Advanced Analytics</h3>
      <ul>
        <li>Comprehensive probability distributions</li>
        <li>Material composition breakdown</li>
        <li>Classification confidence metrics</li>
        <li>Statistical reports on analyzed content</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🛠️ Customization Options</h3>
      <ul>
        <li>Adjustable confidence thresholds</li>
        <li>Configurable video frame sampling</li>
        <li>Visualization preferences</li>
        <li>Export results in multiple formats</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🧠 Technical Specifications

### Model Architecture

The application employs a fine-tuned **Xception** neural network architecture, renowned for its depth-wise separable convolutions that efficiently extract features while maintaining high accuracy with relatively lower computational requirements. The model is hosted on Hugging Face and loaded dynamically at runtime.

### Model Access

The waste classification model is hosted on Hugging Face and accessed through the Hugging Face Hub API. This approach offers several advantages:
- No need to store large model files locally
- Automatic model versioning and updates
- Seamless collaboration with the ML community
- Easy deployment across different environments

### Waste Categories

<div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: space-between;">
  <div style="flex: 1; min-width: 200px; border-left: 4px solid #4CAF50; padding-left: 15px; margin-bottom: 15px;">
    <h4>🧵 Fabric / Textiles</h4>
    <p>Clothing, linens, curtains, and other textile materials</p>
  </div>
  <div style="flex: 1; min-width: 200px; border-left: 4px solid #2196F3; padding-left: 15px; margin-bottom: 15px;">
    <h4>🍶 Glass</h4>
    <p>Bottles, jars, containers, and other glass products</p>
  </div>
  <div style="flex: 1; min-width: 200px; border-left: 4px solid #F44336; padding-left: 15px; margin-bottom: 15px;">
    <h4>🗑️ Non-Recyclable</h4>
    <p>General waste, mixed materials, and contaminated items</p>
  </div>
  <div style="flex: 1; min-width: 200px; border-left: 4px solid #FFC107; padding-left: 15px; margin-bottom: 15px;">
    <h4>📄 Paper & Cardboard</h4>
    <p>Newspapers, magazines, packaging, and cardboard boxes</p>
  </div>
  <div style="flex: 1; min-width: 200px; border-left: 4px solid #9C27B0; padding-left: 15px; margin-bottom: 15px;">
    <h4>♻️ Recyclable Inorganic</h4>
    <p>Metal cans, plastic bottles, containers, and other recyclable materials</p>
  </div>
</div>

### Performance Optimization

- **Image Processing**: Optimal performance with 299×299 pixel input images
- **Batch Processing**: Configurable batch sizes for efficient processing
- **Hardware Acceleration**: Automatic GPU utilization when available
- **Memory Management**: Optimized for various hardware configurations
- **Caching**: Model caching for improved inference speed

---

## 📊 Usage Guide

### Image Classification

1. Select **"Upload Image"** or **"Image URL"** from the sidebar
2. Upload an image file or provide a valid URL
3. Adjust the confidence threshold slider as needed
4. View classification results and disposal recommendations

<div align="center">
  <img src="/api/placeholder/700/300" alt="Image Classification Demo" />
</div>

### Video Analysis

1. Select **"Upload Video"** from the sidebar
2. Upload a video file in a supported format
3. Configure the frame processing interval
4. Review the classification timeline and aggregated results

<div align="center">
  <img src="/api/placeholder/700/300" alt="Video Analysis Demo" />
</div>

---

## 🛠️ Development

### Adding New Material Categories

To extend classification capabilities:

1. Update `data/class_info.py` with new category definitions:
   ```python
   WASTE_CATEGORIES = {
       # Existing categories...
       "new_category": {
           "description": "Description of the new waste category",
           "handling": "Instructions for proper disposal",
           "color": "#HEX_COLOR"
       }
   }
   ```

2. Retrain the model with the expanded dataset
3. Upload the updated model to Hugging Face Hub
4. Update the model reference in `utils/model.py`

### Hugging Face Model Loading

The application loads the model from Hugging Face Hub

### Environment Requirements

Complete dependencies are listed in `requirements.txt`, with core requirements including:
- Python 3.7+
- TensorFlow 2.5+
- Streamlit 1.10+
- Hugging Face Hub
- Pillow 8.0+
- NumPy 1.19+
- OpenCV 4.5+

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- The model was trained on a customized waste classification dataset
- Xception architecture originally developed by François Chollet
- Inspired by global initiatives to improve waste management and recycling processes
- Hugging Face for providing model hosting infrastructure

---