import React from 'react';
import './App.css';
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
import { profileData } from './mock';

function App() {
  return (
    <div className="App">
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
      <Toaster />
    </div>
  );
}

export default App;
