/**
 * Footer Component
 * Application footer with version info
 */
export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center">
          <p className="text-xs text-gray-500 dark:text-gray-500">
            © {currentYear} Thyroid Cancer Detection System v2.0.0 | Made with ❤️ for better healthcare through AI
          </p>
        </div>
      </div>
    </footer>
  );
}
