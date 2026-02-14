import streamlit as st
import logging
from PIL import Image
from datetime import datetime
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Import custom modules
from utils.logger_config import configure_logging
from utils.processing import preprocess_image
from model.model_loader import load_model
from utils.gradcam import make_gradcam_heatmap
# Note: Custom layers are implicitly needed for loading, but are handled within model_loader.py
# If explicit import is needed for other reasons, uncomment below:
# from model.custom_layers import CustomLSTM, Avg2MaxPooling, DepthwiseSeparableConv

matplotlib.use('Agg')  # Use non-interactive backend for Streamlit

# --------------------------------------------------
# Configure Logging
# --------------------------------------------------
# Setup logging using the modular configuration
logger = configure_logging()

# --------------------------------------------------
# Load model
# --------------------------------------------------
# Load model with error handling
try:
    model = load_model()
except Exception as e:
    logger.critical(f"Critical error during model initialization: {str(e)}")
    st.error("Application failed to initialize. Please check logs.")
    st.stop()

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.title("🦋 Thyroid Cancer Detection System")
st.write("Upload a thyroid medical image (ultrasound/pathology) for AI-powered cancer detection")

st.header("📤 Upload Thyroid Image")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a thyroid image file (.png, .jpg, .jpeg)",
    type=["png", "jpg", "jpeg"],
    help="Upload a thyroid ultrasound or pathology image for analysis"
)

