from pydantic import BaseModel, Field
from typing import Optional

class ImageRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = Field(None, description="Original filename")

class PredictionResponse(BaseModel):
    success: bool
    timestamp: str
    filename: Optional[str] = None
    prediction: dict
    risk_assessment: str
    recommendation: str

class GradCAMRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = None
    layer_name: Optional[str] = None

class GradCAMResponse(BaseModel):
    success: bool
    timestamp: str
    filename: Optional[str] = None
    layer_used: str
    images: dict
    prediction: dict

class AnalyzeRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image string")
    filename: Optional[str] = None
    include_gradcam: bool = True

class AnalyzeResponse(BaseModel):
    success: bool
    timestamp: str
    filename: Optional[str] = None
    prediction: dict
    risk_assessment: str
    recommendation: str
    gradcam: Optional[dict] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    timestamp: str
    version: str

class ModelInfoResponse(BaseModel):
    model_name: str
    input_shape: list
    output_shape: list
    total_parameters: int
    classes: dict
    conv_layers: list

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str
