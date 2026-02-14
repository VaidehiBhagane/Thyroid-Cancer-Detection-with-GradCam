# 🦋 Thyroid Cancer Detection System - React Frontend

Modern, responsive React frontend for the AI-powered thyroid cancer detection system.

## 📋 Features

- ✅ **Drag & Drop Upload** - Intuitive image upload interface
- ✅ **Real-time Analysis** - Get instant predictions from the AI model
- ✅ **Grad-CAM Visualization** - See model attention heatmaps
- ✅ **Risk Assessment** - Color-coded clinical recommendations
- ✅ **Report Downloads** - Export results as PDF or JSON
- ✅ **Dark Mode** - Full dark mode support with theme persistence
- ✅ **Responsive Design** - Works seamlessly on all devices
- ✅ **Accessibility** - WCAG AA compliant with screen reader support

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run preview
```

## 📚 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Layout/         # Header, Footer, Container
│   │   ├── Upload/         # Image upload & preview
│   │   ├── Results/        # Prediction metrics & assessment
│   │   ├── Visualization/  # Grad-CAM panels
│   │   ├── Reports/        # Download buttons
│   │   └── UI/             # Reusable UI components
│   ├── context/            # React Context providers
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API service layer
│   ├── utils/              # Helper functions
│   ├── styles/             # Global styles
│   ├── App.jsx             # Main app component
│   └── main.jsx            # Entry point
├── public/                 # Static assets
├── index.html              # HTML template
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # TailwindCSS configuration
└── README.md               # This file
```

## 🎨 Technology Stack

- **Build Tool:** Vite 5.x
- **Framework:** React 18.x
- **Styling:** TailwindCSS 3.x
- **State Management:** React Context API
- **HTTP Client:** Axios
- **File Upload:** react-dropzone
- **Icons:** Heroicons
- **Notifications:** react-hot-toast
- **UI Components:** Headless UI

## 🔌 API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`

### API Endpoints Used:

- `GET /api/v1/health` - Health check
- `GET /api/v1/model-info` - Model information
- `POST /api/v1/analyze` - Complete analysis (prediction + Grad-CAM)
- `POST /api/v1/report/pdf` - Download PDF report
- `POST /api/v1/report/json` - Download JSON report

### Request Format:

```javascript
{
  "image": "<base64_encoded_image>",
  "filename": "scan.jpg",
  "include_gradcam": true
}
```

## 🎯 Component Overview

### Core Components

- **ImageUpload** - Drag & drop file upload with validation
- **ImagePreview** - Display uploaded image with analysis trigger
- **PredictionMetrics** - Show prediction results in metric cards
- **ClinicalAssessment** - Risk assessment with color-coded alerts
- **GradCAMPanel** - Three-panel Grad-CAM visualization
- **DownloadButtons** - PDF and JSON report downloads
- **MedicalDisclaimer** - Important medical disclaimer

### Context Providers

- **ThemeContext** - Dark mode state management
- **PredictionContext** - Analysis state management

### Custom Hooks

- **useAnalysis** - Handles image analysis workflow

## 🎨 Styling & Theming

### Color Palette

```javascript
colors: {
  medical: {
    blue: '#0066CC',    // Primary
    green: '#10B981',   // Success/Benign
    orange: '#F59E0B',  // Warning/Moderate
    red: '#EF4444'      // Error/High Risk
  }
}
```

### Risk Color Coding

- 🟢 **Green** - Low Risk Benign (confidence ≤ 0.25)
- 🔵 **Blue** - Borderline Benign (0.25 < confidence < 0.5)
- 🟡 **Orange** - Moderate Risk Malignant (0.5 ≤ confidence < 0.75)
- 🔴 **Red** - High Risk Malignant (confidence ≥ 0.75)

## 📱 Responsive Breakpoints

- **Mobile:** < 640px
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

## 🔒 Security & Privacy

- No data is stored on the frontend
- All processing happens via API calls
- Images are converted to base64 in memory
- No cookies or tracking

## ⚠️ Error Handling

The app handles:
- Network errors
- File validation errors
- Size limit errors (10MB max)
- API timeout errors
- Invalid image format errors

## 🧪 Development

### Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

### Environment Variables

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📝 License

For research and educational purposes only. See main project README for full license information.

## 🙏 Acknowledgments

- Built with React + Vite
- Styled with TailwindCSS
- Icons by Heroicons
- Medical AI powered by TensorFlow

---

**Made with ❤️ for better healthcare through AI**
