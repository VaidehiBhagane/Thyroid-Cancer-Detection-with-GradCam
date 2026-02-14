/**
 * DownloadButtons Component
 * Buttons to download PDF and JSON reports
 */
import { useState } from 'react';
import { ArrowDownTrayIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import Button from '../UI/Button';
import { usePrediction } from '../../context/PredictionContext';
import { downloadPDFReport, downloadJSONReport } from '../../services/api';
import { downloadBlob, generateTimestampedFilename } from '../../utils/helpers';
import toast from 'react-hot-toast';

export default function DownloadButtons() {
  const { uploadedImage, predictionResult } = usePrediction();
  const [loadingPDF, setLoadingPDF] = useState(false);
  const [loadingJSON, setLoadingJSON] = useState(false);

  if (!predictionResult || !uploadedImage) {
    return null;
  }

  const handleDownloadPDF = async () => {
    setLoadingPDF(true);
    try {
      const blob = await downloadPDFReport(uploadedImage, true);
      const filename = generateTimestampedFilename('thyroid_analysis', 'pdf');
      downloadBlob(blob, filename);
      toast.success('PDF report downloaded successfully!');
    } catch (error) {
      console.error('PDF download error:', error);
      toast.error('Failed to download PDF report');
    } finally {
      setLoadingPDF(false);
    }
  };

  const handleDownloadJSON = async () => {
    setLoadingJSON(true);
    try {
      const blob = await downloadJSONReport(uploadedImage, true);
      const filename = generateTimestampedFilename('thyroid_analysis', 'json');
      downloadBlob(blob, filename);
      toast.success('JSON report downloaded successfully!');
    } catch (error) {
      console.error('JSON download error:', error);
      toast.error('Failed to download JSON report');
    } finally {
      setLoadingJSON(false);
    }
  };

  return (
    <div className="animate-slide-up">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          📥 Download Report
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Download a comprehensive analysis report in your preferred format.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Button
            variant="primary"
            size="lg"
            onClick={handleDownloadPDF}
            disabled={loadingPDF || loadingJSON}
            loading={loadingPDF}
            className="flex-1"
          >
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            Download PDF Report
          </Button>

          <Button
            variant="secondary"
            size="lg"
            onClick={handleDownloadJSON}
            disabled={loadingPDF || loadingJSON}
            loading={loadingJSON}
            className="flex-1"
          >
            <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
            Download JSON Report
          </Button>
        </div>

        <p className="text-xs text-gray-500 dark:text-gray-500 mt-4 text-center">
          Reports include prediction results, risk assessment, and Grad-CAM visualization
        </p>
      </div>
    </div>
  );
}
