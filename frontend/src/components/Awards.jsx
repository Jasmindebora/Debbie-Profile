import React from 'react';
import { Award, Trophy, Star } from 'lucide-react';

const Awards = ({ data }) => {
  return (
    <section className="section-container" id="awards">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">Awards & Recognition</h2>
          <p className="section-subtitle">Celebrating excellence in healthcare and education</p>
        </div>
        
        <div className="awards-grid">
          {data.awards.map((award, index) => (
            <div key={index} className="award-card">
              <div className="award-icon-wrapper">
                {index === 0 ? <Trophy className="award-icon" /> : 
                 index === 1 ? <Star className="award-icon" /> : 
                 <Award className="award-icon" />}
              </div>
              <div className="award-content">
                <h3 className="award-title">{award.title}</h3>
                <p className="award-organization">{award.organization}</p>
                <p className="award-year">{award.year}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Awards;
