import React from 'react';
import { currencies } from '../../utils/currencies';
import { useClickOutside } from '../../hooks/useClickOutside';

/**
 * CurrencyPopover Component - Dropdown for currency selection
 * Features: Currency codes, symbols, names, selection handling
 */
const CurrencyPopover = ({ isOpen, onClose, selectedCurrency, onSelect }) => {
  const popoverRef = useClickOutside(onClose);

  if (!isOpen) return null;

  return (
    <div
      ref={popoverRef}
      className="absolute top-full right-0 mt-2 w-48 bg-white rounded-lg shadow-dropdown border border-gray-100 py-2 z-50 animate-scale-in"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="currency-menu"
    >
      {currencies.map((currency) => (
        <button
          key={currency.code}
          onClick={() => {
            onSelect(currency);
            onClose();
          }}
          className={`w-full flex items-center justify-between px-4 py-3 text-sm hover:bg-gray-50 transition-colors ${
            selectedCurrency.code === currency.code ? 'bg-blue-50 text-blue-700' : 'text-gray-700'
          }`}
          role="menuitem"
        >
          <div className="flex items-center">
            <span className="font-medium mr-2">{currency.symbol}</span>
            <span>{currency.code}</span>
          </div>
          <span className="text-xs text-gray-500">{currency.name}</span>
          {selectedCurrency.code === currency.code && (
            <svg className="w-4 h-4 ml-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      ))}
    </div>
  );
};

export default CurrencyPopover;
