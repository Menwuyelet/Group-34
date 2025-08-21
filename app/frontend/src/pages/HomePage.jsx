import React from 'react';
import h1 from '/public/images/hotel/h1.jpg';
import h2 from '/public/images/hotel/h2.jpg';
import h3 from '/public/images/hotel/h3.jpg';
import h4 from '/public/images/hotel/h4.jpeg';
import h5 from '/public/images/hotel/h5.jpg';
import h6 from '/public/images/hotel/h6.jpg';

import c1 from '/public/images/cities/c1.jpg';
import c2 from '/public/images/cities/c2.jpeg';
import c3 from '/public/images/cities/c3.jpg';
import c4 from '/public/images/cities/c4.jpeg';
import c6 from '/public/images/cities/c6.jpg';
import c7 from '/public/images/cities/c7.webp';


import a3 from '/public/images/ads/a3.jpg';
import a5 from '/public/images/ads/a5.jpg';
import a6 from '/public/images/ads/a6.png';
import a9 from '/public/images/ads/a9.jpeg';

// Star rating component to render the stars

// Data for the trending destinations
const trendingDestinations = [
{
id: 1,
title: 'Addis Ababa',
location: 'Ethiopia',
imageUrl: c1,
},
{
id: 2,
title: 'Bar Dar',
location: 'Gambela',
imageUrl: c2,
},
{
id: 3,
title: 'Arba Minch',
location: 'Souther Region',
imageUrl: c3,
},
{
id: 4,
title: 'Jimma',
location: 'Afar Region',
imageUrl: c6,
},
{
id: 5,
title: 'Haramaya',
location: 'Tigray Region',
imageUrl: c7,
},
{
id: 5,
title: 'Jinka',
location: 'Southern Region',
imageUrl: c4,
},
];

// Data for the popular hotels
const popularHotels = [
{
id: 1,
name: 'The Skylight Hotel',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h1,
},
{
id: 2,
name: 'Addis Ababa Bole',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h2,
},
{
id: 3,
name: 'Sheraton Addis',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h3,
},
{
id: 4,
name: 'Ramada Addis Hotel',
location: 'Addis Ababa, Ethiopia',
rating: 4,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h4,
},
{
id: 5,
name: 'Hyatt Regency Addis',
location: 'Addis Ababa, Ethiopia',
rating: 4,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h5,
},
{
id: 6,
name: 'Ethiopian Skylight Hotel',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h6,
},
{
id: 6,
name: 'James Hote Ethiopia',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h2,
},
{
id: 6,
name: 'Pyramid Continental Hotel',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h1,
},
{
id: 6,
name: 'Daros Hotel',
location: 'Addis Ababa, Ethiopia',
rating: 5,
description: 'This is a description of the hotel. It is a very nice hotel with a lot of features and amenities for your convenience.',
imageUrl: h4,
},
];



