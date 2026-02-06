# 🦋 Thyroid Cancer Detection System

An AI-powered web application for detecting thyroid cancer from medical images using deep learning. This system analyzes thyroid ultrasound or pathology images and classifies them as **Benign** (non-cancerous) or **Malignant** (cancerous).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Medical Disclaimer](#medical-disclaimer)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🖼️ **Image Upload**: Support for PNG, JPG, JPEG formats
- 🤖 **AI-Powered Analysis**: Deep learning model with custom CNN architecture
- 📊 **Confidence Scoring**: Detailed probability metrics for predictions
- 🎨 **Interactive UI**: Clean, professional Streamlit interface
- 📥 **Results Download**: Export predictions as JSON reports
- 🔒 **Error Handling**: Robust validation and error recovery
- 📝 **Logging**: Comprehensive debugging and audit trail
- ⚕️ **Clinical Recommendations**: Risk-stratified guidance based on predictions

---

## 🏗️ System Architecture

```
User Upload Image (.png/.jpg/.jpeg)
        ↓
Image Preprocessing (224x224, RGB, Normalization)
        ↓
Deep Learning Model (thyroid_cancer_model.h5)
  - Custom LSTM Layers
  - DepthwiseSeparableConv
  - Avg2MaxPooling
        ↓
Binary Classification (Sigmoid Output)
        ↓
Results Display (0=Benign, 1=Malignant)
        ↓
Download Report (JSON)
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
python -c "import streamlit, tensorflow, keras; print('✅ Installation successful!')"

# Or run the application
streamlit run main.py
```

---

## 💻 Usage

### Running the Application

```bash
streamlit run main.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Using the Web Interface

1. **Upload Image**
   - Click "Browse files" or drag-and-drop
   - Select a thyroid medical image (.png, .jpg, .jpeg)
   - Preview appears automatically

2. **Analyze**
   - Click the "🔮 Analyze Image" button
   - Wait for processing (usually 1-3 seconds)

3. **View Results**
   - **Prediction**: Benign or Malignant
   - **Class**: 0 (Benign) or 1 (Malignant)
   - **Confidence Score**: Probability value (0.0 - 1.0)
   - **Clinical Recommendation**: Risk-based guidance

4. **Download Report**
   - Click "📥 Download Prediction Report"
   - Saves detailed JSON file with all results

### Command-Line Testing (Advanced)

```bash
# Check model loading
python -c "from main import load_model; model = load_model(); print(model.summary())"

# Test image preprocessing
python -c "from processing import preprocess_image; print('Image processing works!')"
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
├── main.py                          # Streamlit app + UI + model loading
├── processing.py                    # Image preprocessing pipeline
├── requirements.txt                 # Python dependencies
├── thyroid_cancer_model.h5          # Pre-trained deep learning model (3.5 MB)
├── thyroid-classification.ipynb     # Original training notebook
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore rules
│
└── logs/                            # Application logs (auto-created)
    └── app.log
```

---

## 🔧 API Reference

### `processing.py`

#### `preprocess_image(uploaded_file, target_size=(224, 224))`

Preprocesses uploaded image for model prediction.

**Parameters:**
- `uploaded_file` (UploadedFile): Streamlit file upload object
- `target_size` (tuple): Target dimensions (width, height)

**Returns:**
- `numpy.ndarray`: Preprocessed image array with shape (1, 224, 224, 3)

**Example:**
```python
from processing import preprocess_image

processed = preprocess_image(uploaded_file)
prediction = model.predict(processed)
```

---

### `main.py`

#### `load_model()`

Loads the pre-trained model with custom layers.

**Returns:**
- `tensorflow.keras.Model`: Compiled Keras model

**Caching:**
- Uses `@st.cache_resource` for performance
- Loads only once per session

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
# Error: "No model found in config file"
# Solution: Verify thyroid_cancer_model.h5 exists and is not corrupted
ls -lh thyroid_cancer_model.h5
```

**3. Image Upload Issues**
```bash
# Error: "cannot identify image file"
# Solution: Ensure file is valid PNG/JPG/JPEG
# Try opening in image viewer first
```

**4. Memory Errors**
```bash
# Error: "OOM when allocating tensor"
# Solution: Reduce image size or use machine with more RAM
```

### Debug Mode

Enable detailed logging:
```python
# In main.py, logging is automatically enabled
# Check logs/app.log for details
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

### Benign Case
```
Prediction: Benign (Non-Cancerous)
Class: 0
Confidence Score: 0.1234
Confidence %: 87.66%
Recommendation: ✅ LOW RISK BENIGN - Routine monitoring recommended
```

### Malignant Case
```
Prediction: Malignant (Cancerous)
Class: 1
Confidence Score: 0.8765
Confidence %: 87.65%
Recommendation: 🚨 HIGH RISK MALIGNANT - Immediate specialist consultation recommended
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd thyroid_cancer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

---

## 📝 License

This project is provided for **educational and research purposes only**. Use at your own risk.

---

## 📧 Support

For issues, questions, or suggestions:

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Submit via GitHub discussions
- � **Documentation**: See README.md and inline code comments

---

## 🙏 Acknowledgments

- TensorFlow/Keras teams for deep learning framework
- Streamlit for the amazing web framework
- Medical imaging community for research insights

---

## 📚 References

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Thyroid Cancer Research](https://www.cancer.org/cancer/thyroid-cancer.html)

---

**Made with ❤️ for better healthcare through AI**

*Last Updated: February 5, 2026*
