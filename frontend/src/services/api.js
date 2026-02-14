/**
 * API Service Layer for Thyroid Cancer Detection System
 * Handles all API calls to the FastAPI backend
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for  analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Convert image file to base64 string
 * @param {File} file - Image file to convert
 * @returns {Promise<string>} Base64 encoded string
 */
export const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      // Remove data URL prefix (data:image/jpeg;base64,)
      const base64 = reader.result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = (error) => reject(error);
  });
};

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/api/v1/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

/**
 * Get model information
 * @returns {Promise<Object>} Model details
 */
export const getModelInfo = async () => {
  try {
    const response = await apiClient.get('/api/v1/model-info');
    return response.data;
  } catch (error) {
    console.error('Failed to get model info:', error);
    throw error;
  }
};

/**
 * Predict cancer from image (basic prediction only)
 * @param {File} imageFile - Image file to analyze
 * @returns {Promise<Object>} Prediction results
 */
export const predictImage = async (imageFile) => {
  try {
    const base64Image = await fileToBase64(imageFile);
    
    const response = await apiClient.post('/api/v1/predict', {
      image: base64Image,
      filename: imageFile.name
    });
    
    return response.data;
  } catch (error) {
    console.error('Prediction failed:', error);
    throw error;
  }
};

/**
 * Generate Grad-CAM visualization
 * @param {File} imageFile - Image file to analyze
 * @returns {Promise<Object>} Grad-CAM images (original, heatmap, overlay)
 */
export const generateGradCAM = async (imageFile) => {
  try {
    const base64Image = await fileToBase64(imageFile);
    
    const response = await apiClient.post('/api/v1/gradcam', {
      image: base64Image,
      filename: imageFile.name
    });
    
    return response.data;
  } catch (error) {
    console.error('Grad-CAM generation failed:', error);
    throw error;
  }
};

/**
 * Complete analysis (prediction + Grad-CAM)
 * @param {File} imageFile - Image file to analyze
 * @param {boolean} includeGradcam - Whether to include Grad-CAM visualization
 * @returns {Promise<Object>} Complete analysis results
 */
export const analyzeImage = async (imageFile, includeGradcam = true) => {
  try {
    const base64Image = await fileToBase64(imageFile);
    
    const response = await apiClient.post('/api/v1/analyze', {
      image: base64Image,
      filename: imageFile.name,
      include_gradcam: includeGradcam
    });
    
    return response.data;
  } catch (error) {
    console.error('Complete analysis failed:', error);
    throw error;
  }
};

/**
 * Download PDF report
 * @param {File} imageFile - Image file used for analysis
 * @param {boolean} includeGradcam - Whether to include Grad-CAM
 * @returns {Promise<Blob>} PDF file blob
 */
export const downloadPDFReport = async (imageFile, includeGradcam = true) => {
  try {
    const base64Image = await fileToBase64(imageFile);
    
    const response = await apiClient.post('/api/v1/report/pdf', {
      image: base64Image,
      filename: imageFile.name,
      include_gradcam: includeGradcam
    }, {
      responseType: 'blob'
    });
    
    return response.data;
  } catch (error) {
    console.error('PDF download failed:', error);
    throw error;
  }
};

/**
 * Download JSON report
 * @param {File} imageFile - Image file used for analysis
 * @param {boolean} includeGradcam - Whether to include Grad-CAM
 * @returns {Promise<Blob>} JSON file blob
 */
export const downloadJSONReport = async (imageFile, includeGradcam = true) => {
  try {
    const base64Image = await fileToBase64(imageFile);
    
    const response = await apiClient.post('/api/v1/report/json', {
      image: base64Image,
      filename: imageFile.name,
      include_gradcam: includeGradcam
    }, {
      responseType: 'blob'
    });
    
    return response.data;
  } catch (error) {
    console.error('JSON download failed:', error);
    throw error;
  }
};

export default {
  checkHealth,
  getModelInfo,
  predictImage,
  generateGradCAM,
  analyzeImage,
  downloadPDFReport,
  downloadJSONReport
};
