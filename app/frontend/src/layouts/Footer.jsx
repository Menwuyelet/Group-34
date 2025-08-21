import React from 'react';
import { FaPhone, FaEnvelope, FaFacebook, FaInstagram, FaTiktok, FaYoutube, FaTelegram, FaWhatsapp, FaPinterest, FaLinkedin } from 'react-icons/fa';
import { MdLocationPin } from 'react-icons/md';

// NOTE: logos for GuzoMate and Sponsors.
import Logo from '/public/images/logos/logo-black.png'; 
import INSA from '/public/images/logos/INSA.png';

const Footer = () => {
return (
<footer className="bg-gray-200 py-5 pt-15 px-4 md:px-8 lg:px-16">
    <div className="container mx-auto">

    {/* Main footer content */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">


        {/* GuzoMate Logo & Title Section */}
        <a href="#"><div className="flex flex-col items-center justify-center md:items-start text-center md:text-left">

        {/* with a linke to the homepage */}
        <img src={Logo} alt="GuzoMate Logo" className="h-23 w-auto place-self-center -mb-2" />
        <p className="text-[25px] font-black text-black-800 place-self-center">GuzoMate</p>
        </div></a>



        {/* Contact Section */}
        <div className="flex flex-col items-center md:items-start text-center md:text-left">
            <h6 className="text-lg font-bold text-gray-800 mb-4 hover:text-yellow-900"><a href="#">Contact Us</a></h6>
            <div className="flex items-center text-gray-600 mb-2 hover:text-yellow-900">
                <FaPhone className="mr-2 text-black-500" />
                <span><a href="">+251 922 978 877</a></span>
            </div>
            <div className="flex items-center text-gray-600 mb-2 hover:text-yellow-900">
                <FaEnvelope className="mr-2 text-black-500" />
                <span><a href="#">GuzoMate@gmail.com</a></span>
            </div>
            <div className="flex items-center text-gray-600 hover:text-yellow-900">
                <MdLocationPin className="mr-2 text-black-500 " />
                <span><a href="">Addis Ababa, Ethiopia</a></span>
            </div>
        </div>



        {/* About Us & Social Media Section */}
        <div className="flex flex-col items-center justify-centerss md:items-start text-center md:text-left">
        <h6 className="text-lg font-bold ml-[12%] text-gray-800 mb-4 hover:text-yellow-900"><a href="#">About Us</a></h6>
        <div className="flex flex-wrap w-[200px] justify-center md:justify-start gap-4">

            <a href="#" className="text-gray-600 hover:text-blue-700 transition-colors">
            <FaFacebook className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-pink-500 transition-colors">
            <FaInstagram className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-red-500 transition-colors">
            <FaPinterest className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-red-400 transition-colors">
            <FaTiktok className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-red-500 transition-colors">
            <FaYoutube className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-blue-500 transition-colors">
            <FaTelegram className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-green-500 transition-colors">
            <FaWhatsapp className="h-7 w-7" />
            </a>
            <a href="#" className="text-gray-600 hover:text-blue-500 transition-colors">
            <FaLinkedin className="h-7 w-7" />
            </a>
        </div>
        </div>


        {/* Sponsors & Partners Section */}
        <div className="flex flex-col items-center md:items-start text-center md:text-left">
        <h6 className="text-lg font-bold text-gray-800 mb-4 hover:text-yellow-900"><a href="">Sponsors & Partners</a></h6>
        <div className="flex flex-wrap justify-center md:justify-start gap-4">
            {/* These images are placeholders. Replace them with your partner logos. */}
            <a href="#"><img src={INSA} alt="Partner 1" className="h-25 w-auto relative -top-4" /></a>
        </div>
        </div>
    </div>


    {/* Copyright and mission statement section */}
    <div className="mt-5 pt-6 border-t border-gray-400 text-center text-gray-600">
        <p className="text-sm">GuzoMate is leader in online hotel booking, travel and related services.</p>
        <p className="text-sm mt-1">Copyright © 2025 GuzoMate™. All rights reserved</p>
    </div>
    </div>
</footer>
);
};

export default Footer;