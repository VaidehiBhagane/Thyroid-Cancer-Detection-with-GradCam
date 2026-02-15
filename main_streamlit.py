import streamlit as st
from PIL import Image
from datetime import datetime
import json, cv2, numpy as np, matplotlib.pyplot as plt, matplotlib
from utils.logger_config import configure_logging
from utils.processing import preprocess_image
from model.model_loader import load_model
from utils.gradcam import make_gradcam_heatmap

matplotlib.use('Agg')
logger = configure_logging()

try: model = load_model()
except Exception as e:
    logger.critical(f"Model init error: {e}")
    st.error("Failed to initialize. Check logs.")
    st.stop()

def show_results(cls, lbl, pred, conf_pct):
    st.subheader("🔬 Analysis Results")
    c1, c2 = st.columns(2)
    c1.metric("Prediction", lbl); c1.metric("Class", str(cls))
    c2.metric("Confidence Score", f"{pred:.4f}"); c2.metric("Confidence %", f"{conf_pct:.2f}%")
    st.markdown("---"); st.subheader("⚕️ Clinical Recommendation")
    for (c, t), (fn, msg) in {(1,.75):("error","🚨 **HIGH RISK** - Immediate specialist consultation"),
        (1,0):("warning","⚠️ **MODERATE RISK** - Further tests advised"),
        (0,.25):("success","✅ **LOW RISK** - Routine monitoring"),
        (0,0):("info","ℹ️ **BORDERLINE** - 6-12 month follow-up")}.items():
        if cls==c and (pred>=t if c else pred<=(1-t)): getattr(st,fn)(msg); break

def show_gradcam(proc, img, lbl):
    st.markdown("---"); st.subheader("🔍 Model Attention Map (Grad-CAM)")
    try:
        # Get only Conv2D layers (exclude custom layers like DepthwiseSeparableConv)
        cl = [l.name for l in model.layers if 'conv2d' in l.name.lower()]
        if not cl: 
            logger.warning("No Conv2D layers found for Grad-CAM")
            st.warning("⚠️ No suitable layers for attention map")
            return
        
        # Use the last Conv2D layer before the dense layers
        target_layer = cl[-1]
        logger.info(f"Using layer '{target_layer}' for Grad-CAM")
        
        orig = np.array(img.resize((224,224))); orig = orig/255 if orig.max()>1 else orig
        hm = cv2.resize(make_gradcam_heatmap(proc, model, target_layer), (224,224))
        fig, ax = plt.subplots(1,3,figsize=(15,5))
        for i, (a, t) in enumerate(zip(ax, ['Original','Heatmap',f'Overlay ({lbl})'])):
            a.imshow(orig if i!=1 else hm, cmap=None if i==0 else 'jet')
            if i==2: a.imshow(hm, alpha=0.4, cmap='jet')
            a.set_title(t, fontsize=12, fontweight='bold'); a.axis('off')
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)
        st.info("💡 Red/yellow=important, Blue=less relevant")
        logger.info("Grad-CAM generated successfully")
    except Exception as e: 
        logger.error(f"Grad-CAM failed: {e}", exc_info=True)
        st.warning(f"⚠️ Could not generate attention map: {str(e)}")

st.title("🦋 Thyroid Cancer Detection System")
st.write("Upload a thyroid medical image (ultrasound/pathology) for AI-powered cancer detection")
uploaded_file = st.file_uploader("📤 Choose image (.png, .jpg, .jpeg)", type=["png","jpg","jpeg"])

if uploaded_file:
    st.subheader("📸 Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption="Thyroid Medical Image", use_container_width=True)
    if st.button("🔮 Analyze Image", type="primary"):
        with st.spinner("🔬 Analyzing..."):
            try:
                logger.info(f"Analyzing: {uploaded_file.name}")
                proc = preprocess_image(uploaded_file)
                pred = float(model.predict(proc, verbose=0)[0][0])
                cls = 1 if pred>=0.5 else 0
                lbl = "Malignant (Cancerous)" if cls else "Benign (Non-Cancerous)"
                conf = pred*100 if cls else (1-pred)*100
                logger.info(f"Result: {lbl} ({pred:.4f})")
                show_results(cls, lbl, pred, conf)
                show_gradcam(proc, image, lbl)
                st.markdown("---")
                st.subheader("📥 Download Report")
                ri = 3 if pred>=0.75 else 2 if pred>=0.5 else 1 if pred>=0.25 else 0
                report = {"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "filename":uploaded_file.name,
                         "prediction":{"class":int(cls),"label":lbl,"confidence_score":float(pred),"confidence_percentage":float(conf)},
                         "risk_assessment":["Low Risk","Borderline","Moderate Risk","High Risk"][ri],
                         "recommendation":["Routine monitoring","6-12 month follow-up","Further tests","Immediate specialist consultation"][ri]}
                st.download_button("📥 Download JSON Report", json.dumps(report, indent=2),
                                 f"thyroid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")
                logger.info(f"Analysis completed: {uploaded_file.name}")
            except (FileNotFoundError, ValueError) as e: logger.error(f"Error: {e}"); st.error(f"❌ {type(e).__name__}: {e}")
            except Exception as e: logger.error(f"Analysis error: {e}", exc_info=True); st.error(f"❌ Analysis failed: {e}")
else:
    st.info("👆 Please upload an image to begin")
    with st.expander("ℹ️ Info & Guidelines"):
        st.markdown("**Formats:** PNG, JPEG | **Min size:** 224x224px | **Output:** 0=Benign, 1=Malignant")