# Display uploaded image
if uploaded_file is not None:
    # Show the uploaded image
    st.subheader("📸 Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption="Thyroid Medical Image", use_container_width=True)
    
    # Add predict button
    if st.button("🔮 Analyze Image", type="primary"):
        with st.spinner("🔬 Analyzing image..."):
            try:
                logger.info(f"Starting image analysis for file: {uploaded_file.name}")
                
                # Preprocess the image
                processed_image = preprocess_image(uploaded_file)
                logger.info("Image preprocessing completed successfully")
                
                # Make prediction
                prediction = model.predict(processed_image, verbose=0)[0][0]
                logger.info(f"Prediction completed: {prediction:.4f}")
                
                # Determine label (threshold at 0.5)
                predicted_class = 1 if prediction >= 0.5 else 0
                label = "Malignant (Cancerous)" if predicted_class == 1 else "Benign (Non-Cancerous)"
                
                logger.info(f"Classification: {label} (Class: {predicted_class})")
                
                # Display results
                st.subheader("🔬 Analysis Results")
                
                # Create columns for better layout
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Prediction", label)
                    st.metric("Class", f"{predicted_class}")
                
                with col2:
                    st.metric("Confidence Score", f"{prediction:.4f}")
                    confidence_pct = prediction * 100 if predicted_class == 1 else (1 - prediction) * 100
                    st.metric("Confidence %", f"{confidence_pct:.2f}%")
                
                # Risk assessment with color coding
                st.markdown("---")
                st.subheader("⚕️ Clinical Recommendation")
                
                if predicted_class == 1:  # Malignant
                    if prediction >= 0.75:
                        st.error("🚨 **HIGH RISK MALIGNANT** - Immediate specialist consultation and biopsy recommended")
                    else:
                        st.warning("⚠️ **MODERATE RISK MALIGNANT** - Further diagnostic tests and specialist review advised")
                else:  # Benign
                    if prediction <= 0.25:
                        st.success("✅ **LOW RISK BENIGN** - Routine monitoring recommended")
                    else:
                        st.info("ℹ️ **BORDERLINE BENIGN** - Follow-up imaging in 6-12 months advised")
                
                # Grad-CAM Visualization
                st.markdown("---")
                st.subheader("🔍 Model Attention Map (Grad-CAM)")
                st.write("This heatmap shows which regions of the image the AI model focused on when making its prediction.")
                
                try:
                    # Find the last convolutional layer
                    conv_layers = [layer.name for layer in model.layers if 'depthwise_separable_conv' in layer.name.lower() or 'conv' in layer.name.lower()]
                    
                    if conv_layers:
                        last_conv_name = conv_layers[-1]
                        logger.info(f"Using layer '{last_conv_name}' for Grad-CAM")
                        
                        # Generate heatmap
                        heatmap = make_gradcam_heatmap(processed_image, model, last_conv_name)
                        
                        # Prepare original image for visualization
                        original_img = np.array(image.resize((224, 224)))
                        if original_img.max() > 1:
                            original_img = original_img / 255.0
                        
                        # Resize heatmap to match image size (cv2.resize expects (width, height))
                        heatmap_resized = cv2.resize(heatmap, dsize=(224, 224), interpolation=cv2.INTER_LINEAR)
                        
                        # Create Grad-CAM overlay
                        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
                        
                        # Original image
                        axes[0].imshow(original_img)
                        axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
                        axes[0].axis('off')
                        
                        # Heatmap only
                        axes[1].imshow(heatmap_resized, cmap='jet')
                        axes[1].set_title('Attention Heatmap', fontsize=12, fontweight='bold')
                        axes[1].axis('off')
                        
                        # Overlay
                        axes[2].imshow(original_img)
                        axes[2].imshow(heatmap_resized, alpha=0.4, cmap='jet')
                        axes[2].set_title(f'Grad-CAM Overlay ({label})', fontsize=12, fontweight='bold')
                        axes[2].axis('off')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)
                        
                        st.info("💡 **Interpretation:** Red/yellow areas indicate regions the model considers most important for its prediction. Blue areas are less relevant.")
                        logger.info("Grad-CAM visualization generated successfully")
                    else:
                        st.warning("⚠️ No convolutional layers found for Grad-CAM visualization")
                        logger.warning("No convolutional layers found in model")
                        
                except Exception as e:
                    logger.warning(f"Grad-CAM visualization failed: {str(e)}")
                    st.warning(f"⚠️ Could not generate attention map: {str(e)}")
                
                # Disclaimer
                st.markdown("---")
                st.caption("⚠️ **Medical Disclaimer:** This is an AI-assisted tool and should not replace professional medical diagnosis. Always consult with qualified healthcare providers for final diagnosis and treatment decisions.")
                
                # Download report functionality
                st.markdown("---")
                st.subheader("📥 Download Report")
                
                report_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": uploaded_file.name,
                    "prediction": {
                        "class": int(predicted_class),
                        "label": label,
                        "confidence_score": float(prediction),
                        "confidence_percentage": float(confidence_pct)
                    },
                    "risk_assessment": "High Risk" if prediction >= 0.75 else "Moderate Risk" if prediction >= 0.5 else "Borderline" if prediction >= 0.25 else "Low Risk",
                    "recommendation": "Immediate specialist consultation" if predicted_class == 1 and prediction >= 0.75 else "Further diagnostic tests advised" if predicted_class == 1 else "Follow-up imaging in 6-12 months" if prediction >= 0.25 else "Routine monitoring recommended"
                }
                
                report_json = json.dumps(report_data, indent=2)
                st.download_button(
                    label="📥 Download Prediction Report (JSON)",
                    data=report_json,
                    file_name=f"thyroid_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                logger.info(f"Analysis completed successfully for {uploaded_file.name}")
                
            except FileNotFoundError as e:
                logger.error(f"File not found error: {str(e)}")
                st.error(f"❌ File error: {str(e)}")
            except ValueError as e:
                logger.error(f"Value error during processing: {str(e)}")
                st.error(f"❌ Invalid image format: {str(e)}")
                st.error("Please ensure the image is a valid thyroid medical image in .png, .jpg, or .jpeg format.")
            except Exception as e:
                logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
                st.error(f"❌ Analysis failed: {str(e)}")
                st.error("Please ensure the image is a valid thyroid medical image in .png, .jpg, or .jpeg format.")
else:
    # Instructions when no file is uploaded
    st.info("👆 Please upload a thyroid medical image to begin analysis")
    
    # Add example information
    with st.expander("ℹ️ Supported Image Formats & Guidelines"):
        st.markdown("""
        **Accepted Formats:**
        - PNG (.png)
        - JPEG (.jpg, .jpeg)
        
        **Image Guidelines:**
        - Clear thyroid ultrasound images
        - Pathology slides of thyroid tissue
        - Minimum resolution: 224x224 pixels
        - Well-lit and properly focused images
        
        **Model Output:**
        - **0** → Benign (Non-cancerous)
        - **1** → Malignant (Cancerous)
        """)

