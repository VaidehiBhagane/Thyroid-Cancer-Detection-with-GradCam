/**
 * ImagePreview Component
 * Shows uploaded image with option to remove and analyze
 */
import { XMarkIcon } from '@heroicons/react/24/outline';
import { usePrediction } from '../../context/PredictionContext';
import { useAnalysis } from '../../hooks/useAnalysis';
import Button from '../UI/Button';
import { formatFileSize } from '../../utils/helpers';

export default function ImagePreview() {
  const { uploadedImage, resetAnalysis, isLoading } = usePrediction();
  const { performAnalysis } = useAnalysis();

  if (!uploadedImage) {
    return null;
  }

  const imageUrl = URL.createObjectURL(uploadedImage);

  return (
    <div className="animate-slide-up">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Uploaded Image
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {uploadedImage.name} ({formatFileSize(uploadedImage.size)})
            </p>
          </div>
          <button
            onClick={resetAnalysis}
            disabled={isLoading}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200 disabled:opacity-50"
            aria-label="Remove image"
          >
            <XMarkIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        <div className="mb-6">
          <img
            src={imageUrl}
            alt="Uploaded thyroid scan"
            className="w-full max-w-md mx-auto rounded-lg shadow-md"
          />
        </div>

        <div className="flex justify-center">
          <Button
            variant="primary"
            size="lg"
            onClick={performAnalysis}
            disabled={isLoading}
            loading={isLoading}
            className="w-full sm:w-auto"
          >
            {isLoading ? 'Analyzing...' : '🔮 Analyze Image'}
          </Button>
        </div>
      </div>
    </div>
  );
}
