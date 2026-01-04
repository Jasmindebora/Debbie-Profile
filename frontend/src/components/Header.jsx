import React, { useState, useEffect } from 'react';
import { Menu, X, Activity } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate, useLocation } from 'react-router-dom';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  const isPortfolioPage = location.pathname === '/portfolio';

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    setIsMobileMenuOpen(false);
  };

  return (
    <header className={`nav-header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="nav-container">
        <div className="nav-logo" onClick={() => navigate('/portfolio')}>
          <span className="logo-text">Dr. Debora Jasmin</span>
        </div>
        
        {isPortfolioPage ? (
          <>
            <nav className="nav-menu">
              <button onClick={() => scrollToSection('about')} className="nav-link">About</button>
              <button onClick={() => scrollToSection('experience')} className="nav-link">Experience</button>
              <button onClick={() => scrollToSection('innovations')} className="nav-link">Innovations</button>
              <button onClick={() => scrollToSection('research')} className="nav-link">Research</button>
              <button onClick={() => scrollToSection('awards')} className="nav-link">Awards</button>
              <button onClick={() => scrollToSection('skills')} className="nav-link">Skills</button>
            </nav>
            
            <div className="nav-actions">
              <Button 
                className="btn-secondary"
                onClick={() => navigate('/cdss')}
              >
                <Activity className="w-4 h-4 mr-2" />
                NP-CDSS
              </Button>
              <Button 
                className="btn-primary nav-cta"
                onClick={() => scrollToSection('contact')}
              >
                Contact
              </Button>
            </div>
          </>
        ) : (
          <Button 
            className="btn-secondary"
            onClick={() => navigate('/portfolio')}
          >
            Back to Portfolio
          </Button>
        )}
        
        <button 
          className="mobile-menu-toggle"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>
      
      {isMobileMenuOpen && isPortfolioPage && (
        <div className="mobile-menu">
          <button onClick={() => scrollToSection('about')} className="mobile-menu-item">About</button>
          <button onClick={() => scrollToSection('experience')} className="mobile-menu-item">Experience</button>
          <button onClick={() => scrollToSection('innovations')} className="mobile-menu-item">Innovations</button>
          <button onClick={() => scrollToSection('research')} className="mobile-menu-item">Research</button>
          <button onClick={() => scrollToSection('awards')} className="mobile-menu-item">Awards</button>
          <button onClick={() => scrollToSection('skills')} className="mobile-menu-item">Skills</button>
          <button onClick={() => navigate('/cdss')} className="mobile-menu-item">NP-CDSS</button>
          <button onClick={() => scrollToSection('contact')} className="mobile-menu-item mobile-menu-cta">Contact</button>
        </div>
      )}
    </header>
  );
};

export default Header;
