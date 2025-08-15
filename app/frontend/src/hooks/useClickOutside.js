import { useEffect, useRef } from 'react';

/**
 * Custom hook to handle clicks outside of a referenced element
 * @param {Function} handler - Function to call when clicking outside
 * @returns {Object} ref - Ref to attach to the element
 */
export const useClickOutside = (handler) => {
  const ref = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        handler();
      }
    };

    const handleEscapeKey = (event) => {
      if (event.key === 'Escape') {
        handler();
      }
    };

    // Add event listeners
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscapeKey);

    // Cleanup event listeners
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [handler]);

  return ref;
};
