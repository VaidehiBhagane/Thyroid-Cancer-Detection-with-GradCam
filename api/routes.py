"""
API routes for Thyroid Cancer Detection API
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import json

from api.schemas import (
    ImageRequest, PredictionResponse, GradCAMRequest, GradCAMResponse,
    AnalyzeRequest, AnalyzeResponse, HealthResponse, ModelInfoResponse
)
from utils.image_utils import preprocess_base64_image, encode_numpy_to_base64
from utils.gradcam import make_gradcam_heatmap
from utils.pdf_generator import generate_pdf_report

logger = logging.getLogger(__name__)
router = APIRouter()
_model = None

def set_model(model):
    """Set the global model instance"""
    global _model
    _model = model

def get_model():
    """Get the global model instance"""
    if _model is None:
        from app import get_model as app_get_model
        return app_get_model()
    return _model

# Helper functions
def get_classification_data(prediction):
    """Calculate classification metrics from prediction score"""
    predicted_class = 1 if prediction >= 0.5 else 0
    label = "Malignant (Cancerous)" if predicted_class == 1 else "Benign (Non-Cancerous)"
    confidence_pct = prediction * 100 if predicted_class == 1 else (1 - prediction) * 100
    return predicted_class, label, confidence_pct

def get_risk_assessment(predicted_class, prediction):
    """Determine risk level and recommendation based on prediction"""
    if predicted_class == 1:
        if prediction >= 0.75:
            return "High Risk", "Immediate specialist consultation and biopsy recommended"
        return "Moderate Risk", "Further diagnostic tests and specialist review advised"
    else:
        if prediction <= 0.25:
            return "Low Risk", "Routine monitoring recommended"
        return "Borderline", "Follow-up imaging in 6-12 months advised"

def find_last_conv_layer(model, layer_name=None):
    """Find the last convolutional layer in the model"""
    if layer_name:
        return layer_name
    conv_layers = [
        layer.name for layer in model.layers 
        if 'depthwise_separable_conv' in layer.name.lower() or 'conv' in layer.name.lower()
    ]
    if not conv_layers:
        raise HTTPException(status_code=400, detail="No convolutional layers found in model")
    return conv_layers[-1]

def prepare_gradcam_images(heatmap, original_pil):
    """Prepare and encode Grad-CAM visualization images"""
    original_img = np.array(original_pil.resize((224, 224)))
    if original_img.max() > 1:
        original_img = original_img / 255.0
    
    heatmap_resized = cv2.resize(heatmap, dsize=(224, 224), interpolation=cv2.INTER_LINEAR)
    heatmap_colored = (plt.cm.jet(heatmap_resized)[:, :, :3] * 255).astype(np.uint8)
    
    overlay = (original_img * 255).astype(np.uint8)
    overlay = cv2.addWeighted(overlay, 0.6, heatmap_colored, 0.4, 0)
    
    return {
        "original": encode_numpy_to_base64((original_img * 255).astype(np.uint8)),
        "heatmap": encode_numpy_to_base64(heatmap_colored),
        "overlay": encode_numpy_to_base64(overlay)
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API and model status"""
    try:
        model = get_model()
        model_loaded = model is not None
        return HealthResponse(
            status="healthy" if model_loaded else "unhealthy",
            model_loaded=model_loaded,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            version="2.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the loaded model"""
    try:
        model = get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        conv_layers = [
            layer.name for layer in model.layers 
            if 'depthwise_separable_conv' in layer.name.lower() or 'conv' in layer.name.lower()
        ]
        
        return ModelInfoResponse(
            model_name="Thyroid Cancer Detection Model",
            input_shape=list(model.input_shape),
            output_shape=list(model.output_shape),
            total_parameters=model.count_params(),
            classes={"0": "Benign (Non-Cancerous)", "1": "Malignant (Cancerous)"},
            conv_layers=conv_layers
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: ImageRequest):
    """Predict thyroid cancer from base64 encoded image"""
    try:
        model = get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        logger.info(f"Starting prediction for file: {request.filename or 'unknown'}")
        
        processed_image, _ = preprocess_base64_image(request.image)
        prediction = model.predict(processed_image, verbose=0)[0][0]
        logger.info(f"Prediction completed: {prediction:.4f}")
        
        predicted_class, label, confidence_pct = get_classification_data(prediction)
        risk, recommendation = get_risk_assessment(predicted_class, prediction)
        
        logger.info(f"Classification: {label} (Class: {predicted_class}), Risk: {risk}")
        
        return PredictionResponse(
            success=True,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename=request.filename,
            prediction={
                "class": int(predicted_class),
                "label": label,
                "confidence_score": float(prediction),
                "confidence_percentage": float(confidence_pct)
            },
            risk_assessment=risk,
            recommendation=recommendation
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/gradcam", response_model=GradCAMResponse)
async def generate_gradcam(request: GradCAMRequest):
    """Generate Grad-CAM visualization for base64 encoded image"""
    try:
        model = get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        logger.info(f"Starting Grad-CAM generation for file: {request.filename or 'unknown'}")
        
        processed_image, original_pil = preprocess_base64_image(request.image)
        prediction = model.predict(processed_image, verbose=0)[0][0]
        predicted_class, label, _ = get_classification_data(prediction)
        
        last_conv_name = find_last_conv_layer(model, request.layer_name)
        logger.info(f"Using layer '{last_conv_name}' for Grad-CAM")
        
        heatmap = make_gradcam_heatmap(processed_image, model, last_conv_name)
        images = prepare_gradcam_images(heatmap, original_pil)
        
        logger.info("Grad-CAM visualization generated successfully")
        
        return GradCAMResponse(
            success=True,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename=request.filename,
            layer_used=last_conv_name,
            images=images,
            prediction={"class": int(predicted_class), "label": label, "confidence_score": float(prediction)}
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Grad-CAM generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Grad-CAM generation failed: {str(e)}")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_complete(request: AnalyzeRequest):
    """Complete analysis: prediction + optional Grad-CAM visualization"""
    try:
        model = get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        logger.info(f"Starting complete analysis for file: {request.filename or 'unknown'}")
        
        processed_image, original_pil = preprocess_base64_image(request.image)
        prediction = model.predict(processed_image, verbose=0)[0][0]
        logger.info(f"Prediction completed: {prediction:.4f}")
        
        predicted_class, label, confidence_pct = get_classification_data(prediction)
        risk, recommendation = get_risk_assessment(predicted_class, prediction)
        
        gradcam_data = None
        if request.include_gradcam:
            try:
                last_conv_name = find_last_conv_layer(model)
                logger.info(f"Using layer '{last_conv_name}' for Grad-CAM")
                heatmap = make_gradcam_heatmap(processed_image, model, last_conv_name)
                gradcam_data = {
                    "layer_used": last_conv_name,
                    "images": prepare_gradcam_images(heatmap, original_pil)
                }
                logger.info("Grad-CAM visualization generated successfully")
            except Exception as e:
                logger.warning(f"Grad-CAM generation failed: {str(e)}")
        
        logger.info(f"Complete analysis finished for {request.filename or 'unknown'}")
        
        return AnalyzeResponse(
            success=True,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename=request.filename,
            prediction={
                "class": int(predicted_class),
                "label": label,
                "confidence_score": float(prediction),
                "confidence_percentage": float(confidence_pct)
            },
            risk_assessment=risk,
            recommendation=recommendation,
            gradcam=gradcam_data
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/report/pdf")
async def download_pdf_report(request: AnalyzeRequest):
    """Generate and download PDF report for the analysis"""
    try:
        analysis_result = await analyze_complete(request)
        if not analysis_result.success:
            raise HTTPException(status_code=400, detail="Analysis failed, cannot generate report")
        
        prediction_data = {
            'timestamp': analysis_result.timestamp,
            'filename': analysis_result.filename or 'Unknown',
            'prediction': analysis_result.prediction,
            'risk_assessment': analysis_result.risk_assessment,
            'recommendation': analysis_result.recommendation
        }
        
        pdf_buffer = generate_pdf_report(prediction_data, analysis_result.gradcam if request.include_gradcam else None)
        filename = f"thyroid_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        logger.info(f"PDF report generated: {filename}")
        
        return StreamingResponse(
            pdf_buffer, media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF report generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")


@router.post("/report/json")
async def download_json_report(request: AnalyzeRequest):
    """Generate and download JSON report for the analysis"""
    try:
        analysis_result = await analyze_complete(request)
        if not analysis_result.success:
            raise HTTPException(status_code=400, detail="Analysis failed, cannot generate report")
        
        json_buffer = BytesIO(json.dumps(analysis_result.dict(), indent=2).encode('utf-8'))
        filename = f"thyroid_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        logger.info(f"JSON report generated: {filename}")
        
        return StreamingResponse(
            json_buffer, media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"JSON report generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate JSON report: {str(e)}")
