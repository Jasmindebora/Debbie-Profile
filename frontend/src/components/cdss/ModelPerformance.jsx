import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { TrendingUp, Award, Target } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ModelPerformance = () => {
  const [performance, setPerformance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPerformance();
  }, []);

  const fetchPerformance = async () => {
    try {
      const response = await axios.get(`${API}/cdss/models/performance`);
      setPerformance(response.data.performance || []);
    } catch (err) {
      console.error('Error fetching performance:', err);
    } finally {
      setLoading(false);
    }
  };

  const getMetricColor = (value) => {
    if (value >= 0.9) return 'metric-excellent';
    if (value >= 0.8) return 'metric-good';
    if (value >= 0.7) return 'metric-fair';
    return 'metric-poor';
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading model performance metrics...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="model-performance">
      <Card className="performance-intro">
        <CardHeader>
          <CardTitle>
            <Award className="w-6 h-6 inline mr-2" />
            Model Performance Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="performance-description">
            Our NP-CDSS uses Random Forest models trained on 8,000 synthetic Emergency Department
            patient records. Models are evaluated using standard classification metrics to ensure
            reliable clinical predictions.
          </p>
        </CardContent>
      </Card>

      <div className="performance-grid">
        {performance.map((perf, idx) => (
          <Card key={idx} className="performance-card">
            <CardHeader>
              <div className="performance-header">
                <Target className="w-5 h-5" />
                <CardTitle className="outcome-name">{perf.outcome}</CardTitle>
              </div>
              <Badge className="model-badge">{perf.model}</Badge>
            </CardHeader>
            <CardContent>
              <div className="metrics-grid">
                <div className="metric-item">
                  <div className="metric-label">Accuracy</div>
                  <div className={`metric-value ${getMetricColor(perf.accuracy)}`}>
                    {(perf.accuracy * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.accuracy * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-item">
                  <div className="metric-label">Precision</div>
                  <div className={`metric-value ${getMetricColor(perf.precision)}`}>
                    {(perf.precision * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.precision * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-item">
                  <div className="metric-label">Recall (Sensitivity)</div>
                  <div className={`metric-value ${getMetricColor(perf.recall)}`}>
                    {(perf.recall * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.recall * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-item">
                  <div className="metric-label">Specificity</div>
                  <div className={`metric-value ${getMetricColor(perf.specificity)}`}>
                    {(perf.specificity * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.specificity * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-item">
                  <div className="metric-label">F1 Score</div>
                  <div className={`metric-value ${getMetricColor(perf.f1_score)}`}>
                    {(perf.f1_score * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.f1_score * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-item">
                  <div className="metric-label">ROC-AUC</div>
                  <div className={`metric-value ${getMetricColor(perf.roc_auc)}`}>
                    {(perf.roc_auc * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div 
                      className="metric-fill"
                      style={{ width: `${perf.roc_auc * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Metrics Explanation */}
      <Card className="metrics-explanation">
        <CardHeader>
          <CardTitle>Understanding the Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="explanation-grid">
            <div className="explanation-item">
              <strong>Accuracy:</strong> Overall correctness of predictions (correct predictions / total predictions)
            </div>
            <div className="explanation-item">
              <strong>Precision:</strong> Of all positive predictions, how many were actually positive (reduces false alarms)
            </div>
            <div className="explanation-item">
              <strong>Recall/Sensitivity:</strong> Of all actual positive cases, how many were correctly identified (reduces missed cases)
            </div>
            <div className="explanation-item">
              <strong>Specificity:</strong> Of all actual negative cases, how many were correctly identified as negative
            </div>
            <div className="explanation-item">
              <strong>F1 Score:</strong> Harmonic mean of precision and recall (balances both metrics)
            </div>
            <div className="explanation-item">
              <strong>ROC-AUC:</strong> Model's ability to distinguish between classes (higher is better, max = 1.0)
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ModelPerformance;
