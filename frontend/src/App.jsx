import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from './context/ThemeContext';
import { PredictionProvider, usePrediction } from './context/PredictionContext';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Container from './components/Layout/Container';
import ImageUpload from './components/Upload/ImageUpload';
import ImagePreview from './components/Upload/ImagePreview';
import PredictionMetrics from './components/Results/PredictionMetrics';
import ClinicalAssessment from './components/Results/ClinicalAssessment';
import GradCAMPanel from './components/Visualization/GradCAMPanel';
import InterpretationGuide from './components/Visualization/InterpretationGuide';
import DownloadButtons from './components/Reports/DownloadButtons';
import LoadingSpinner from './components/UI/LoadingSpinner';

function MainContent() {
  const { uploadedImage, predictionResult, gradcamImages, isLoading } = usePrediction();

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        <Container>
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
          <div className="mb-8">
            <ImageUpload />
            <ImagePreview />
          </div>
          {isLoading && (
            <div className="my-12">
              <LoadingSpinner size="lg" message="🔬 Analyzing image... This may take a few seconds." />
            </div>
          )}
          {predictionResult && !isLoading && (
            <div className="space-y-8">
              <PredictionMetrics />
              <ClinicalAssessment />
              {gradcamImages && (
                <>
                  <GradCAMPanel />
                  <InterpretationGuide />
                </>
              )}
              <DownloadButtons />
            </div>
          )}
        </Container>
      </main>
      <Footer />
      <Toaster position="top-right" toastOptions={{
        duration: 4000,
        style: { background: 'var(--toast-bg)', color: 'var(--toast-color)' },
        success: { iconTheme: { primary: '#10B981', secondary: '#fff' } },
        error: { iconTheme: { primary: '#EF4444', secondary: '#fff' } }
      }} />
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <PredictionProvider>
        <MainContent />
      </PredictionProvider>
    </ThemeProvider>
  );
}
