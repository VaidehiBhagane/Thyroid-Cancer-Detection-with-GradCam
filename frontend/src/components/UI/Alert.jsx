/**
 * Alert Component
 * Displays alerts with different severity levels
 */
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon, 
  XCircleIcon 
} from '@heroicons/react/24/outline';

export default function Alert({ type = 'info', title, message, className = '' }) {
  const types = {
    success: {
      bg: 'bg-green-50 dark:bg-green-900/20',
      border: 'border-green-500',
      text: 'text-green-800 dark:text-green-300',
      icon: CheckCircleIcon,
      iconColor: 'text-green-600 dark:text-green-400'
    },
    warning: {
      bg: 'bg-orange-50 dark:bg-orange-900/20',
      border: 'border-orange-500',
      text: 'text-orange-800 dark:text-orange-300',
      icon: ExclamationTriangleIcon,
      iconColor: 'text-orange-600 dark:text-orange-400'
    },
    error: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      border: 'border-red-500',
      text: 'text-red-800 dark:text-red-300',
      icon: XCircleIcon,
      iconColor: 'text-red-600 dark:text-red-400'
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-500',
      text: 'text-blue-800 dark:text-blue-300',
      icon: InformationCircleIcon,
      iconColor: 'text-blue-600 dark:text-blue-400'
    }
  };

  const config = types[type];
  const Icon = config.icon;

  return (
    <div 
      className={`${config.bg} border-l-4 ${config.border} p-4 rounded-r-lg ${className}`}
      role="alert"
    >
      <div className="flex items-start">
        <Icon className={`h-6 w-6 ${config.iconColor} mr-3 flex-shrink-0`} />
        <div className="flex-1">
          {title && (
            <h3 className={`font-semibold ${config.text} mb-1`}>
              {title}
            </h3>
          )}
          {message && (
            <p className={`${config.text} text-sm`}>
              {message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
