import React from 'react';
//import Header from './layouts/Header.jsx';
import Footer from './layouts/Footer.jsx';
import Header2 from './layouts/Header2.jsx';
import Hero from './layouts/Hero.jsx';

import Homepage from './pages/homepage.jsx';


export default function App() {
    return (
        <>
            <Header2 />
            <Hero />
            <div className='pl-30 pr-30 bg-gray-50 mt-5'><Homepage /></div>
            <Footer />
        </>
    );
}