import React, { useState, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

import c1 from '/public/images/cities/c1.jpg';
import c2 from '/public/images/cities/c2.jpeg';
import c3 from '/public/images/cities/c3.jpg';
import c4 from '/public/images/cities/c4.jpeg';
import c6 from '/public/images/cities/c6.jpg';
import c7 from '/public/images/cities/c7.webp';


// Main App Component which serves as our Hero Slider
export default function App() {

// Array of slide data. Each object represents a slide with its image and text content.
const slides = [
    {
        url: c1,
        title: 'Addis Ababa',
        description: 'Addis Ababa, the capital city of Ethiopia, most beautiful city.',
    },
    {
        url: c2,
        title: 'Haramaya',
        description: 'One of the busy cities in Ethiopia, full of natural wonders.',
    },
    {
        url: c3,
        title: 'Bar Dar',
        description: 'Nature and beauty city of Ethiopia, with amazing destinations.',
    },
    {
        url: c4,
        title: 'Arba Minch',
        description: 'The land of Peace and Wisdom, in the Southern Region.',
    },
    {
        url: c6,
        title: 'Wolayta',
        description: 'The land of Peace and Wisdom, in the Southern Region.',
    },
    {
        url: c7,
        title: 'Jinka',
        description: 'The land of Peace and Wisdom, in the Southern Region.',
    },
];


// State to keep track of the current slide index
const [currentIndex, setCurrentIndex] = useState(0);

// Function to go to the previous slide
const prevSlide = useCallback(() => {
    const isFirstSlide = currentIndex === 0;
    const newIndex = isFirstSlide ? slides.length - 1 : currentIndex - 1;
    setCurrentIndex(newIndex);
}, [currentIndex, slides.length]);

// Function to go to the next slide
const nextSlide = useCallback(() => {
    const isLastSlide = currentIndex === slides.length - 1;
    const newIndex = isLastSlide ? 0 : currentIndex + 1;
    setCurrentIndex(newIndex);
}, [currentIndex, slides.length]);

// Function to go to a specific slide by its index
const goToSlide = (slideIndex) => {
    setCurrentIndex(slideIndex);
};

// useEffect hook to handle the auto-play functionality
useEffect(() => {
    // Set an interval to automatically advance to the next slide every 3 seconds
    const slideInterval = setInterval(nextSlide, 3000);
    
    // Cleanup function to clear the interval when the component unmounts
    // or when the dependencies (nextSlide) change. This prevents memory leaks.
    return () => clearInterval(slideInterval);
}, [nextSlide]);


return (
    <div className="w-full h-screen m-auto relative group">
        {/* Background Image and Overlay */}
        <div
            style={{ backgroundImage: `url(${slides[currentIndex].url})` }}
            className="w-full h-full bg-center bg-cover duration-1000 ease-in-out"
        >
            {/* Dark overlay for better text readability and the gradient from down*/}
            <div className='absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent'></div>
            <div className="absolute inset-0 bg-black opacity-40"></div>
        </div>

        {/* Overlay Content (Title, Description, Button) */}
        <div className="absolute inset-0 flex flex-col items-start justify-end text-center text-white p-4 ml-15 mb-15">
            <h1 className="lg:text-[50px] md:text-6xl font-extrabold mb-2 drop-shadow-2xl transition-all duration-500">
                {slides[currentIndex].title}
            </h1>
            <p className="text-left text-lg md:text-xl max-w-2xl mb-8 drop-shadow-lg transition-all duration-500">
                <a href="">{slides[currentIndex].description}</a>
            </p>
            <button className="bg-yellow-800 hover:bg-yellow-900 text-white font-bold py-3 px-8 rounded-lg text-lg transition duration-300 ease-in-out transform hover:scale-105">
                Explore More
            </button>
        </div>

        {/* Left Arrow */}
        <div className="hidden group-hover:block absolute top-1/2 -translate-y-1/2 left-5 text-2xl rounded-full p-2 bg-black/40 text-white cursor-pointer transition-opacity duration-300">
            <ChevronLeft onClick={prevSlide} size={30} />
        </div>

        {/* Right Arrow */}
        <div className="hidden group-hover:block absolute top-1/2 -translate-y-1/2 right-5 text-2xl rounded-full p-2 bg-black/40 text-white cursor-pointer transition-opacity duration-300">
            <ChevronRight onClick={nextSlide} size={30} />
        </div>

        {/* Pagination Dots */}
        <div className="absolute bottom-5 left-1/2 -translate-x-1/2 flex justify-center py-2 space-x-3">
            {slides.map((slide, slideIndex) => (
                <div
                    key={slideIndex}
                    onClick={() => goToSlide(slideIndex)}
                    className={`cursor-pointer w-2 h-2 rounded-full transition-all duration-300 ${
                        currentIndex === slideIndex ? 'bg-white scale-125' : 'bg-white/50'
                    }`}
                ></div>
            ))}
        </div>
    </div>
);
}
