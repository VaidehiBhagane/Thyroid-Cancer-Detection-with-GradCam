/**
 * Card Component
 * Container wrapper with shadow and rounded corners
 */
export default function Card({ children, className = '', ...props }) {
  return (
    <div 
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors duration-300 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
