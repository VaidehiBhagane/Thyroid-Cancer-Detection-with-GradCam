/**
 * ImageUpload Component
 * Drag & drop file upload with validation
 */
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { CloudArrowUpIcon, PhotoIcon } from '@heroicons/react/24/outline';
import { usePrediction } from '../../context/PredictionContext';
import { validateFile } from '../../utils/helpers';
import toast from 'react-hot-toast';

export default function ImageUpload() {
  const { uploadedImage, setUploadedImage, resetAnalysis } = usePrediction();

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file
    const validation = validateFile(file);
    if (!validation.valid) {
      toast.error(validation.error);
      return;
    }

    // Reset previous analysis
    resetAnalysis();
    
    // Set uploaded image
    setUploadedImage(file);
    toast.success('Image uploaded successfully!');
  }, [setUploadedImage, resetAnalysis]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  });

  if (uploadedImage) {
    return null; // Show ImagePreview instead
  }

  return (
    <div className="animate-fade-in">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-300
          ${isDragActive 
            ? 'border-medical-blue bg-blue-50 dark:bg-blue-900/20 scale-102' 
            : 'border-gray-300 dark:border-gray-600 hover:border-medical-blue dark:hover:border-medical-blue hover:bg-gray-50 dark:hover:bg-gray-800/50'
          }`}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {isDragActive ? (
            <>
              <CloudArrowUpIcon className="h-16 w-16 text-medical-blue animate-bounce" />
              <p className="text-lg font-semibold text-medical-blue">
                Drop your image here...
              </p>
            </>
          ) : (
            <>
              <PhotoIcon className="h-16 w-16 text-gray-400 dark:text-gray-500" />
              <div>
                <p className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Upload Thyroid Medical Image
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Drag & drop an image here, or click to browse
                </p>
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500 space-y-1">
                <p>Supported formats: PNG, JPG, JPEG</p>
                <p>Maximum size: 10MB</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
