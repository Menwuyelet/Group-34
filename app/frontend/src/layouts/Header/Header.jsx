/**
 * GuzoMate Header Component
 * 
 * USAGE:
 * import Header from './layouts/Header/Header';
 * <Header onSearch={handleSearch} onLogin={handleLogin} onRegister={handleRegister} />
 * 
 * FEATURES:
 * - Responsive design (desktop-first)
 * - Search dropdown with location, dates, guests/rooms
 * - Language and currency selection
 * - Authentication modals
 * - Keyboard navigation and accessibility
 * 
 * SAMPLE SEARCH PAYLOAD:
 * {
 *   location: "Addis Ababa",
 *   dates: { checkIn: "2024-03-15", checkOut: "2024-03-18" },
 *   guests: { adults: 2, children: 0, rooms: 1 },
 *   language: { code: "en", name: "English" },
 *   currency: { code: "USD", symbol: "$" },
 *   timestamp: "2024-03-10T10:30:00.000Z"
 * }
 */

import React, { useState } from 'react';
import SearchBar from '../../components/search/SearchBar';
import LanguagePopover from '../../components/popups/LanguagePopover';
import CurrencyPopover from '../../components/popups/CurrencyPopover';
import RegisterModal from '../../components/auth/RegisterModal';
import LoginModal from '../../components/auth/LoginModal';
import { defaultLanguage } from '../../utils/languages';
import { defaultCurrency } from '../../utils/currencies';

const Header = ({ onSearch, onLogin, onRegister }) => {
  // State management for all header interactions
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isLanguageOpen, setIsLanguageOpen] = useState(false);
  const [isCurrencyOpen, setIsCurrencyOpen] = useState(false);
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  
  const [selectedLanguage, setSelectedLanguage] = useState(defaultLanguage);
  const [selectedCurrency, setSelectedCurrency] = useState(defaultCurrency);

  // Enhanced search handler that includes language and currency context
  const handleSearch = (searchData) => {
    const enhancedPayload = {
      ...searchData,
      language: selectedLanguage,
      currency: selectedCurrency,
    };
    
    console.log('Search Payload:', enhancedPayload);
    onSearch?.(enhancedPayload);
  };

  // Authentication handlers
  const handleLogin = async (loginData) => {
    console.log('Login attempt:', loginData);
    await onLogin?.(loginData);
  };

  const handleRegister = async (registerData) => {
    console.log('Register attempt:', registerData);
    await onRegister?.(registerData);
  };

  // Modal switching handlers
  const switchToLogin = () => {
    setIsRegisterOpen(false);
    setIsLoginOpen(true);
  };

  const switchToRegister = () => {
    setIsLoginOpen(false);
    setIsRegisterOpen(true);
  };

  return (
    <>
      {/* Main Header */}
      <header className="fixed top-0 left-0 right-0 bg-gray-900 bg-opacity-80 backdrop-blur-sm w-full z-50">
        <div className="w-full px-4">
          <div className="flex items-center justify-between h-20">
            {/* Logo Section */}
            <div className="flex items-center space-x-3">
              <img
                src="/public/images/logos/logo-white.png"
                alt="GuzoMate"
                className="h-8 w-auto"
                onError={(e) => {
                  e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iOCIgZmlsbD0iI0EzNzIzOCIvPgo8dGV4dCB4PSIxNiIgeT0iMjAiIGZvbnQtZmFtaWx5PSJJbnRlciwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5HTTwvdGV4dD4KPC9zdmc+';
                }}
              />
              <span className="text-xl font-bold text-white">GuzoMate</span>
            </div>

            {/* Right Section - Actions */}
            <div className="flex items-center space-x-4">
              {/* Search Icon */}
              <div className="relative">
                <button
                  onClick={() => setIsSearchOpen(!isSearchOpen)}
                  className="p-2 text-white hover:text-gray-300 transition-colors"
                  aria-label="Toggle search"
                  aria-expanded={isSearchOpen}
                >
                  <img
                    src="/public/icons/search_icon.png"
                    alt="Search"
                    className="w-5 h-5"
                    onError={(e) => {
                      e.target.outerHTML = '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>';
                    }}
                  />
                </button>

                {/* Search Dropdown */}
                <SearchBar
                  isVisible={isSearchOpen}
                  onClose={() => setIsSearchOpen(false)}
                  onSearch={handleSearch}
                />
              </div>

              {/* Language Selector */}
              <div className="relative">
                <button
                  onClick={() => setIsLanguageOpen(!isLanguageOpen)}
                  className="flex items-center space-x-2 p-2 bg-white rounded-md hover:bg-gray-100 transition-colors"
                  aria-label="Select language"
                  aria-expanded={isLanguageOpen}
                  id="language-menu"
                >
                  <img
                    src={selectedLanguage.flagSrc}
                    alt={`${selectedLanguage.name} flag`}
                    className="w-5 h-5 rounded-sm object-cover"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xMCA1TDE1IDEwTDEwIDE1TDUgMTBMMTAgNVoiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
                    }}
                  />
                </button>

                <LanguagePopover
                  isOpen={isLanguageOpen}
                  onClose={() => setIsLanguageOpen(false)}
                  selectedLanguage={selectedLanguage}
                  onSelect={setSelectedLanguage}
                />
              </div>

              {/* Currency Selector */}
              <div className="relative">
                <button
                  onClick={() => setIsCurrencyOpen(!isCurrencyOpen)}
                  className="flex items-center space-x-1 px-3 py-2 bg-[#A37238] hover:bg-[#8B5E2F] text-white rounded-md transition-colors"
                  aria-label="Select currency"
                  aria-expanded={isCurrencyOpen}
                  id="currency-menu"
                >
                  <span className="text-sm font-medium">{selectedCurrency.code}</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                <CurrencyPopover
                  isOpen={isCurrencyOpen}
                  onClose={() => setIsCurrencyOpen(false)}
                  selectedCurrency={selectedCurrency}
                  onSelect={setSelectedCurrency}
                />
              </div>

              {/* Authentication Buttons */}
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setIsRegisterOpen(true)}
                  className="bg-[#A37238] hover:bg-[#8B5E2F] text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Register
                </button>
                <button
                  onClick={() => setIsLoginOpen(true)}
                  className="bg-[#A37238] hover:bg-[#8B5E2F] text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Sign in
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Authentication Modals */}
      <RegisterModal
        isOpen={isRegisterOpen}
        onClose={() => setIsRegisterOpen(false)}
        onRegister={handleRegister}
        onSwitchToLogin={switchToLogin}
      />

      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onLogin={handleLogin}
        onSwitchToRegister={switchToRegister}
      />
    </>
  );
};

export default Header;
