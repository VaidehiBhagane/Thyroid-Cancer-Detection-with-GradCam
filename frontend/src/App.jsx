/**
 * Main Application Component
 * Orchestrates all components and manages the application flow
 */
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from './context/ThemeContext';
import { PredictionProvider, usePrediction } from './context/PredictionContext';

// Layout components
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Container from './components/Layout/Container';

// Upload components
import ImageUpload from './components/Upload/ImageUpload';
import ImagePreview from './components/Upload/ImagePreview';

// Results components
import PredictionMetrics from './components/Results/PredictionMetrics';
import ClinicalAssessment from './components/Results/ClinicalAssessment';
import MedicalDisclaimer from './components/Results/MedicalDisclaimer';

// Visualization components
import GradCAMPanel from './components/Visualization/GradCAMPanel';
import InterpretationGuide from './components/Visualization/InterpretationGuide';

// Reports component
import DownloadButtons from './components/Reports/DownloadButtons';

// UI components
import LoadingSpinner from './components/UI/LoadingSpinner';

function MainContent() {
  const { uploadedImage, predictionResult, gradcamImages, isLoading } = usePrediction();

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-grow">
        <Container>
          {/* Instructions */}
          {!uploadedImage && (
            <div className="mb-8 text-center animate-fade-in">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
                Upload a Thyroid Medical Image
              </h2>
              <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Upload a thyroid ultrasound or pathology image for AI-powered analysis. 
                The system will classify the image as benign or malignant and provide clinical recommendations.
              </p>
            </div>
          )}

          {/* Upload Section */}
          <div className="mb-8">
            <ImageUpload />
            <ImagePreview />
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="my-12">
              <LoadingSpinner size="lg" message="🔬 Analyzing image... This may take a few seconds." />
            </div>
          )}

          {/* Results Section */}
          {predictionResult && !isLoading && (
            <div className="space-y-8">
              {/* Prediction Metrics */}
              <PredictionMetrics />

              {/* Clinical Assessment */}
              <ClinicalAssessment />

              {/* Grad-CAM Visualization */}
              {gradcamImages && (
                <>
                  <GradCAMPanel />
                  <InterpretationGuide />
                </>
              )}

              {/* Download Reports */}
              <DownloadButtons />

              {/* Medical Disclaimer */}
              <MedicalDisclaimer />
            </div>
          )}
        </Container>
      </main>

      <Footer />

      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--toast-bg)',
            color: 'var(--toast-color)',
          },
          success: {
            iconTheme: {
              primary: '#10B981',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#EF4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <PredictionProvider>
        <MainContent />
      </PredictionProvider>
    </ThemeProvider>
  );
}

export default App;
