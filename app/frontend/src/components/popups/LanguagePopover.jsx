import React from 'react';
import { languages } from '../../utils/languages';
import { useClickOutside } from '../../hooks/useClickOutside';

/**
 * LanguagePopover Component - Dropdown for language selection
 * Features: Flag icons, language names, selection handling
 */
const LanguagePopover = ({ isOpen, onClose, selectedLanguage, onSelect }) => {
  const popoverRef = useClickOutside(onClose);

  if (!isOpen) return null;

  return (
    <div
      ref={popoverRef}
      className="absolute top-full right-0 mt-2 w-56 bg-white rounded-lg shadow-dropdown border border-gray-100 py-2 z-50 animate-scale-in"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="language-menu"
    >
      {languages.map((language) => (
        <button
          key={language.code}
          onClick={() => {
            onSelect(language);
            onClose();
          }}
          className={`w-full flex items-center px-4 py-3 text-sm hover:bg-gray-50 transition-colors ${
            selectedLanguage.code === language.code ? 'bg-white-50 text-gray-700' : 'text-gray-700'
          }`}
          role="menuitem"
        >
          <img
            src={language.flagSrc}
            alt={`${language.name} flag`}
            className="w-5 h-5 rounded-sm mr-3 object-cover"
            onError={(e) => {
              e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xMCA1TDE1IDEwTDEwIDE1TDUgMTBMMTAgNVoiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
            }}
          />
          <span className="font-medium">{language.name}</span>
          {selectedLanguage.code === language.code && (
            <svg className="w-4 h-4 ml-auto text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      ))}
    </div>
  );
};

export default LanguagePopover;
