import logging
from datetime import datetime
from fastapi import HTTPException
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.image_utils import preprocess_base64_image, encode_numpy_to_base64

logger = logging.getLogger(__name__)
_model = None

def set_model(m):
    global _model
    _model = m

def get_model():
    return _model if _model else __import__('app').get_model()

def validate(img):
    m = get_model()
    if not m: raise HTTPException(503, "Model not available")
    if not img or len(img) > 10485760: raise HTTPException(400, "Invalid image data or size")
    return m

def classify(p):
    c = int(p >= 0.5)
    return c, ["Benign (Non-Cancerous)", "Malignant (Cancerous)"][c], (p if c else 1-p)*100

def assess_risk(c, p):
    return (("High Risk", "Immediate specialist consultation and biopsy recommended") if p >= 0.75 
            else ("Moderate Risk", "Further diagnostic tests and specialist review advised")) if c \
           else (("Low Risk", "Routine monitoring recommended") if p <= 0.25 
                 else ("Borderline", "Follow-up imaging in 6-12 months advised"))

def get_conv_layer(m, ln=None):
    if ln: return ln
    # Get only Conv2D layers (exclude custom layers like DepthwiseSeparableConv)
    l = [x.name for x in m.layers if 'conv2d' in x.name.lower()]
    if not l: raise HTTPException(400, "No Conv2D layers found")
    logger.info(f"Using layer '{l[-1]}' for Grad-CAM")
    return l[-1]

def create_gradcam_vis(h, op):
    img = np.array(op.resize((224, 224)))
    img = img/255.0 if img.max()>1 else img
    hc = (plt.cm.jet(cv2.resize(h, (224, 224)))[:,:,:3]*255).astype(np.uint8)
    i8 = (img*255).astype(np.uint8)
    return {"original": encode_numpy_to_base64(i8), "heatmap": encode_numpy_to_base64(hc),
            "overlay": encode_numpy_to_base64(cv2.addWeighted(i8, 0.6, hc, 0.4, 0))}

def predict_image(img, fn=None):
    try:
        proc, orig = preprocess_base64_image(img)
        pred = float(get_model().predict(proc, verbose=0)[0][0])
        if np.isnan(pred) or np.isinf(pred): raise ValueError("Invalid prediction")
        logger.info(f"{fn or 'unknown'}: {pred:.4f}")
        return proc, orig, pred
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(500, "Prediction failed")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
