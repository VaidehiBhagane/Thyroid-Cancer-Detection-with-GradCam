/**
 * PredictionMetrics Component
 * Displays prediction results in metric cards
 */
import Card from '../UI/Card';
import { usePrediction } from '../../context/PredictionContext';

export default function PredictionMetrics() {
  const { predictionResult } = usePrediction();

  if (!predictionResult) {
    return null;
  }

  const { prediction } = predictionResult;
  const { class: predClass, label, confidence_score, confidence_percentage } = prediction;

  const metrics = [
    {
      label: 'Classification',
      value: label,
      description: 'AI Prediction Result'
    },
    {
      label: 'Class',
      value: predClass,
      description: '0 = Benign, 1 = Malignant'
    },
    {
      label: 'Confidence Score',
      value: confidence_score.toFixed(4),
      description: 'Model Confidence (0-1)'
    },
    {
      label: 'Confidence Percentage',
      value: `${confidence_percentage.toFixed(2)}%`,
      description: 'Percentage Confidence'
    }
  ];

  return (
    <div className="animate-slide-up">
      <Card>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          📊 Analysis Results
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {metrics.map((metric, index) => (
            <div
              key={index}
              className="metric-card"
            >
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                {metric.label}
              </p>
              <p className={`text-2xl font-bold mb-1 ${
                index === 0 
                  ? (predClass === 1 ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400')
                  : 'text-gray-900 dark:text-white'
              }`}>
                {metric.value}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-500">
                {metric.description}
              </p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
