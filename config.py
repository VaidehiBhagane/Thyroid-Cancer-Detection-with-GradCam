"""
Configuration file for Thyroid Cancer Detection Application
Contains model paths, HuggingFace credentials, and other constants
"""

# HuggingFace Model Configuration
HF_REPO_ID = "vaidehibh/fibonacci_cnn"
HF_MODEL_FILENAME = "thyroid_cancer_model.h5"

# Model Configuration
MODEL_INPUT_SIZE = (224, 224)
MODEL_INPUT_CHANNELS = 3

# Application Settings
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
