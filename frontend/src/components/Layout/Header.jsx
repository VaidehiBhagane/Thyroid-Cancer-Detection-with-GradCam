/**
 * Header Component
 * Main application header with title and dark mode toggle
 */
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';
import { useTheme } from '../../context/ThemeContext';

export default function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <span className="text-4xl">🦋</span>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                Thyroid Cancer Detection System
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                AI-Powered Medical Image Analysis
              </p>
            </div>
          </div>
          
          {/* Dark Mode Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
            aria-label="Toggle dark mode"
          >
            {theme === 'light' ? (
              <MoonIcon className="h-6 w-6 text-gray-700 dark:text-gray-300" />
            ) : (
              <SunIcon className="h-6 w-6 text-yellow-500" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
