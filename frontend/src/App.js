import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from './components/ui/toaster';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import Experience from './components/Experience';
import Innovations from './components/Innovations';
import Research from './components/Research';
import Awards from './components/Awards';
import Skills from './components/Skills';
import Contact from './components/Contact';
import Footer from './components/Footer';
import CDSSDashboard from './components/cdss/CDSSDashboard';
import { profileData } from './mock';

// Portfolio Page
const PortfolioPage = () => (
  <>
    <Header />
    <Hero data={profileData} />
    <About data={profileData} />
    <Experience data={profileData} />
    <Innovations data={profileData} />
    <Research data={profileData} />
    <Awards data={profileData} />
    <Skills data={profileData} />
    <Contact data={profileData} />
    <Footer data={profileData} />
  </>
);

// CDSS Page
const CDSSPage = () => (
  <div className="cdss-page">
    <CDSSDashboard />
  </div>
);

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/portfolio" replace />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
          <Route path="/cdss" element={<CDSSPage />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;
