/**
 * Utility helper functions
 */

/**
 * File validation constants
 */
export const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/jpg'];
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

/**
 * Validate uploaded file
 * @param {File} file - File to validate
 * @returns {Object} Validation result with valid flag and error message
 */
export function validateFile(file) {
  if (!file) {
    return { valid: false, error: 'No file provided' };
  }

  if (!ALLOWED_TYPES.includes(file.type)) {
    return { 
      valid: false, 
      error: 'Invalid file type. Please upload PNG, JPG, or JPEG.' 
    };
  }

  if (file.size > MAX_FILE_SIZE) {
    return { 
      valid: false, 
      error: 'File too large. Maximum size is 10MB.' 
    };
  }

  return { valid: true };
}

/**
 * Format file size to human-readable string
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted size string
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Get risk color based on prediction
 * @param {number} predictionClass - 0 (benign) or 1 (malignant)
 * @param {number} confidenceScore - Confidence score (0-1)
 * @returns {Object} Color configuration for UI
 */
export function getRiskColor(predictionClass, confidenceScore) {
  if (predictionClass === 1) {
    // Malignant
    if (confidenceScore >= 0.75) {
      return {
        bg: 'bg-red-50 dark:bg-red-900/20',
        border: 'border-red-500',
        text: 'text-red-700 dark:text-red-400',
        icon: 'text-red-600',
        badge: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
      };
    } else {
      return {
        bg: 'bg-orange-50 dark:bg-orange-900/20',
        border: 'border-orange-500',
        text: 'text-orange-700 dark:text-orange-400',
        icon: 'text-orange-600',
        badge: 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200'
      };
    }
  } else {
    // Benign
    if (confidenceScore <= 0.25) {
      return {
        bg: 'bg-green-50 dark:bg-green-900/20',
        border: 'border-green-500',
        text: 'text-green-700 dark:text-green-400',
        icon: 'text-green-600',
        badge: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
      };
    } else {
      return {
        bg: 'bg-blue-50 dark:bg-blue-900/20',
        border: 'border-blue-500',
        text: 'text-blue-700 dark:text-blue-400',
        icon: 'text-blue-600',
        badge: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
      };
    }
  }
}

/**
 * Download blob as file
 * @param {Blob} blob - File blob
 * @param {string} filename - Filename for download
 */
export function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

/**
 * Generate timestamped filename
 * @param {string} prefix - Filename prefix
 * @param {string} extension - File extension
 * @returns {string} Timestamped filename
 */
export function generateTimestampedFilename(prefix, extension) {
  const now = new Date();
  const timestamp = now.toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .slice(0, 19);
  return `${prefix}_${timestamp}.${extension}`;
}
