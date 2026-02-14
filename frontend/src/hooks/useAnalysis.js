/**
 * Custom hook for image analysis
 * Handles the complete analysis workflow
 */
import { useState } from 'react';
import { analyzeImage } from '../services/api';
import { usePrediction } from '../context/PredictionContext';
import toast from 'react-hot-toast';

export function useAnalysis() {
  const {
    uploadedImage,
    setPredictionResult,
    setGradcamImages,
    setIsLoading,
    setError
  } = usePrediction();

  const performAnalysis = async () => {
    if (!uploadedImage) {
      toast.error('Please upload an image first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Show loading toast
      const loadingToast = toast.loading('Analyzing image...');

      // Perform complete analysis
      const result = await analyzeImage(uploadedImage, true);

      // Update state with results
      setPredictionResult(result);
      
      // Extract Grad-CAM data if available
      if (result.gradcam) {
        setGradcamImages(result.gradcam);
      }

      // Dismiss loading toast and show success
      toast.dismiss(loadingToast);
      toast.success('Analysis completed successfully!');

    } catch (err) {
      console.error('Analysis error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Analysis failed';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return { performAnalysis };
}
