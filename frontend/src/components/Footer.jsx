import React from 'react';
import { Linkedin, Mail, BookOpen, FileText, Heart } from 'lucide-react';

const Footer = ({ data }) => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-grid">
          <div className="footer-section">
            <h3 className="footer-title">Dr. Debora Jasmin</h3>
            <p className="footer-description">
              Professor, Healthcare Innovator, and AI Researcher dedicated to advancing healthcare through technology and education.
            </p>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-heading">Quick Links</h4>
            <div className="footer-links">
              <a href="#about" className="footer-link">About</a>
              <a href="#experience" className="footer-link">Experience</a>
              <a href="#innovations" className="footer-link">Innovations</a>
              <a href="#research" className="footer-link">Research</a>
            </div>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-heading">Connect</h4>
            <div className="footer-social">
              <a href={data.linkedin} target="_blank" rel="noopener noreferrer" className="footer-social-link">
                <Linkedin className="w-5 h-5" />
                <span>LinkedIn</span>
              </a>
              <a href={data.googleScholar} target="_blank" rel="noopener noreferrer" className="footer-social-link">
                <BookOpen className="w-5 h-5" />
                <span>Google Scholar</span>
              </a>
              <a href={data.researchgate} target="_blank" rel="noopener noreferrer" className="footer-social-link">
                <FileText className="w-5 h-5" />
                <span>ResearchGate</span>
              </a>
              <a href={`mailto:${data.email}`} className="footer-social-link">
                <Mail className="w-5 h-5" />
                <span>Email</span>
              </a>
            </div>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-heading">Affiliation</h4>
            <p className="footer-affiliation">
              SGT University<br />
              Faculty of Nursing<br />
              Gurugram, Haryana, India
            </p>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p className="footer-copyright">
            © {currentYear} Dr. Debora Jasmin Settepalli. All rights reserved.
          </p>
          <p className="footer-credits">
            Built with <Heart className="w-4 h-4 inline" style={{ color: '#8FEC78' }} /> for healthcare innovation
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
