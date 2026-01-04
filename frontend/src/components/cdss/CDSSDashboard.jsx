import React, { useState } from 'react';
import { Activity, AlertCircle, TrendingUp, Users } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import PatientForm from './PatientForm';
import PredictionResults from './PredictionResults';
import ModelPerformance from './ModelPerformance';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CDSSDashboard = () => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [statistics, setStatistics] = useState(null);

  React.useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API}/cdss/statistics`);
      setStatistics(response.data);
    } catch (err) {
      console.error('Error fetching statistics:', err);
    }
  };

  const handlePredict = async (patientData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API}/cdss/predict`, patientData);
      setPredictions(response.data);
      fetchStatistics(); // Refresh stats
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to make prediction');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPredictions(null);
    setError(null);
  };

  return (
    <div className="cdss-container">
      {/* Header */}
      <div className="cdss-header">
        <div className="cdss-header-content">
          <div className="cdss-header-icon">
            <Activity className="w-8 h-8" />
          </div>
          <div>
            <h1 className="cdss-title">NP-CDSS</h1>
            <p className="cdss-subtitle">Nurse Practitioner Clinical Decision Support System</p>
          </div>
        </div>
        
        {/* Statistics Cards */}
        {statistics && (
          <div className="cdss-stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <Users className="w-5 h-5" />
              </div>
              <div>
                <div className="stat-value">{statistics.total_predictions}</div>
                <div className="stat-label">Total Predictions</div>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">
                <TrendingUp className="w-5 h-5" />
              </div>
              <div>
                <div className="stat-value">{statistics.predictions_last_24h}</div>
                <div className="stat-label">Last 24 Hours</div>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon alert">
                <AlertCircle className="w-5 h-5" />
              </div>
              <div>
                <div className="stat-value">{statistics.high_risk_predictions}</div>
                <div className="stat-label">High Risk Cases</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="cdss-content">
        <Tabs defaultValue="predict" className="cdss-tabs">
          <TabsList className="tabs-list">
            <TabsTrigger value="predict">Patient Assessment</TabsTrigger>
            <TabsTrigger value="performance">Model Performance</TabsTrigger>
          </TabsList>

          <TabsContent value="predict" className="tabs-content">
            <div className="cdss-grid">
              {/* Patient Input Form */}
              <div className="cdss-form-section">
                <Card>
                  <CardHeader>
                    <CardTitle>Patient Data Input</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <PatientForm 
                      onSubmit={handlePredict} 
                      onReset={handleReset}
                      loading={loading}
                    />
                  </CardContent>
                </Card>
              </div>

              {/* Prediction Results */}
              <div className="cdss-results-section">
                {error && (
                  <Card className="error-card">
                    <CardContent>
                      <div className="error-message">
                        <AlertCircle className="w-5 h-5" />
                        <span>{error}</span>
                      </div>
                    </CardContent>
                  </Card>
                )}
                
                {loading && (
                  <Card>
                    <CardContent>
                      <div className="loading-state">
                        <div className="spinner"></div>
                        <p>Analyzing patient data and generating predictions...</p>
                      </div>
                    </CardContent>
                  </Card>
                )}
                
                {predictions && !loading && (
                  <PredictionResults predictions={predictions} />
                )}
                
                {!predictions && !loading && !error && (
                  <Card>
                    <CardContent>
                      <div className="empty-state">
                        <Activity className="w-16 h-16 empty-icon" />
                        <h3>Ready for Assessment</h3>
                        <p>Enter patient data and click "Generate Prediction" to analyze risk factors and receive clinical recommendations.</p>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="performance" className="tabs-content">
            <ModelPerformance />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default CDSSDashboard;
