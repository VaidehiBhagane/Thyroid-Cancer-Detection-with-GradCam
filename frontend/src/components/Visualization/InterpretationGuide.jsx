/**
 * InterpretationGuide Component
 * Explains how to interpret the Grad-CAM heatmap
 */
import { InformationCircleIcon } from '@heroicons/react/24/outline';

export default function InterpretationGuide() {
  return (
    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div className="flex items-start">
        <InformationCircleIcon className="h-6 w-6 text-blue-600 dark:text-blue-400 mr-3 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">
            💡 How to Interpret the Heatmap
          </h4>
          <div className="text-sm text-blue-800 dark:text-blue-300 space-y-1">
            <p>
              The color-coded heatmap shows which regions the AI model focused on when making its prediction:
            </p>
            <ul className="list-disc list-inside ml-2 space-y-1">
              <li><span className="font-semibold text-red-600 dark:text-red-400">Red/Yellow areas:</span> Regions of high importance (strong influence on prediction)</li>
              <li><span className="font-semibold text-green-600 dark:text-green-400">Green areas:</span> Moderate importance</li>
              <li><span className="font-semibold text-blue-600 dark:text-blue-400">Blue areas:</span> Low importance (minimal influence)</li>
            </ul>
            <p className="italic mt-2">
              The overlay combines the heatmap with the original image for easier interpretation.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
