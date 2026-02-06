import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
import logging

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Preprocess image for prediction
# --------------------------------------------------
def preprocess_image(uploaded_file, target_size=(224, 224)):
    """
    Preprocess uploaded image file for model prediction.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        target_size: Tuple (width, height) to resize image to
    
    Returns:
        numpy array ready for model prediction with shape (1, 224, 224, 3)
    
    Raises:
        ValueError: If image cannot be processed or is invalid format
        FileNotFoundError: If uploaded file is None or invalid
    """
    try:
        if uploaded_file is None:
            raise FileNotFoundError("No file uploaded")
        
        logger.info(f"Processing image: {uploaded_file.name}")
        
        # Open image using PIL
        img = Image.open(uploaded_file)
        logger.info(f"Original image size: {img.size}, mode: {img.mode}")
        
        # Convert to RGB if image is grayscale or has alpha channel
        if img.mode != 'RGB':
            logger.info(f"Converting image from {img.mode} to RGB")
            img = img.convert('RGB')
        
        # Resize to target size
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        logger.info(f"Image resized to: {target_size}")
        
        # Convert to numpy array
        img_array = keras_image.img_to_array(img)
        
        # Normalize pixel values to [0, 1] range
        img_array = img_array / 255.0
        logger.info("Image normalized to [0, 1] range")
        
        # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)
        logger.info(f"Final image shape: {img_array.shape}")
        
        return img_array
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to preprocess image: {str(e)}")
