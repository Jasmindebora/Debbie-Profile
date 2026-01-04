import React from 'react';
import { BookOpen, ExternalLink, Quote } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card';
import { Badge } from './ui/badge';

const Research = ({ data }) => {
  return (
    <section className="section-container section-alt" id="research">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">Research & Publications</h2>
          <p className="section-subtitle">Contributing to healthcare and AI knowledge base</p>
        </div>
        
        <div className="research-metrics">
          <div className="metric-card">
            <div className="metric-value">{data.researchMetrics.totalPublications}</div>
            <div className="metric-label">Total Publications</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{data.researchMetrics.citations}</div>
            <div className="metric-label">Citations</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{data.researchMetrics.hIndex}</div>
            <div className="metric-label">h-Index</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{data.researchMetrics.i10Index}</div>
            <div className="metric-label">i10-Index</div>
          </div>
        </div>
        
        <div className="publications-grid">
          {data.publications.map((pub, index) => (
            <Card key={index} className="publication-card">
              <CardHeader>
                <div className="publication-icon">
                  <BookOpen className="w-5 h-5" />
                </div>
                <CardTitle className="publication-title">{pub.title}</CardTitle>
                <div className="publication-meta">
                  <Badge variant="secondary">{pub.year}</Badge>
                  <Badge variant="outline">
                    <Quote className="w-3 h-3 mr-1" />
                    {pub.citations} citations
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="publication-journal">{pub.journal}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="research-links">
          <a href={data.googleScholar} target="_blank" rel="noopener noreferrer" className="research-link-btn">
            <ExternalLink className="w-4 h-4 mr-2" />
            View All on Google Scholar
          </a>
          <a href={data.researchgate} target="_blank" rel="noopener noreferrer" className="research-link-btn">
            <ExternalLink className="w-4 h-4 mr-2" />
            ResearchGate Profile
          </a>
        </div>
      </div>
    </section>
  );
};

export default Research;
