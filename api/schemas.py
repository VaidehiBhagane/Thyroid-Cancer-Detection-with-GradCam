"""
Pydantic models for API request and response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ImageRequest(BaseModel):
    """Request model for image-based predictions"""
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = Field(None, description="Original filename (optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "filename": "thyroid_scan.jpg"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    success: bool = Field(..., description="Whether the prediction was successful")
    timestamp: str = Field(..., description="Timestamp of prediction")
    filename: Optional[str] = Field(None, description="Original filename if provided")
    prediction: dict = Field(..., description="Prediction results")
    risk_assessment: str = Field(..., description="Risk level assessment")
    recommendation: str = Field(..., description="Clinical recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
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
        }


class GradCAMRequest(BaseModel):
    """Request model for Grad-CAM visualization"""
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = Field(None, description="Original filename (optional)")
    layer_name: Optional[str] = Field(None, description="Specific layer name for Grad-CAM (optional, auto-detected if not provided)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "filename": "thyroid_scan.jpg",
                "layer_name": None
            }
        }


class GradCAMResponse(BaseModel):
    """Response model for Grad-CAM visualization"""
    success: bool = Field(..., description="Whether Grad-CAM generation was successful")
    timestamp: str = Field(..., description="Timestamp of generation")
    filename: Optional[str] = Field(None, description="Original filename if provided")
    layer_used: str = Field(..., description="Convolutional layer used for Grad-CAM")
    images: dict = Field(..., description="Base64 encoded images")
    prediction: dict = Field(..., description="Associated prediction results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2026-02-13 10:30:45",
                "filename": "thyroid_scan.jpg",
                "layer_used": "depthwise_separable_conv_2",
                "images": {
                    "original": "base64_string...",
                    "heatmap": "base64_string...",
                    "overlay": "base64_string..."
                },
                "prediction": {
                    "class": 0,
                    "label": "Benign (Non-Cancerous)",
                    "confidence_score": 0.1234
                }
            }
        }


class AnalyzeRequest(BaseModel):
    """Request model for complete analysis (prediction + Grad-CAM)"""
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = Field(None, description="Original filename (optional)")
    include_gradcam: bool = Field(True, description="Whether to include Grad-CAM visualization")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "filename": "thyroid_scan.jpg",
                "include_gradcam": True
            }
        }


class AnalyzeResponse(BaseModel):
    """Response model for complete analysis"""
    success: bool = Field(..., description="Whether the analysis was successful")
    timestamp: str = Field(..., description="Timestamp of analysis")
    filename: Optional[str] = Field(None, description="Original filename if provided")
    prediction: dict = Field(..., description="Prediction results")
    risk_assessment: str = Field(..., description="Risk level assessment")
    recommendation: str = Field(..., description="Clinical recommendation")
    gradcam: Optional[dict] = Field(None, description="Grad-CAM visualization data if requested")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class ModelInfoResponse(BaseModel):
    """Response model for model information"""
    model_name: str = Field(..., description="Model name")
    input_shape: list = Field(..., description="Expected input shape")
    output_shape: list = Field(..., description="Model output shape")
    total_parameters: int = Field(..., description="Total number of parameters")
    classes: dict = Field(..., description="Classification labels")
    conv_layers: list = Field(..., description="Available convolutional layers for Grad-CAM")


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="Error timestamp")
