/**
 * ClinicalAssessment Component
 * Displays risk assessment and clinical recommendations
 */
import Alert from '../UI/Alert';
import { usePrediction } from '../../context/PredictionContext';
import { getRiskColor } from '../../utils/helpers';

export default function ClinicalAssessment() {
  const { predictionResult } = usePrediction();

  if (!predictionResult) {
    return null;
  }

  const { prediction, risk_assessment, recommendation } = predictionResult;
  const colors = getRiskColor(prediction.class, prediction.confidence_score);

  // Determine alert type based on risk
  let alertType = 'info';
  if (risk_assessment.includes('High Risk')) {
    alertType = 'error';
  } else if (risk_assessment.includes('Moderate Risk')) {
    alertType = 'warning';
  } else if (risk_assessment.includes('Low Risk')) {
    alertType = 'success';
  }

  return (
    <div className="animate-slide-up space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        ⚕️ Clinical Risk Assessment
      </h2>

      <div className={`${colors.bg} border-2 ${colors.border} rounded-lg p-6`}>
        <div className="mb-4">
          <span className={`inline-block px-4 py-2 rounded-full font-semibold ${colors.badge}`}>
            {risk_assessment}
          </span>
        </div>

        <div>
          <h3 className={`text-lg font-semibold ${colors.text} mb-2`}>
            Clinical Recommendation:
          </h3>
          <p className={`${colors.text}`}>
            {recommendation}
          </p>
        </div>
      </div>

      <Alert
        type={alertType}
        title="Important"
        message="This analysis should be reviewed by qualified healthcare professionals. Never make medical decisions based solely on AI predictions."
      />
    </div>
  );
}