const Homepage = () => {
return (
<div className="font-sans bg-gray-50 text-gray-800">
    {/* Offers Section */}
    <section className="container mx-auto p-4 md:p-8 space-y-4">
    <h2 className="text-xl font-bold text-gray-700">Offers</h2>
    <p className="text-sm text-gray-500">Promotional offers, deals and special offers for you</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-40">
        <div className="overflow-hidden rounded-xl shadow-lg ">
        <img src={a6} alt="Offer 1" className="w-fit h-auto" />
        </div>
        <div className="overflow-hidden rounded-xl shadow-lg">
        <img src={a5} alt="Offer 2" className="w-fit h-auto" />
        </div>
    </div>
    </section>


    {/* Trending Destinations Section */}
    <section className="container mx-auto p-4 md:p-8 space-y-4">
    <h2 className="text-xl font-bold text-gray-700">Trending Destinations</h2>
    <p className="text-sm text-gray-500">Most popular choices for international travels to Ethiopia</p>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4">
        {trendingDestinations.map((dest) => (
        <div key={dest.id} className="relative overflow-hidden rounded-xl shadow-lg group">
            <img src={dest.imageUrl} alt={dest.title} className="w-full h-48 object-cover rounded-xl transition-transform duration-300 group-hover:scale-105" />
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent flex items-end p-4 rounded-xl">
            <div>
                <h3 className="text-white font-bold">{dest.title}</h3>
                <p className="text-gray-200 text-sm">{dest.location}</p>
            </div>
            </div>
        </div>
        ))}
    </div>
    </section>


    {/* Feature Icons Section */}
    <section className="container mx-auto p-4 md:p-8">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-3 bg-blue-100 rounded-full text-blue-500">
            <svg  xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c1.657 0 3 1.343 3 3v2a3 3 0 01-3 3h-2a3 3 0 01-3-3v-2c0-1.657 1.343-3 3-3z" />
            </svg>
        </div>
        <div>
            <h4 className="font-bold text-gray-700">Book and pay online</h4>
            <p className="text-sm text-gray-500">Use any card to book a room and pay online</p>
        </div>
        </div>
        <div className="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-3 bg-red-100 rounded-full text-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
        </div>
        <div>
            <h4 className="font-bold text-gray-700">Trusted 24/7 customer service</h4>
            <p className="text-sm text-gray-500">Book a room and instantly receive a confirmation via email</p>
        </div>
        </div>
        <div className="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-3 bg-green-100 rounded-full text-green-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 1h-3.414a2 2 0 00-1.414.586L12 17.586l-2.172-2.172A2 2 0 008.414 15H5m0-12h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z" />
            </svg>
        </div>
        <div>
            <h4 className="font-bold text-gray-700">Hold seat and pay at the office</h4>
            <p className="text-sm text-gray-500">Reserve your room and pay later</p>
        </div>
        </div>
    </div>
    </section>


    {/* Popular Hotels Section */}
    <section className="container mx-auto p-4 md:p-8 space-y-4">
    <h2 className="text-xl font-bold text-gray-700">Popular Hotels</h2>
    <p className="text-sm text-gray-500">Most popular choices for travelers to Ethiopia</p>
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {popularHotels.map((hotel) => (
        <div key={hotel.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
            <img src={hotel.imageUrl} alt={hotel.name} className="w-full h-48 object-cover" />
            <div className="p-4 space-y-2">
            <h3 className="font-bold text-lg text-gray-900">{hotel.name}</h3>
            {/*<StarRating rating={hotel.rating} />*/}
            <p className="text-sm text-gray-500">{hotel.location}</p>
            <p className="text-sm text-gray-700">{hotel.description}</p>
            <button className="w-full mt-2 bg-yellow-800  text-white py-2 rounded-lg font-semibold hover:bg-yellow-900 transition-colors">Book Now</button>
            </div>
        </div>
        ))}
    </div>
    </section>


    {/* Main Banner */}
    <section className="container mx-auto p-4 md:p-8">
    <div className="overflow-hidden rounded-xl shadow-lg">
        <img src={a9} alt="Main Banner" className="w-full h-auto" />
    </div>
    </section>


    {/* Second Offers Section */}
    <section className="container mx-auto p-4 md:p-8 space-y-4">
    <h2 className="text-xl font-bold text-gray-700">Offers</h2>
    <p className="text-sm text-gray-500">Promotional offers, deals and special offers for you</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-40">
        <div className="overflow-hidden rounded-xl shadow-lg">
        <img src={a6} alt="Offer 3" className="w-fit h-fit" />
        </div>
        <div className="overflow-hidden rounded-xl shadow-lg">
        <img src={a3} alt="Offer 4" className="w-fit h-fit" />
        </div>
    </div>
    </section>


    {/* Contact Form Section */}
    <section className="container mx-auto p-4 md:p-8 space-y-4">
    <div className="bg-white rounded-xl flex-row p-10">
        <h3 className="text-lg font-bold text-gray-800">Please send your comment below</h3>
        <textarea
        className="w-[500px] h-32 p-4 mt-2 mr-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Type here..."
        ></textarea><br />
        <button className="mt-3 px-6 py-2 bg-yellow-600 text-white font-semibold rounded-lg hover:bg-yellow-700 transition-colors">
        Submit
        </button>
    </div>
    </section>
</div>
);
};

export default Homepage;
