import React from 'react';
import { Briefcase, MapPin, Calendar } from 'lucide-react';

const Experience = ({ data }) => {
  return (
    <section className="section-container section-alt" id="experience">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">Professional Experience</h2>
          <p className="section-subtitle">Two decades of healthcare leadership and innovation</p>
        </div>
        
        <div className="timeline">
          {data.experience.map((exp, index) => (
            <div key={index} className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <div className="timeline-header">
                  <div>
                    <h3 className="timeline-title">{exp.title}</h3>
                    <div className="timeline-organization">
                      <Briefcase className="w-4 h-4" />
                      {exp.organization}
                    </div>
                  </div>
                  <div className="timeline-meta">
                    <div className="timeline-period">
                      <Calendar className="w-4 h-4" />
                      {exp.period}
                    </div>
                    <div className="timeline-location">
                      <MapPin className="w-4 h-4" />
                      {exp.location}
                    </div>
                  </div>
                </div>
                <p className="timeline-description">{exp.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Experience;
