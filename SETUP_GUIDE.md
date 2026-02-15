# 🚀 Complete Setup Guide - Thyroid Cancer Detection System

## Full Stack Setup: FastAPI Backend + React Frontend

This guide will help you set up and run both the backend and frontend applications.

---

## 📋 Prerequisites

### System Requirements:
- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **4GB+ RAM** recommended
- **Windows/macOS/Linux**

### Check Installation:
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

---

## 🔧 Backend Setup (FastAPI)

### Step 1: Navigate to Project Directory

```bash
cd "e:\thyroid with gradcam\thyroid_cancer"
```

### Step 2: Create & Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- TensorFlow (ML model)
- HuggingFace Hub (model download)
- Uvicorn (ASGI server)
- ReportLab (PDF generation)
- OpenCV, Pillow (image processing)
- And more...

### Step 4: Start the Backend Server

**Note:** The model will be automatically downloaded from HuggingFace on first startup.

```bash
python app.py
```

**Or using uvicorn directly:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be available at:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Step 6: Test Backend (Optional)

In a **new terminal** (keep backend running):

```bash
# Activate venv first
venv\Scripts\activate

# Run test script
python test_api.py
```

---

## 🎨 Frontend Setup (React + Vite)

### Step 1: Navigate to Frontend Directory

**Open a NEW terminal** (keep backend running in the first one!)

```bash
cd "e:\thyroid with gradcam\thyroid_cancer\frontend"
```

### Step 2: Install Frontend Dependencies

```bash
npm install
```

This installs:
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- Axios (HTTP client)
- React Dropzone (file upload)
- Heroicons (icons)
- React Hot Toast (notifications)
- And more...

**⏰ This may take 2-5 minutes depending on your internet speed.**

### Step 3: Start the Development Server

```bash
npm run dev
```

**Frontend will be available at:**
- App: http://localhost:3000

---

## ✅ Verify Everything is Working

### 1. Backend Health Check

Open browser: http://localhost:8000/api/v1/health

Should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-02-13 10:30:45",
  "version": "2.0.0"
}
```

### 2. Frontend Loading

Open browser: http://localhost:3000

Should see:
- 🦋 Thyroid Cancer Detection System
- Upload area
- Dark mode toggle

### 3. Test Complete Workflow

1. Upload a thyroid image (PNG/JPG/JPEG, max 10MB)
2. Click "🔮 Analyze Image"
3. Wait 3-5 seconds for analysis
4. View prediction results
5. See Grad-CAM visualization
6. Download PDF or JSON report

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `Module not found` error
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Problem:** `Port 8000 already in use`
```bash
# Solution: Kill the process or use different port
uvicorn app:app --port 8001 --reload
```

**Problem:** `Model file not found` or `Failed to download model`
```bash
# Solution 1: Check internet connection
# Solution 2: Clear model cache and restart
# The model will be automatically downloaded from HuggingFace:
# Repository: vaidehibh/fibonacci_cnn
```

**Problem:** `ImportError: cannot import name 'generate_pdf_report'`
```bash
# Solution: Restart the backend server
```

### Frontend Issues

**Problem:** `npm install` fails
```bash
# Solution: Clear cache and retry
npm cache clean --force
npm install
```

**Problem:** `Port 3000 already in use`
```bash
# Vite will automatically suggest another port (3001, 3002, etc.)
# Or manually specify:
npm run dev -- --port 3001
```

**Problem:** Can't connect to backend
```bash
# Solution: Make sure backend is running on port 8000
# Check: http://localhost:8000/api/v1/health
```

**Problem:** CORS errors
```bash
# Solution: Backend already has CORS enabled
# If still having issues, check app.py CORS configuration
```

### Image Upload Issues

**Problem:** File validation error
- Supported formats: PNG, JPG, JPEG only
- Maximum size: 10MB
- Ensure image is not corrupted

**Problem:** Analysis takes too long
- Normal analysis: 3-5 seconds
- If > 30 seconds: Check backend logs for errors

---

## 📦 Project Structure Overview

```
thyroid_cancer/
├── backend (FastAPI)
│   ├── app.py                 # Main FastAPI app
│   ├── config.py             # Configuration settings
│   ├── api/
│   │   ├── routes.py         # API endpoints
│   │   └── schemas.py        # Pydantic models
│   ├── model/
│   │   └── model_loader.py   # ML model loader from HuggingFace
│   ├── model_cache/          # Downloaded model cache
│   ├── utils/
│   │   ├── gradcam.py        # Grad-CAM generation
│   │   ├── pdf_generator.py # PDF report generation
│   │   └── image_utils.py    # Image processing
│   └── requirements.txt      # Python dependencies
│
└── frontend/ (React + Vite)
    ├── src/
    │   ├── components/       # React components
    │   ├── context/         # State management
    │   ├── services/        # API calls
    │   ├── hooks/           # Custom hooks
    │   ├── utils/           # Helper functions
    │   └── App.jsx          # Main app
    ├── package.json         # NPM dependencies
    └── vite.config.js       # Vite configuration
```

---

## 🎯 Common Development Workflow

### Terminal 1: Backend
```bash
cd "e:\thyroid with gradcam\thyroid_cancer"
venv\Scripts\activate
python app.py
```

### Terminal 2: Frontend
```bash
cd "e:\thyroid with gradcam\thyroid_cancer\frontend"
npm run dev
```

### Making Changes

**Backend Changes:**
- Edit Python files
- Server auto-reloads (if using `--reload`)
- Check http://localhost:8000/docs for API changes

**Frontend Changes:**
- Edit JSX/JS files
- Vite hot-reloads instantly
- Changes appear immediately in browser

---

## 📝 API Endpoints Reference

### Health & Info
- `GET /api/v1/health` - Server status
- `GET /api/v1/model-info` - Model details

### Analysis
- `POST /api/v1/predict` - Basic prediction
- `POST /api/v1/gradcam` - Grad-CAM visualization
- `POST /api/v1/analyze` - Complete analysis (recommended)

### Reports
- `POST /api/v1/report/pdf` - Download PDF report
- `POST /api/v1/report/json` - Download JSON report

**All POST endpoints accept JSON with base64 encoded images.**

---

## 🚀 Production Build

### Backend Production
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Production
```bash
cd frontend
npm run build
npm run preview
```

---

## 🎉 Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Backend health check returns `"status": "healthy"`
- [ ] Frontend running on http://localhost:3000
- [ ] Can upload image successfully
- [ ] Analysis completes and shows results
- [ ] Grad-CAM visualization displays
- [ ] Can download PDF report
- [ ] Can download JSON report
- [ ] Dark mode toggle works

---

## 📞 Need Help?

1. **Check Logs:**
   - Backend: Terminal output + `logs/app.log`
   - Frontend: Browser console (F12)

2. **Documentation:**
   - Backend: http://localhost:8000/docs
   - Frontend: `frontend/README.md`

3. **Test API:**
   - Use Swagger UI at http://localhost:8000/docs
   - Or run `python test_api.py`

---

## 🎊 You're All Set!

Both backend and frontend should now be running. Visit http://localhost:3000 to start analyzing thyroid images!

**Happy Coding! 🚀🦋**
