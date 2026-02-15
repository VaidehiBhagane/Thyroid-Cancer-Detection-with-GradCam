import base64, io, logging
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image

logger = logging.getLogger(__name__)

def decode_base64_image(base64_string: str) -> Image.Image:
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',', 1)[1]
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        logger.info(f"Decoded: size={image.size}, mode={image.mode}")
        return image
    except Exception as e:
        logger.error(f"Decode error: {str(e)}")
        raise ValueError(f"Invalid base64 image: {str(e)}")

def encode_image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    try:
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Encode error: {str(e)}")
        raise ValueError(f"Failed to encode: {str(e)}")

def encode_numpy_to_base64(img_array: np.ndarray, format: str = "PNG") -> str:
    try:
        img_array = (img_array * 255).astype(np.uint8) if img_array.max() <= 1.0 else img_array.astype(np.uint8)
        return encode_image_to_base64(Image.fromarray(img_array), format)
    except Exception as e:
        logger.error(f"Numpy encode error: {str(e)}")
        raise ValueError(f"Failed to encode array: {str(e)}")

def preprocess_base64_image(base64_string: str, target_size=(224, 224)) -> np.ndarray:
    try:
        img = decode_base64_image(base64_string)
        logger.info(f"Original: {img.size}, {img.mode}")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img_array = np.expand_dims(keras_image.img_to_array(img) / 255.0, axis=0)
        logger.info(f"Preprocessed: {img_array.shape}")
        return img_array, img
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Preprocess error: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to preprocess: {str(e)}")
