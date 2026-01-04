import React from 'react';
import { Mail, Phone, Linkedin, BookOpen, FileText } from 'lucide-react';
import { Button } from './ui/button';

const Hero = ({ data }) => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <div className="hero-badge">
          <span>Healthcare Innovation • AI Research • Nursing Excellence</span>
        </div>
        
        <h1 className="hero-title">{data.name}</h1>
        
        <p className="hero-subtitle">{data.title}</p>
        
        <p className="hero-tagline">{data.tagline}</p>
        
        <div className="hero-stats">
          <div className="stat-item">
            <div className="stat-number">{data.researchMetrics.totalPublications}</div>
            <div className="stat-label">Publications</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">{data.researchMetrics.citations}</div>
            <div className="stat-label">Citations</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">4+</div>
            <div className="stat-label">AI Patents</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">20+</div>
            <div className="stat-label">Years Experience</div>
          </div>
        </div>
        
        <div className="hero-actions">
          <Button 
            className="btn-primary"
            onClick={() => document.getElementById('contact').scrollIntoView({ behavior: 'smooth' })}
          >
            <Mail className="w-4 h-4 mr-2" />
            Get in Touch
          </Button>
          <Button 
            className="btn-secondary"
            onClick={() => window.open(data.googleScholar, '_blank')}
          >
            <BookOpen className="w-4 h-4 mr-2" />
            View Publications
          </Button>
        </div>
        
        <div className="hero-links">
          <a href={data.linkedin} target="_blank" rel="noopener noreferrer" className="hero-link">
            <Linkedin className="w-5 h-5" />
          </a>
          <a href={data.researchgate} target="_blank" rel="noopener noreferrer" className="hero-link">
            <FileText className="w-5 h-5" />
          </a>
          <a href={data.googleScholar} target="_blank" rel="noopener noreferrer" className="hero-link">
            <BookOpen className="w-5 h-5" />
          </a>
        </div>
      </div>
    </section>
  );
};

export default Hero;
