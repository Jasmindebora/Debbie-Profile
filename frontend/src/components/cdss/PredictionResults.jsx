import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { AlertTriangle, TrendingUp, Activity, Heart } from 'lucide-react';

const PredictionResults = ({ predictions }) => {
  if (!predictions) return null;

  const getRiskColor = (level) => {
    switch (level) {
      case 'Critical': return 'risk-critical';
      case 'High': return 'risk-high';
      case 'Moderate': return 'risk-moderate';
      case 'Low': return 'risk-low';
      default: return 'risk-low';
    }
  };

  const getOutcomeIcon = (outcome) => {
    switch (outcome) {
      case 'ICU Admission': return <Activity className="w-5 h-5" />;
      case 'Intubation': return <TrendingUp className="w-5 h-5" />;
      case 'In-Hospital Cardiac Arrest': return <Heart className="w-5 h-5" />;
      case 'Inotropic Usage': return <Activity className="w-5 h-5" />;
      default: return <AlertTriangle className="w-5 h-5" />;
    }
  };

  return (
    <div className="prediction-results">
      {/* Overall Risk Score */}
      <Card className="overall-risk-card">
        <CardHeader>
          <CardTitle>Overall Risk Assessment</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overall-risk">
            <div className="risk-score-circle">
              <svg className="risk-progress" viewBox="0 0 100 100">
                <circle
                  className="risk-progress-bg"
                  cx="50"
                  cy="50"
                  r="45"
                />
                <circle
                  className="risk-progress-fill"
                  cx="50"
                  cy="50"
                  r="45"
                  style={{
                    strokeDashoffset: 283 - (283 * predictions.overall_risk_score)
                  }}
                />
              </svg>
              <div className="risk-score-value">
                <span className="score-number">{(predictions.overall_risk_score * 100).toFixed(0)}%</span>
                <span className="score-label">Risk Score</span>
              </div>
            </div>
            <div className="risk-info">
              <p className="patient-id">Patient ID: {predictions.patient_id}</p>
              <p className="timestamp">
                {new Date(predictions.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Individual Outcome Predictions */}
      <div className="outcomes-grid">
        {Object.entries(predictions.predictions).map(([key, pred]) => (
          <Card key={key} className={`outcome-card ${getRiskColor(pred.risk_level)}`}>
            <CardHeader>
              <div className="outcome-header">
                <div className="outcome-icon">
                  {getOutcomeIcon(pred.outcome_name)}
                </div>
                <div>
                  <CardTitle className="outcome-title">{pred.outcome_name}</CardTitle>
                  <Badge className={`risk-badge ${getRiskColor(pred.risk_level)}`}>
                    {pred.risk_level} Risk
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="outcome-probability">
                <div className="probability-label">Probability</div>
                <div className="probability-value">
                  {(pred.probability * 100).toFixed(1)}%
                </div>
              </div>
              <div className="probability-bar">
                <div 
                  className="probability-fill"
                  style={{ width: `${pred.probability * 100}%` }}
                />
              </div>
              
              {/* Top Contributing Factors */}
              {pred.top_contributors && pred.top_contributors.length > 0 && (
                <div className="contributors">
                  <h4 className="contributors-title">Top Contributing Factors</h4>
                  <div className="contributors-list">
                    {pred.top_contributors.slice(0, 5).map((contrib, idx) => (
                      <div key={idx} className="contributor-item">
                        <span className="contributor-feature">
                          {contrib.feature.replace(/_/g, ' ')}
                        </span>
                        <span className="contributor-value">
                          {typeof contrib.value === 'number' ? contrib.value.toFixed(2) : contrib.value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Clinical Recommendations */}
      {predictions.recommendations && predictions.recommendations.length > 0 && (
        <Card className="recommendations-card">
          <CardHeader>
            <CardTitle>
              <AlertTriangle className="w-5 h-5 inline mr-2" />
              Clinical Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="recommendations-list">
              {predictions.recommendations.map((rec, idx) => (
                <li key={idx} className="recommendation-item">
                  <span className="recommendation-bullet">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Disclaimer */}
      <Card className="disclaimer-card">
        <CardContent>
          <div className="disclaimer">
            <AlertTriangle className="w-4 h-4" />
            <p>
              <strong>Clinical Decision Support Tool:</strong> These predictions are meant to assist
              clinical decision-making and should not replace professional medical judgment. Always
              consider the complete clinical picture and patient-specific factors.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PredictionResults;
