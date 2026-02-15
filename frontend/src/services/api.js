import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' }
});

export const fileToBase64 = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => resolve(reader.result.split(',')[1]);
  reader.onerror = reject;
});

const apiCall = async (method, endpoint, data = null, config = {}) => {
  try {
    const response = await apiClient[method](endpoint, data, config);
    return response.data;
  } catch (error) {
    console.error(`API call failed (${endpoint}):`, error);
    throw error;
  }
};

const prepareImageRequest = async (imageFile, includeGradcam) => ({
  image: await fileToBase64(imageFile),
  filename: imageFile.name,
  ...(includeGradcam !== undefined && { include_gradcam: includeGradcam })
});

export const checkHealth = () => apiCall('get', '/api/v1/health');
export const getModelInfo = () => apiCall('get', '/api/v1/model-info');

export const predictImage = async (imageFile) => 
  apiCall('post', '/api/v1/predict', await prepareImageRequest(imageFile));

export const generateGradCAM = async (imageFile) => 
  apiCall('post', '/api/v1/gradcam', await prepareImageRequest(imageFile));

export const analyzeImage = async (imageFile, includeGradcam = true) => 
  apiCall('post', '/api/v1/analyze', await prepareImageRequest(imageFile, includeGradcam));

export const downloadPDFReport = async (imageFile, includeGradcam = true) => 
  apiCall('post', '/api/v1/report/pdf', await prepareImageRequest(imageFile, includeGradcam), { responseType: 'blob' });

export const downloadJSONReport = async (imageFile, includeGradcam = true) => 
  apiCall('post', '/api/v1/report/json', await prepareImageRequest(imageFile, includeGradcam), { responseType: 'blob' });

export default {
  checkHealth, getModelInfo, predictImage, generateGradCAM,
  analyzeImage, downloadPDFReport, downloadJSONReport
};
