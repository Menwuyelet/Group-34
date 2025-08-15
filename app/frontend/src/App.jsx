import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './layouts/Header/Header';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import './App.css';

function App() {
  // Handler functions for header interactions
  const handleSearch = (searchData) => {
    console.log('Search submitted:', searchData);
    // TODO: Implement search functionality
  };

  const handleLogin = async (loginData) => {
    console.log('Login attempt:', loginData);
    // TODO: Implement authentication
    return Promise.resolve();
  };

  const handleRegister = async (registerData) => {
    console.log('Registration attempt:', registerData);
    // TODO: Implement user registration
    return Promise.resolve();
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header 
          onSearch={handleSearch}
          onLogin={handleLogin}
          onRegister={handleRegister}
        />
        <main className="pt-20">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
