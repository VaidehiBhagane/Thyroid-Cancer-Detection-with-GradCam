/**
 * Prediction Context Provider
 * Manages analysis state including image, prediction results, and Grad-CAM data
 */
import { createContext, useContext, useState } from 'react';

const PredictionContext = createContext();

export function PredictionProvider({ children }) {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [gradcamImages, setGradcamImages] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const resetAnalysis = () => {
    setUploadedImage(null);
    setPredictionResult(null);
    setGradcamImages(null);
    setIsLoading(false);
    setError(null);
  };

  const value = {
    uploadedImage,
    setUploadedImage,
    predictionResult,
    setPredictionResult,
    gradcamImages,
    setGradcamImages,
    isLoading,
    setIsLoading,
    error,
    setError,
    resetAnalysis
  };

  return (
    <PredictionContext.Provider value={value}>
      {children}
    </PredictionContext.Provider>
  );
}

export function usePrediction() {
  const context = useContext(PredictionContext);
  if (context === undefined) {
    throw new Error('usePrediction must be used within a PredictionProvider');
  }
  return context;
}
