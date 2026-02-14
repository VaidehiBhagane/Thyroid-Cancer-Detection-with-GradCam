/**
 * GradCAMPanel Component
 * Three-panel display of Grad-CAM visualization
 */
import { usePrediction } from '../../context/PredictionContext';

export default function GradCAMPanel() {
  const { gradcamImages, predictionResult } = usePrediction();

  if (!gradcamImages || !gradcamImages.images) {
    return null;
  }

  const { images, layer_used } = gradcamImages;
  const { original, heatmap, overlay } = images;
  const predictionLabel = predictionResult?.prediction?.label || 'N/A';

  const panels = [
    {
      title: 'Original Image',
      description: 'Input medical image',
      image: original
    },
    {
      title: 'Attention Heatmap',
      description: 'Model focus regions',
      image: heatmap
    },
    {
      title: 'Grad-CAM Overlay',
      description: `Heatmap on original (${predictionLabel})`,
      image: overlay
    }
  ];

  return (
    <div className="animate-slide-up">
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          🔍 Model Attention Visualization (Grad-CAM)
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Layer used: <span className="font-mono font-semibold">{layer_used}</span>
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {panels.map((panel, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
          >
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {panel.title}
              </h3>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                {panel.description}
              </p>
            </div>
            <div className="p-4 bg-gray-50 dark:bg-gray-900">
              <img
                src={`data:image/png;base64,${panel.image}`}
                alt={panel.title}
                className="w-full h-auto rounded-lg shadow-sm"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
