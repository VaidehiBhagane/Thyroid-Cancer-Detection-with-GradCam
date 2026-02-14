"""
Utility functions for handling base64 encoded images
"""
import base64
import io
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
import logging

logger = logging.getLogger(__name__)


def decode_base64_image(base64_string: str) -> Image.Image:
    """
    Decode base64 string to PIL Image.
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        PIL Image object
    
    Raises:
        ValueError: If base64 string is invalid or cannot be decoded
    """
    try:
        # Remove data URL prefix if present (e.g., "data:image/png;base64,")
        if ',' in base64_string:
            base64_string = base64_string.split(',', 1)[1]
        
        # Decode base64 string
        image_bytes = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        logger.info(f"Decoded image: size={image.size}, mode={image.mode}")
        return image
        
    except Exception as e:
        logger.error(f"Error decoding base64 image: {str(e)}")
        raise ValueError(f"Invalid base64 image data: {str(e)}")


def encode_image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """
    Encode PIL Image to base64 string.
    
    Args:
        image: PIL Image object
        format: Image format (PNG, JPEG, etc.)
    
    Returns:
        Base64 encoded string
    """
    try:
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return img_base64
        
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        raise ValueError(f"Failed to encode image: {str(e)}")


def encode_numpy_to_base64(img_array: np.ndarray, format: str = "PNG") -> str:
    """
    Encode numpy array to base64 string.
    
    Args:
        img_array: Numpy array (should be in range [0, 255] or [0, 1])
        format: Image format (PNG, JPEG, etc.)
    
    Returns:
        Base64 encoded string
    """
    try:
        # Ensure array is in [0, 255] range
        if img_array.max() <= 1.0:
            img_array = (img_array * 255).astype(np.uint8)
        else:
            img_array = img_array.astype(np.uint8)
        
        # Convert to PIL Image
        image = Image.fromarray(img_array)
        
        return encode_image_to_base64(image, format)
        
    except Exception as e:
        logger.error(f"Error encoding numpy array to base64: {str(e)}")
        raise ValueError(f"Failed to encode numpy array: {str(e)}")


def preprocess_base64_image(base64_string: str, target_size=(224, 224)) -> np.ndarray:
    """
    Preprocess base64 encoded image for model prediction.
    
    Args:
        base64_string: Base64 encoded image string
        target_size: Tuple (width, height) to resize image to
    
    Returns:
        Numpy array ready for model prediction with shape (1, 224, 224, 3)
    
    Raises:
        ValueError: If image cannot be processed or is invalid format
    """
    try:
        # Decode base64 to PIL Image
        img = decode_base64_image(base64_string)
        
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
        
        return img_array, img  # Return both processed array and PIL image
        
    except ValueError as e:
        # Re-raise ValueError as-is
        raise
    except Exception as e:
        logger.error(f"Error preprocessing base64 image: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to preprocess image: {str(e)}")
