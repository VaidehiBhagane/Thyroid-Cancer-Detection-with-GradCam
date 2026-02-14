/**
 * Loading Spinner Component
 * Shows loading state with optional message
 */
export default function LoadingSpinner({ size = 'md', message = 'Loading...' }) {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16'
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className="relative">
        <div className={`${sizes[size]} border-4 border-medical-blue border-t-transparent rounded-full animate-spin`}></div>
      </div>
      {message && (
        <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
          {message}
        </p>
      )}
    </div>
  );
}
