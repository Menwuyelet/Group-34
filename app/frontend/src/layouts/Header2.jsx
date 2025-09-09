import React, { useState, useEffect, useRef } from 'react';
import logo from '/public/images/logos/logo-black.png'
import ethio from '/public/icons/ethiopia.png'


// Function to get the number of days in a specific month and year.
const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();

// Function to get the first day of the month (0=Sunday, 1=Monday, ...).
const firstDayOfMonth = (year, month) => new Date(year, month, 1).getDay();

const BedIcon = () => (
<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
    <path d="M17.293 7.293A1 1 0 0118 8v8a1 1 0 01-1 1H3a1 1 0 01-1-1V8a1 1 0 01.707-.957l7-2a1 1 0 01.586 0l7 2zM12 10a1 1 0 10-2 0v3a1 1 0 102 0v-3zM5 10a1 1 0 10-2 0v3a1 1 0 102 0v-3z" />
    <path fillRule="evenodd" d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
</svg>
);

const CalendarIcon = () => (
<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
</svg>
);

const UserGroupIcon = () => (
<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zm-1.559 4.157a4.5 4.5 0 00-5.882 0 6.002 6.002 0 00-2.03 4.642V16a1 1 0 001 1h10a1 1 0 001-1v-1.201a6.002 6.002 0 00-2.03-4.642zM16.5 6a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zM18 10a4.5 4.5 0 00-5.882 0 6.002 6.002 0 00-2.03 4.642V16a1 1 0 00.5.874 4.502 4.502 0 008.062 0 1 1 0 00.5-.874v-1.201a6.002 6.002 0 00-2.03-4.642z" />
</svg>
);

const ChevronDownIcon = () => (
<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
</svg>
);



// This is the core component that for the search interface.
const SearchDropdown = () => {

// State to manage which dropdown (region, calendar, guests) is currently open.
const [activeDropdown, setActiveDropdown] = useState(null);

// State for all the form inputs.
const [region, setRegion] = useState('Addis Ababa');
const [checkInDate, setCheckInDate] = useState(null);
const [checkOutDate, setCheckOutDate] = useState(null);
const [adults, setAdults] = useState(2);
const [children, setChildren] = useState(0);
const [rooms, setRooms] = useState(1);

// A ref to the main dropdown container. Used to detect clicks outside of the component.
const dropdownRef = useRef(null);


// This effect adds an event listener to the whole document to detect clicks.
// If a click happens outside the `dropdownRef` element, it closes any active dropdown.
useEffect(() => {
    const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setActiveDropdown(null);
        }
    };
    document.addEventListener("mousedown", handleClickOutside);
    // Cleanup function: remove the event listener when the component unmounts.
    return () => {
        document.removeEventListener("mousedown", handleClickOutside);
    };
}, []);

// Toggles the visibility of a specific dropdown.
const handleDropdownToggle = (dropdownName) => {
    setActiveDropdown(activeDropdown === dropdownName ? null : dropdownName);
};

// Handles the logic for selecting check-in and check-out dates from the calendar.
const handleDateSelect = (day) => {
    const selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    if (!checkInDate || (checkInDate && checkOutDate)) {
        // If no check-in date is set, or if both are set, start a new selection.
        setCheckInDate(selectedDate);
        setCheckOutDate(null);
    } else if (selectedDate > checkInDate) {
        // If a check-in date is set and the new date is after it, set it as the check-out date.
        setCheckOutDate(selectedDate);
        setActiveDropdown(null); // Close calendar after selecting a range.
    } else {
        // If the selected date is before the current check-in date, reset the selection.
        setCheckInDate(selectedDate);
        setCheckOutDate(null);
    }
};

// Handles the final search action.
const handleSearch = () => {
    // Basic validation before proceeding.
    if (!region) {
        alert("Please select a region.");
        return;
    }
    if (!checkInDate || !checkOutDate) {
        alert("Please select a check-in and check-out date.");
        return;
    }
    // Format dates for display or for sending to an API.
    const formattedCheckIn = checkInDate.toLocaleDateString();
    const formattedCheckOut = checkOutDate.toLocaleDateString();

    // For demonstration, we just log the search details to the console.
    // This sends the log in the search details to the database.
    console.log({
        region,
        checkIn: formattedCheckIn,
        checkOut: formattedCheckOut,
        adults,
        children,
        rooms
    });
    alert(`Searching for hotels in ${region} from ${formattedCheckIn} to ${formattedCheckOut}`);
};



// --- CALENDAR LOGIC ---
// State to keep track of the currently displayed month in the calendar.
const [currentDate, setCurrentDate] = useState(new Date());

