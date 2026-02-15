# 🦋 Thyroid Cancer Detection System

An AI-powered **REST API** for detecting thyroid cancer from medical images using deep learning. This system analyzes thyroid ultrasound or pathology images and classifies them as **Benign** (non-cancerous) or **Malignant** (cancerous).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Request & Response Examples](#request--response-examples)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Medical Disclaimer](#medical-disclaimer)
- [Migration from Streamlit](#migration-from-streamlit)
- [License](#license)

---

## ✨ Features

- 🚀 **FastAPI Backend**: High-performance REST API with automatic documentation
- 🖼️ **Base64 Image Support**: Send images as base64 encoded strings in JSON
- 🤖 **AI-Powered Analysis**: Deep learning model with custom CNN architecture
- 📊 **Confidence Scoring**: Detailed probability metrics for predictions
- 🔍 **Grad-CAM Visualization**: Model attention heatmaps showing decision-making regions
- 📥 **Downloadable Results**: All visualizations returned as base64 images
- 🔒 **Error Handling**: Robust validation and error recovery
- 📝 **Comprehensive Logging**: Detailed debugging and audit trail
- ⚕️ **Clinical Recommendations**: Risk-stratified guidance based on predictions
- 📚 **Auto-Generated Docs**: Interactive API documentation at `/docs`

---

## 🏗️ System Architecture

```
Client (JSON with base64 image)
        ↓
FastAPI REST API
        ↓
Image Preprocessing (224x224, RGB, Normalization)
        ↓
Deep Learning Model (from HuggingFace Hub: vaidehibh/fibonacci_cnn)
  - Custom LSTM Layers
  - DepthwiseSeparableConv
  - Avg2MaxPooling
        ↓
Binary Classification (Sigmoid Output)
  ├─ Prediction Endpoint (Class, Confidence)
  ├─ Grad-CAM Endpoint (Heatmap Visualization)
  └─ Analyze Endpoint (Combined Results)
        ↓
JSON Response (Prediction + Base64 Images)
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended

### Step 1: Clone or Download

```bash
# If using Git
git clone <repository-url>
cd thyroid_cancer

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test dependencies
python -c "import fastapi, tensorflow, keras; print('✅ Installation successful!')"
```

---

## 💻 Usage

### Running the API Server

```bash
# Development mode (with auto-reload)
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

### Quick Test

```bash
# Check if server is running
curl http://localhost:8000/

# Health check
curl http://localhost:8000/api/v1/health
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API information |
| `/api/v1/health` | GET | Health check and model status |
| `/api/v1/model-info` | GET | Model architecture and layer information |
| `/api/v1/predict` | POST | Predict cancer from image (basic) |
| `/api/v1/gradcam` | POST | Generate Grad-CAM visualization |
| `/api/v1/analyze` | POST | Complete analysis (prediction + Grad-CAM) |

---

## 📖 Request & Response Examples

### 1. Health Check

**Request:**
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-02-13 10:30:45",
  "version": "2.0.0"
}
```

---

### 2. Model Information

**Request:**
```bash
GET /api/v1/model-info
```

**Response:**
```json
{
  "model_name": "Thyroid Cancer Detection Model",
  "input_shape": [null, 224, 224, 3],
  "output_shape": [null, 1],
  "total_parameters": 1234567,
  "classes": {
    "0": "Benign (Non-Cancerous)",
    "1": "Malignant (Cancerous)"
  },
  "conv_layers": [
    "depthwise_separable_conv",
    "depthwise_separable_conv_1",
    "depthwise_separable_conv_2"
  ]
}
```

---

### 3. Prediction Endpoint

**Request:**
```bash
POST /api/v1/predict
Content-Type: application/json

{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ...",
  "filename": "thyroid_scan.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13 10:30:45",
  "filename": "thyroid_scan.jpg",
  "prediction": {
    "class": 0,
    "label": "Benign (Non-Cancerous)",
    "confidence_score": 0.1234,
    "confidence_percentage": 87.66
  },
  "risk_assessment": "Low Risk",
  "recommendation": "Routine monitoring recommended"
}
```

---

### 4. Grad-CAM Visualization

**Request:**
```bash
POST /api/v1/gradcam
Content-Type: application/json

{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ...",
  "filename": "thyroid_scan.jpg",
  "layer_name": null
}
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13 10:30:45",
  "filename": "thyroid_scan.jpg",
  "layer_used": "depthwise_separable_conv_2",
  "images": {
    "original": "base64_encoded_image...",
    "heatmap": "base64_encoded_heatmap...",
    "overlay": "base64_encoded_overlay..."
  },
  "prediction": {
    "class": 0,
    "label": "Benign (Non-Cancerous)",
    "confidence_score": 0.1234
  }
}
```

---

### 5. Complete Analysis

**Request:**
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ...",
  "filename": "thyroid_scan.jpg",
  "include_gradcam": true
}
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13 10:30:45",
  "filename": "thyroid_scan.jpg",
  "prediction": {
    "class": 1,
    "label": "Malignant (Cancerous)",
    "confidence_score": 0.8765,
    "confidence_percentage": 87.65
  },
  "risk_assessment": "High Risk",
  "recommendation": "Immediate specialist consultation and biopsy recommended",
  "gradcam": {
    "layer_used": "depthwise_separable_conv_2",
    "images": {
      "original": "base64_encoded_image...",
      "heatmap": "base64_encoded_heatmap...",
      "overlay": "base64_encoded_overlay..."
    }
  }
}
```

---

## 🐍 Python Client Example

```python
import requests
import base64
import json
from PIL import Image
import io

# Read and encode image
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# API endpoint
API_URL = "http://localhost:8000/api/v1"

# Encode image
image_base64 = encode_image("thyroid_scan.jpg")

# Make prediction
response = requests.post(
    f"{API_URL}/predict",
    json={
        "image": image_base64,
        "filename": "thyroid_scan.jpg"
    }
)

result = response.json()
print(f"Prediction: {result['prediction']['label']}")
print(f"Confidence: {result['prediction']['confidence_percentage']:.2f}%")
print(f"Risk: {result['risk_assessment']}")
print(f"Recommendation: {result['recommendation']}")

# Complete analysis with Grad-CAM
response = requests.post(
    f"{API_URL}/analyze",
    json={
        "image": image_base64,
        "filename": "thyroid_scan.jpg",
        "include_gradcam": True
    }
)

result = response.json()

# Decode and save Grad-CAM overlay
if result['gradcam']:
    overlay_base64 = result['gradcam']['images']['overlay']
    overlay_bytes = base64.b64decode(overlay_base64)
    overlay_image = Image.open(io.BytesIO(overlay_bytes))
    overlay_image.save("gradcam_overlay.png")
    print("Grad-CAM overlay saved as gradcam_overlay.png")
```

---

## 🧠 Model Details

### Architecture

- **Input Shape**: (224, 224, 3) RGB images
- **Framework**: Keras 3 with TensorFlow backend
- **Custom Layers**:
  - `SEBlock`: Squeeze-and-Excitation attention mechanism
  - `Avg2MaxPooling`: Hybrid pooling with batch normalization
  - `DepthwiseSeparableConv`: Efficient feature extraction with residual connections
- **Output**: Single sigmoid neuron (binary classification)
- **Training**: Binary cross-entropy loss, Adam optimizer
- **Total Layers**: 50 (including custom sublayers)

### Performance Metrics

- **Input Resolution**: 224×224 pixels
- **Image Preprocessing**: RGB conversion, normalization [0, 1]
- **Inference Time**: ~1-3 seconds per image
- **Memory Usage**: ~500MB

### Prediction Thresholds

| Score Range | Classification | Risk Level |
|-------------|----------------|------------|
| ≥ 0.75      | Malignant     | High Risk  |
| 0.50 - 0.74 | Malignant     | Moderate   |
| 0.25 - 0.49 | Benign        | Borderline |
| < 0.25      | Benign        | Low Risk   |

---

## 📁 Project Structure

```
thyroid_cancer/
│
├── app.py                           # FastAPI main application
├── config.py                        # Configuration (HuggingFace settings)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── api/                             # API layer
│   ├── __init__.py
│   ├── routes.py                    # API endpoints
│   └── schemas.py                   # Pydantic request/response models
│
├── model/                           # Model layer
│   ├── __init__.py
│   ├── custom_layers.py             # Custom Keras layers
│   └── model_loader.py              # Model loading from HuggingFace
│
├── model_cache/                     # Downloaded model cache (auto-created)
│
├── utils/                           # Utilities
│   ├── __init__.py
│   ├── gradcam.py                   # Grad-CAM visualization
│   ├── image_utils.py               # Base64 image processing
│   ├── logger_config.py             # Logging configuration
│   └── processing.py                # Image preprocessing (legacy)
│
├── logs/                            # Application logs (auto-created)
│   └── app.log
│
├── experiments/                     # Jupyter notebooks
│   └── 1Thyroid.ipynb
│
└── main_streamlit.py                # Legacy Streamlit app (backup)
```

---

## 🔧 API Reference

### Core Modules

#### `api/routes.py`

Contains all API endpoint handlers:
- `health_check()` - Server and model status
- `get_model_info()` - Model architecture details
- `predict()` - Image classification
- `generate_gradcam()` - Grad-CAM visualization
- `analyze_complete()` - Combined analysis

#### `api/schemas.py`

Pydantic models for request/response validation:
- `ImageRequest` - Base64 image input
- `PredictionResponse` - Prediction results
- `GradCAMRequest` - Grad-CAM parameters
- `GradCAMResponse` - Visualization output
- `AnalyzeRequest` - Complete analysis input
- `AnalyzeResponse` - Combined results
- `HealthResponse` - Health check output
- `ModelInfoResponse` - Model metadata

#### `utils/image_utils.py`

Base64 image handling functions:
- `decode_base64_image(base64_string)` - Decode to PIL Image
- `encode_image_to_base64(image, format)` - Encode PIL to base64
- `encode_numpy_to_base64(img_array, format)` - Encode numpy to base64
- `preprocess_base64_image(base64_string, target_size)` - Full preprocessing pipeline

---

---

## 🔄 Migration from Streamlit

This project has been migrated from Streamlit to FastAPI for better scalability and API-first architecture.

### What Changed?

| Aspect | Before (Streamlit) | After (FastAPI) |
|--------|-------------------|-----------------|
| **Interface** | Web UI | REST API |
| **Input** | File upload | Base64 JSON |
| **Output** | Interactive UI | JSON responses |
| **Deployment** | Streamlit Cloud | Any server/cloud |
| **Integration** | Standalone | API clients |
| **Performance** | Single user | Multi-user/concurrent |

### Running the Old Streamlit App

The original Streamlit application is preserved as `main_streamlit.py`:

```bash
# Install streamlit if needed
pip install streamlit

# Run the old UI
streamlit run main_streamlit.py
```

### Migration Benefits

✅ **Better Integration**: Can be integrated with any frontend framework  
✅ **Scalability**: Handle multiple concurrent requests  
✅ **API-First**: Mobile apps, web apps, microservices  
✅ **Documentation**: Auto-generated interactive docs  
✅ **Performance**: Faster response times  
✅ **Deployment**: More flexible deployment options  

---

## 🐛 Troubleshooting

### Common Issues

**1. Module Import Errors**
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**2. Model Loading Failure**
```bash
# Error: "Failed to download model from HuggingFace"
# Solution 1: Check internet connection
# Solution 2: Verify HuggingFace is accessible
# Solution 3: Clear model cache and retry
rm -rf model_cache
# The model will be automatically downloaded on next startup
```

**3. Base64 Decode Errors**
```bash
# Error: "Invalid base64 image data"
# Solution: Ensure proper base64 encoding
# Remove data URI prefix if present (data:image/png;base64,)
```

**4. Port Already in Use**
```bash
# Error: "Address already in use"
# Solution: Change port or kill existing process
uvicorn app:app --host 0.0.0.0 --port 8001
```

**5. CORS Issues (Frontend)**
```bash
# Error: "CORS policy blocked"
# Solution: Update CORS origins in app.py
# Change allow_origins=["*"] to specific domains
```

### Debug Mode

Enable detailed logging:
```python
# Logs are automatically written to logs/app.log
# Set log level in utils/logger_config.py

import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Testing Endpoints

```bash
# Test with curl
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"image":"YOUR_BASE64_STRING","filename":"test.jpg"}'

# Test with Python requests
import requests
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())
```

---

## ⚕️ Medical Disclaimer

**IMPORTANT:** This application is a **research and educational tool** only.

- ❌ NOT a substitute for professional medical diagnosis
- ❌ NOT FDA-approved or clinically validated
- ❌ Should NOT be used for clinical decision-making

**Always consult qualified healthcare professionals for:**
- Definitive diagnosis
- Treatment planning
- Medical advice

The developers assume **no liability** for medical decisions made using this tool.

---

## 📊 Example Results

### Benign Case (Low Risk)
```json
{
  "prediction": {
    "class": 0,
    "label": "Benign (Non-Cancerous)",
    "confidence_score": 0.1234,
    "confidence_percentage": 87.66
  },
  "risk_assessment": "Low Risk",
  "recommendation": "Routine monitoring recommended"
}
```

### Malignant Case (High Risk)
```json
{
  "prediction": {
    "class": 1,
    "label": "Malignant (Cancerous)",
    "confidence_score": 0.8765,
    "confidence_percentage": 87.65
  },
  "risk_assessment": "High Risk",
  "recommendation": "Immediate specialist consultation and biopsy recommended"
}
```
# Streamlit Deployment
https://thyroid-cancer-detection.streamlit.app/
---

## 📝 License

This project is provided for **educational and research purposes only**. Use at your own risk.

---

## 📧 Support

For issues, questions, or suggestions:

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Submit via GitHub discussions
- 📖 **Documentation**: See `/docs` endpoint when server is running

---

## 🙏 Acknowledgments

- TensorFlow/Keras teams for deep learning framework
- FastAPI team for the amazing web framework
- Pydantic for data validation
- Medical imaging community for research insights

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Grad-CAM Paper](https://arxiv.org/abs/1610.02391)
- [Thyroid Cancer Research](https://www.cancer.org/cancer/thyroid-cancer.html)

---

**Made with ❤️ for better healthcare through AI**

*Last Updated: February 13, 2026*
*Version: 2.0.0 (FastAPI)*
