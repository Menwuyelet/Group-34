import React, { useState } from 'react';

/**
 * SearchBar Component - Matches the exact layout from the header mockup
 * Features: Location input, date pickers, guest/room selector, search button
 */
const SearchBar = ({ onSearch, isVisible, onClose }) => {
  const [searchData, setSearchData] = useState({
    location: 'Addis Ababa',
    checkInDate: '',
    checkOutDate: '',
    adults: 2,
    children: 0,
    rooms: 1,
  });

  const [showGuestPanel, setShowGuestPanel] = useState(false);
  const [showLocationPanel, setShowLocationPanel] = useState(false);

  const cities = ['Addis Ababa', 'Hawassa', 'Arba Minch'];

  const handleInputChange = (field, value) => {
    setSearchData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGuestChange = (type, increment) => {
    setSearchData(prev => ({
      ...prev,
      [type]: Math.max(0, prev[type] + increment)
    }));
  };

  const handleSearch = () => {
    const payload = {
      location: searchData.location,
      dates: {
        checkIn: searchData.checkInDate,
        checkOut: searchData.checkOutDate
      },
      guests: {
        adults: searchData.adults,
        children: searchData.children,
        rooms: searchData.rooms
      },
      timestamp: new Date().toISOString()
    };
    
    onSearch(payload);
    onClose();
  };

  const formatGuestText = () => {
    const parts = [];
    if (searchData.adults > 0) parts.push(`${searchData.adults} adult${searchData.adults > 1 ? 's' : ''}`);
    if (searchData.children > 0) parts.push(`${searchData.children} children`);
    parts.push(`${searchData.rooms} room${searchData.rooms > 1 ? 's' : ''}`);
    return parts.join(' · ');
  };

  if (!isVisible) return null;

  return (
    <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-6 bg-white rounded-xl shadow-xl border border-gray-100 animate-slide-down z-50 w-[900px] max-w-[95vw]">
      <div className="flex items-center h-16">
        {/* Location Section */}
        <div className="flex items-center px-4 py-3 bg-gray-50 rounded-l-xl border-r border-gray-200 w-[200px] relative">
          <div className="w-4 h-4 text-gray-600 mr-3">
            <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
          </div>
          <div 
            className="flex-1 cursor-pointer min-w-0"
            onClick={() => setShowLocationPanel(!showLocationPanel)}
          >
            <span className="text-sm text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">{searchData.location}</span>
          </div>
          <button 
            className="text-gray-400 hover:text-gray-600 ml-2"
            onClick={() => setShowLocationPanel(!showLocationPanel)}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {/* Location Panel Dropdown */}
          {showLocationPanel && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
              {cities.map((city) => (
                <div
                  key={city}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer text-sm text-gray-900 border-b border-gray-100 last:border-b-0"
                  onClick={() => {
                    handleInputChange('location', city);
                    setShowLocationPanel(false);
                  }}
                >
                  {city}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Dates Section */}
        <div className="flex items-center px-4 py-3 bg-gray-50 border-r border-gray-200 w-[280px]">
          <div className="w-4 h-4 text-gray-600 mr-3">
            <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
              <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
          </div>
          <div className="flex-1 flex items-center space-x-2">
            <div className="flex-1">
              <input
                type="date"
                value={searchData.checkInDate}
                onChange={(e) => handleInputChange('checkInDate', e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="w-full text-xs text-gray-900 bg-transparent border-none outline-none cursor-pointer"
                title="Check-in date"
              />
            </div>
            <span className="text-gray-400 text-xs">-</span>
            <div className="flex-1">
              <input
                type="date"
                value={searchData.checkOutDate}
                onChange={(e) => handleInputChange('checkOutDate', e.target.value)}
                min={searchData.checkInDate || new Date().toISOString().split('T')[0]}
                className="w-full text-xs text-gray-900 bg-transparent border-none outline-none cursor-pointer"
                title="Check-out date"
              />
            </div>
          </div>
        </div>

        {/* Guests & Rooms Section */}
        <div className="flex items-center px-3 py-3 bg-gray-50 border-r border-gray-200 w-[220px] relative">
          <div 
            className="flex items-center cursor-pointer w-full"
            onClick={() => setShowGuestPanel(!showGuestPanel)}
          >
            <div className="w-4 h-4 text-gray-600 mr-2">
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                <path d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zm4 18v-6h2.5l-2.54-7.63A1.5 1.5 0 0 0 18.54 8H16c-.8 0-1.54.37-2 .97L12.5 11.5 10.24 9.24A1.5 1.5 0 0 0 9.18 8.71L7.5 10.5V9c0-.55-.45-1-1-1s-1 .45-1 1v13c0 .55.45 1 1 1s1-.45 1-1v-2.5l2.5-2.5L12.5 20H20z"/>
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <span className="text-xs text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">
                {formatGuestText()}
              </span>
            </div>
            <button className="text-gray-400 hover:text-gray-600 ml-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          {/* Guest Panel Dropdown */}
          {showGuestPanel && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 p-3 z-10 min-w-[280px]">
              <div className="space-y-3">
                {/* Adults */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-gray-900">Adults</div>
                    <div className="text-xs text-gray-500">Ages 13 or above</div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleGuestChange('adults', -1)}
                      disabled={searchData.adults <= 1}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:border-[#A37238] text-sm"
                    >
                      −
                    </button>
                    <span className="w-6 text-center text-sm font-medium">{searchData.adults}</span>
                    <button
                      onClick={() => handleGuestChange('adults', 1)}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center hover:border-[#A37238] text-sm"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Children */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-gray-900">Children</div>
                    <div className="text-xs text-gray-500">Ages 2-12</div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleGuestChange('children', -1)}
                      disabled={searchData.children <= 0}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:border-[#A37238] text-sm"
                    >
                      −
                    </button>
                    <span className="w-6 text-center text-sm font-medium">{searchData.children}</span>
                    <button
                      onClick={() => handleGuestChange('children', 1)}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center hover:border-[#A37238] text-sm"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Rooms */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-gray-900">Rooms</div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleGuestChange('rooms', -1)}
                      disabled={searchData.rooms <= 1}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:border-[#A37238] text-sm"
                    >
                      −
                    </button>
                    <span className="w-6 text-center text-sm font-medium">{searchData.rooms}</span>
                    <button
                      onClick={() => handleGuestChange('rooms', 1)}
                      className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center hover:border-[#A37238] text-sm"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Search Button */}
        <div className="flex items-center px-3 w-[120px]">
          <button
            onClick={handleSearch}
            className="bg-[#A37238] hover:bg-[#8B5E2F] text-white px-6 py-3 rounded-xl font-medium text-sm transition-colors duration-200 whitespace-nowrap w-full"
          >
            Search
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
