/**
 * MedicalDisclaimer Component
 * Displays important medical disclaimer
 */
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

export default function MedicalDisclaimer() {
  return (
    <div className="bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-400 dark:border-yellow-600 rounded-lg p-6">
      <div className="flex items-start">
        <ExclamationTriangleIcon className="h-8 w-8 text-yellow-600 dark:text-yellow-400 mr-4 flex-shrink-0" />
        <div>
          <h3 className="text-lg font-bold text-yellow-900 dark:text-yellow-200 mb-2">
            ⚠️ Medical Disclaimer
          </h3>
          <div className="text-sm text-yellow-800 dark:text-yellow-300 space-y-2">
            <p>
              <strong>IMPORTANT:</strong> This is an AI-assisted tool for <strong>research and educational purposes only</strong>.
            </p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>❌ NOT a substitute for professional medical diagnosis</li>
              <li>❌ NOT FDA-approved or clinically validated</li>
              <li>❌ Should NOT be used for clinical decision-making</li>
            </ul>
            <p className="font-semibold">
              Always consult qualified healthcare professionals for definitive diagnosis, treatment planning, and medical advice.
            </p>
            <p className="text-xs italic">
              The developers assume no liability for medical decisions made using this tool.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
