import React from 'react';
import { Brain, Code, Users } from 'lucide-react';

const Skills = ({ data }) => {
  return (
    <section className="section-container section-alt" id="skills">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">Skills & Expertise</h2>
          <p className="section-subtitle">Multidisciplinary competencies in healthcare and technology</p>
        </div>
        
        <div className="skills-grid">
          <div className="skill-category">
            <div className="skill-category-header">
              <Brain className="w-6 h-6" />
              <h3 className="skill-category-title">Clinical Expertise</h3>
            </div>
            <div className="skill-list">
              {data.skills.clinical.map((skill, index) => (
                <div key={index} className="skill-item">{skill}</div>
              ))}
            </div>
          </div>
          
          <div className="skill-category">
            <div className="skill-category-header">
              <Code className="w-6 h-6" />
              <h3 className="skill-category-title">Technical Skills</h3>
            </div>
            <div className="skill-list">
              {data.skills.technical.map((skill, index) => (
                <div key={index} className="skill-item">{skill}</div>
              ))}
            </div>
          </div>
          
          <div className="skill-category">
            <div className="skill-category-header">
              <Users className="w-6 h-6" />
              <h3 className="skill-category-title">Leadership & Management</h3>
            </div>
            <div className="skill-list">
              {data.skills.leadership.map((skill, index) => (
                <div key={index} className="skill-item">{skill}</div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="memberships-section">
          <h3 className="memberships-title">Professional Memberships</h3>
          <div className="memberships-list">
            {data.memberships.map((membership, index) => (
              <div key={index} className="membership-badge">{membership}</div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Skills;
