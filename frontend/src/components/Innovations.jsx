import React from 'react';
import { Lightbulb, FileCheck, Calendar } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card';
import { Badge } from './ui/badge';

const Innovations = ({ data }) => {
  return (
    <section className="section-container" id="innovations">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">AI Innovations & Patents</h2>
          <p className="section-subtitle">Pioneering healthcare technology solutions</p>
        </div>
        
        <div className="innovations-grid">
          {data.patents.map((patent, index) => (
            <Card key={index} className="innovation-card">
              <CardHeader>
                <div className="innovation-icon">
                  <Lightbulb className="w-6 h-6" />
                </div>
                <CardTitle className="innovation-title">{patent.title}</CardTitle>
                <div className="innovation-meta">
                  <Badge variant="secondary" className="innovation-badge">
                    <Calendar className="w-3 h-3 mr-1" />
                    {patent.year}
                  </Badge>
                  <Badge variant="outline" className="innovation-badge">
                    <FileCheck className="w-3 h-3 mr-1" />
                    {patent.applicationNumber}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="innovation-description">
                  {patent.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Innovations;