// --- RENDER FUNCTIONS ---
// These functions return JSX for the different dropdown panels (calendar, guests, region).
// This keeps the main return statement cleaner.

// Renders the interactive calendar for date selection.
const renderCalendar = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const monthName = currentDate.toLocaleString('default', { month: 'long' });

    const days = daysInMonth(year, month);
    const firstDay = firstDayOfMonth(year, month);

    const blanks = Array(firstDay).fill(null);
    const monthDays = Array.from({ length: days }, (_, i) => i + 1);
    
    const today = new Date();
    today.setHours(0,0,0,0); // Normalize today's date to midnight for accurate comparison.

    return (
        <div className="absolute top-full mt-2 w-80 bg-white border rounded-lg shadow-xl z-20 p-4">
            {/* Calendar Header: Month/Year and navigation buttons */}
            <div className="flex justify-between items-center mb-4">
                <button onClick={() => setCurrentDate(new Date(year, month - 1, 1))} className="p-1 rounded-[10px] hover:bg-gray-100">&lt;</button>
                <div className="font-semibold">{monthName} {year}</div>
                <button onClick={() => setCurrentDate(new Date(year, month + 1, 1))} className="p-1 rounded-[10px] hover:bg-gray-100">&gt;</button>
            </div>
            {/* Calendar Grid */}
            <div className="grid grid-cols-7 gap-1 text-center text-sm">
                {/* Day labels (S, M, T, etc.) */}
                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map(day => <div key={day} className="font-medium text-gray-500">{day}</div>)}
                {/* Blank spaces for the start of the month */}
                {blanks.map((_, i) => <div key={`blank-${i}`}></div>)}
                {/* The actual days of the month */}
                {monthDays.map(day => {
                    const date = new Date(year, month, day);
                    date.setHours(0,0,0,0); // Normalize for comparison.

                    // Determine the state of each day (past, selected, in range).
                    const isPast = date < today;
                    const isCheckIn = checkInDate && date.getTime() === checkInDate.getTime();
                    const isCheckOut = checkOutDate && date.getTime() === checkOutDate.getTime();
                    const isInRange = checkInDate && checkOutDate && date > checkInDate && date < checkOutDate;

                    // Apply dynamic styling based on the day's state.
                    let bgClass = '';
                    if (isCheckIn || isCheckOut) bgClass = 'bg-blue-500 text-white rounded-[10px]';
                    else if (isInRange) bgClass = 'bg-blue-100';
                    else if (!isPast) bgClass = 'hover:bg-gray-200 rounded-full';

                    return (
                        <button
                            key={day}
                            onClick={() => !isPast && handleDateSelect(day)}
                            disabled={isPast}
                            className={`p-2 ${bgClass} ${isPast ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700'}`}
                        >
                            {day}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

// Renders the panel for selecting the number of adults, children, and rooms.
const renderGuestSelector = () => (
    <div className="absolute top-full mt-2 w-72 bg-white border rounded-lg shadow-xl z-20 p-4 space-y-4">
        {[{label: 'Adults', value: adults, setter: setAdults, min: 1},
            {label: 'Children', value: children, setter: setChildren, min: 0},
            {label: 'Rooms', value: rooms, setter: setRooms, min: 1}].map(item => (
            <div key={item.label} className="flex justify-between items-center">
                <span className="text-gray-700">{item.label}</span>
                <div className="flex items-center gap-4">
                    <button 
                        onClick={() => item.setter(Math.max(item.min, item.value - 1))}
                        className="w-8 h-8 border rounded-full text-lg font-bold text-gray-600 hover:bg-gray-100 disabled:opacity-50"
                        disabled={item.value === item.min}
                    >-</button>
                    <span>{item.value}</span>
                    <button 
                        onClick={() => item.setter(item.value + 1)}
                        className="w-8 h-8 border rounded-[10px] text-lg font-bold text-gray-600 hover:bg-gray-100"
                    >+</button>
                </div>
            </div>
        ))}
    </div>
);


// Renders the dropdown list of available regions.
const renderRegionSelector = () => (
    <div className="absolute top-full mt-2 w-64 bg-white border rounded-[10px] shadow-xl z-20">
        {['Addis Ababa', 'Gondar', 'Bahir Dar', 'Lalibela', 'Axum','Hawassa','Arba Minch', 'Jimma', 'Haramaya','Dir Dawa'].map(city => (
            <div 
                key={city} 
                onClick={() => { setRegion(city); handleDropdownToggle('region'); }}
                className="p-3 hover:bg-gray-100 rounded-[10px] cursor-pointer text-gray-700"
            >
                {city}
            </div>
        ))}
    </div>
);



// This is the final JSX that gets rendered to the DOM.
return (
    <div ref={dropdownRef} className="bg-white backdrop-blur-sm p-2 rounded-[15px] shadow-lg flex items-center space-x-1 md:space-x-2 w-full max-w-4xl mx-auto">
        {/* Region Selector Section */}
        <div className="relative flex-1">
            <button onClick={() => handleDropdownToggle('region')} className="w-full h-14 text-left px-4 py-2 flex items-center space-x-3 rounded-[10px] hover:bg-gray-200/50 transition-colors">
                <BedIcon />
                <div className="flex-1">
                    <span className="text-sm text-gray-500">Region</span>
                    <p className="font-semibold text-gray-800 truncate">{region}</p>
                </div>
                <ChevronDownIcon />
            </button>
            {activeDropdown === 'region' && renderRegionSelector()}
        </div>

        <div className="h-8 border-l border-gray-200"></div>

        {/* Date Selector Section */}
        <div className="relative flex-1">
            <button onClick={() => handleDropdownToggle('calendar')} className="w-full h-14 text-left px-4 py-2 flex items-center space-x-3 rounded-[10px] hover:bg-gray-200/50 transition-colors">
                <CalendarIcon />
                <div className="flex-1">
                    <span className="text-sm text-gray-500">Check-in - Check-out</span>
                    <p className="font-semibold text-gray-800 truncate">
                        {checkInDate ? checkInDate.toLocaleDateString() : 'Select date'} - {checkOutDate ? checkOutDate.toLocaleDateString() : 'Select date'}
                    </p>
                </div>
            </button>
            {activeDropdown === 'calendar' && renderCalendar()}
        </div>

        <div className="h-8 border-l border-gray-200"></div>

        {/* Guest Selector Section */}
        <div className="relative flex-1">
            <button onClick={() => handleDropdownToggle('guests')} className="w-full h-14 text-left px-4 py-2 flex items-center space-x-3 rounded-[10px] hover:bg-gray-200/50 transition-colors">
                <UserGroupIcon />
                <div className="flex-1">
                    <span className="text-sm text-gray-500">Guests</span>
                    <p className="font-semibold text-gray-800 truncate">{adults} adults, {children} children, {rooms} room</p>
                </div>
            </button>
            {activeDropdown === 'guests' && renderGuestSelector()}
        </div>

        {/* Search Button Section */}
        <div>
            <button 
                onClick={handleSearch}
                className="bg-yellow-800 hover:bg-yellow-900 text-white font-bold h-14 w-14 md:w-28 rounded-[10px] flex items-center justify-center transition-colors">
                <span className="hidden md:inline">Search</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 md:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </button>
        </div>
    </div>
);
};



// The Main Header component
// This component acts as a container to for the Header.

export default function Header2() {
// State to control the visibility of the entire search dropdown component.
const [isSearchVisible, setIsSearchVisible] = useState(false);

return (
    <div className="font-sans antialiased text-gray-800 bg-gray-100">
        {/* The navigation bar */}
        <div className='fixed w-full z-20'>
            <nav className="bg-white shadow-md p-4 flex justify-between items-center">
                <a href="#"><div className=" pl-7 flex gap-2 font-bold items-center w-[100px] justify-right text-yellow-800 text-[23px]"><img className='w-10' src={logo}></img><h1>GuzoMate</h1></div></a>
                
                <div className="flex items-center space-x-4 ">

                    {/* The search icon that toggles the dropdown's visibility */}
                    <button 
                        onClick={() => setIsSearchVisible(!isSearchVisible)}
                        className="p-2 rounded-full hover:bg-gray-200 transition-colors"
                        aria-label="Toggle search"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </button>

                    {/* Language preferences, currency and Register & Sign In */}
                    <img src={ethio} alt="" className='w-7 cursor-pointer'/>
                    <button className="hidden md:block px-4 py-2 text-sm font-bold text-gray-700 rounded-md hover:bg-gray-100">USD</button>
                    <button className="hidden md:block px-4 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100">Log In</button>
                    <button className="hidden md:block px-4 py-2 text-sm font-medium text-white bg-yellow-800 rounded-md hover:bg-yellow-900">Sign Up</button>
                </div>
            </nav>


            {/* The container where the SearchDropdown component is rendered */}
            <div className=" p-4 -mt-3 z-20">
                {/* Conditionally render the SearchDropdown based on isSearchVisible state */}
                {isSearchVisible && (
                    <div className="transition-all duration-300 ease-in-out">
                            <SearchDropdown />
                    </div>
                )}
            </div>
        </div>

    </div>
);
}
