import React from 'react';
import { GraduationCap, Award, Users } from 'lucide-react';

const About = ({ data }) => {
  return (
    <section className="section-container" id="about">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">About Me</h2>
          <p className="section-subtitle">Healthcare Professional • AI Innovator • Academic Leader</p>
        </div>
        
        <div className="about-grid">
          <div className="about-main">
            <p className="about-text">{data.bio}</p>
            
            <div className="about-highlights">
              <div className="highlight-card">
                <div className="highlight-icon">
                  <GraduationCap className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="highlight-title">Academic Excellence</h3>
                  <p className="highlight-description">
                    Doctorate in Hospital Administration with specialization in Medical-Surgical Nursing (Neurosciences)
                  </p>
                </div>
              </div>
              
              <div className="highlight-card">
                <div className="highlight-icon">
                  <Award className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="highlight-title">Research Impact</h3>
                  <p className="highlight-description">
                    {data.researchMetrics.citations} citations with h-index of {data.researchMetrics.hIndex} across {data.researchMetrics.totalPublications} publications
                  </p>
                </div>
              </div>
              
              <div className="highlight-card">
                <div className="highlight-icon">
                  <Users className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="highlight-title">Leadership Roles</h3>
                  <p className="highlight-description">
                    Professor cum Deputy Registrar, HOD MSN, NABH Assessor, and Ideation Mentor
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="about-sidebar">
            <div className="info-card">
              <h3 className="info-title">Education</h3>
              <div className="info-list">
                {data.education.map((edu, index) => (
                  <div key={index} className="info-item">
                    <div className="info-degree">{edu.degree}</div>
                    <div className="info-institution">{edu.institution}</div>
                    <div className="info-year">{edu.year}</div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="info-card">
              <h3 className="info-title">Key Certifications</h3>
              <div className="cert-list">
                {data.certifications.slice(0, 5).map((cert, index) => (
                  <div key={index} className="cert-badge">{cert}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
