import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import json
from api.schemas import *
from api.routes.routes_functions import get_model, validate, classify, assess_risk, get_conv_layer, create_gradcam_vis, predict_image, get_timestamp
from utils.gradcam import make_gradcam_heatmap
from utils.pdf_generator import generate_pdf_report

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    m = get_model()
    return HealthResponse(status="healthy" if m else "unhealthy", model_loaded=bool(m), 
                         timestamp=get_timestamp(), version="2.0.0")

@router.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    try:
        m = validate("")
        return ModelInfoResponse(model_name="Thyroid Cancer Detection Model", input_shape=list(m.input_shape),
                                output_shape=list(m.output_shape), total_parameters=m.count_params(),
                                classes={"0": "Benign (Non-Cancerous)", "1": "Malignant (Cancerous)"},
                                conv_layers=[l.name for l in m.layers if 'conv2d' in l.name.lower()])
    except: raise HTTPException(503, "Model not available")

@router.post("/predict", response_model=PredictionResponse)
async def predict(req: ImageRequest):
    try:
        validate(req.image)
        _, _, p = predict_image(req.image, req.filename)
        c, l, cf = classify(p)
        r, rc = assess_risk(c, p)
        return PredictionResponse(success=True, timestamp=get_timestamp(), filename=req.filename,
                                 prediction={"class": c, "label": l, "confidence_score": float(p), 
                                           "confidence_percentage": float(cf)},
                                 risk_assessment=r, recommendation=rc)
    except HTTPException: raise
    except Exception as e:
        logger.error(f"Predict error: {e}")
        raise HTTPException(500, "Prediction failed")

@router.post("/gradcam", response_model=GradCAMResponse)
async def generate_gradcam(req: GradCAMRequest):
    try:
        m = validate(req.image)
        pr, og, p = predict_image(req.image, req.filename)
        c, l, _ = classify(p)
        ly = get_conv_layer(m, req.layer_name)
        h = make_gradcam_heatmap(pr, m, ly)
        return GradCAMResponse(success=True, timestamp=get_timestamp(), filename=req.filename,
                              layer_used=ly, images=create_gradcam_vis(h, og),
                              prediction={"class": c, "label": l, "confidence_score": float(p)})
    except HTTPException: raise
    except Exception as e:
        logger.error(f"GradCAM error: {e}")
        raise HTTPException(500, "Grad-CAM failed")

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_complete(req: AnalyzeRequest):
    try:
        m = validate(req.image)
        pr, og, p = predict_image(req.image, req.filename)
        c, l, cf = classify(p)
        r, rc = assess_risk(c, p)
        gd = None
        if req.include_gradcam:
            try:
                ly = get_conv_layer(m)
                gd = {"layer_used": ly, "images": create_gradcam_vis(make_gradcam_heatmap(pr, m, ly), og)}
            except Exception as e: logger.warning(f"GradCAM skipped: {e}")
        return AnalyzeResponse(success=True, timestamp=get_timestamp(), filename=req.filename,
                              prediction={"class": c, "label": l, "confidence_score": float(p),
                                        "confidence_percentage": float(cf)},
                              risk_assessment=r, recommendation=rc, gradcam=gd)
    except HTTPException: raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(500, "Analysis failed")

@router.post("/report/pdf")
async def download_pdf_report(req: AnalyzeRequest):
    try:
        res = await analyze_complete(req)
        pdf = generate_pdf_report({'timestamp': res.timestamp, 'filename': res.filename or 'Unknown',
                                   'prediction': res.prediction, 'risk_assessment': res.risk_assessment,
                                   'recommendation': res.recommendation}, res.gradcam if req.include_gradcam else None)
        fn = f"thyroid_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return StreamingResponse(pdf, media_type="application/pdf",
                               headers={"Content-Disposition": f"attachment; filename={fn}"})
    except Exception as e:
        logger.error(f"PDF error: {e}")
        raise HTTPException(500, "PDF failed")

@router.post("/report/json")
async def download_json_report(req: AnalyzeRequest):
    try:
        res = await analyze_complete(req)
        fn = f"thyroid_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return StreamingResponse(BytesIO(json.dumps(res.dict(), indent=2).encode()), 
                               media_type="application/json",
                               headers={"Content-Disposition": f"attachment; filename={fn}"})
    except Exception as e:
        logger.error(f"JSON error: {e}")
        raise HTTPException(500, "JSON failed")
