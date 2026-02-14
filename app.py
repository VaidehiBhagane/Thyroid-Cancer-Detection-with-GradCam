"""
FastAPI application for Thyroid Cancer Detection System
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import custom modules
from utils.logger_config import configure_logging
from model.model_loader import load_model
from api.routes import router as api_router

# Configure logging
logger = configure_logging()

# Initialize FastAPI app
app = FastAPI(
    title="🦋 Thyroid Cancer Detection API",
    description="AI-powered API for detecting thyroid cancer from medical images using deep learning",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (for future frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    try:
        logger.info("Loading thyroid cancer detection model...")
        model = load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.critical(f"Failed to load model: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Thyroid Cancer Detection API")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": " Thyroid Cancer Detection API",
        "version": "2.0.0",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "model_info": "/api/v1/model-info",
            "predict": "/api/v1/predict",
            "gradcam": "/api/v1/gradcam",
            "analyze": "/api/v1/analyze"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )

def get_model():
    """Get the loaded model instance"""
    return model

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
