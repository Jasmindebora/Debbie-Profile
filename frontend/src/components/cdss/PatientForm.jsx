import React, { useState } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { samplePatients, defaultPatientData } from '../../cdss_mock';
import { Activity, RotateCcw } from 'lucide-react';

const PatientForm = ({ onSubmit, onReset, loading }) => {
  const [formData, setFormData] = useState(defaultPatientData);

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const loadSamplePatient = (sample) => {
    setFormData(sample.data);
  };

  const resetForm = () => {
    setFormData(defaultPatientData);
    onReset();
  };

  return (
    <form onSubmit={handleSubmit} className="patient-form">
      {/* Sample Patients */}
      <div className="sample-patients">
        <Label>Quick Load Sample Patients:</Label>
        <div className="sample-buttons">
          {samplePatients.map(sample => (
            <Button
              key={sample.id}
              type="button"
              variant="outline"
              size="sm"
              onClick={() => loadSamplePatient(sample)}
              className="sample-btn"
            >
              {sample.name}
            </Button>
          ))}
        </div>
      </div>

      <Tabs defaultValue="demographics" className="form-tabs">
        <TabsList className="grid grid-cols-5 w-full">
          <TabsTrigger value="demographics">Demographics</TabsTrigger>
          <TabsTrigger value="vitals">Vital Signs</TabsTrigger>
          <TabsTrigger value="labs">Lab Values</TabsTrigger>
          <TabsTrigger value="clinical">Clinical</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>

        {/* Demographics */}
        <TabsContent value="demographics" className="form-section">
          <div className="form-grid">
            <div className="form-field">
              <Label htmlFor="age">Age (years)</Label>
              <Input
                id="age"
                type="number"
                min="18"
                max="120"
                value={formData.age}
                onChange={(e) => handleChange('age', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="gender">Gender</Label>
              <Select value={formData.gender} onValueChange={(value) => handleChange('gender', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Male">Male</SelectItem>
                  <SelectItem value="Female">Female</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="form-field">
              <Label htmlFor="triage">Triage Category</Label>
              <Select 
                value={formData.triage_category.toString()} 
                onValueChange={(value) => handleChange('triage_category', parseInt(value))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1 - Critical</SelectItem>
                  <SelectItem value="2">2 - Emergency</SelectItem>
                  <SelectItem value="3">3 - Urgent</SelectItem>
                  <SelectItem value="4">4 - Semi-Urgent</SelectItem>
                  <SelectItem value="5">5 - Non-Urgent</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </TabsContent>

        {/* Vital Signs */}
        <TabsContent value="vitals" className="form-section">
          <div className="form-grid">
            <div className="form-field">
              <Label htmlFor="hr">Heart Rate (bpm)</Label>
              <Input
                id="hr"
                type="number"
                min="30"
                max="200"
                value={formData.heart_rate}
                onChange={(e) => handleChange('heart_rate', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="sbp">Systolic BP (mmHg)</Label>
              <Input
                id="sbp"
                type="number"
                min="60"
                max="250"
                value={formData.systolic_bp}
                onChange={(e) => handleChange('systolic_bp', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="dbp">Diastolic BP (mmHg)</Label>
              <Input
                id="dbp"
                type="number"
                min="30"
                max="150"
                value={formData.diastolic_bp}
                onChange={(e) => handleChange('diastolic_bp', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="rr">Respiratory Rate (breaths/min)</Label>
              <Input
                id="rr"
                type="number"
                min="5"
                max="50"
                value={formData.respiratory_rate}
                onChange={(e) => handleChange('respiratory_rate', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="spo2">SpO2 (%)</Label>
              <Input
                id="spo2"
                type="number"
                min="50"
                max="100"
                value={formData.spo2}
                onChange={(e) => handleChange('spo2', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="temp">Temperature (°F)</Label>
              <Input
                id="temp"
                type="number"
                step="0.1"
                min="90"
                max="110"
                value={formData.temperature}
                onChange={(e) => handleChange('temperature', parseFloat(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="gcs">GCS Score</Label>
              <Select 
                value={formData.gcs_score.toString()} 
                onValueChange={(value) => handleChange('gcs_score', parseInt(value))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {[15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3].map(score => (
                    <SelectItem key={score} value={score.toString()}>{score}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </TabsContent>

        {/* Lab Values */}
        <TabsContent value="labs" className="form-section">
          <div className="form-grid">
            <div className="form-field">
              <Label htmlFor="wbc">WBC Count (×10³/μL)</Label>
              <Input
                id="wbc"
                type="number"
                step="0.1"
                min="0"
                max="50"
                value={formData.wbc_count}
                onChange={(e) => handleChange('wbc_count', parseFloat(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="hgb">Hemoglobin (g/dL)</Label>
              <Input
                id="hgb"
                type="number"
                step="0.1"
                min="3"
                max="20"
                value={formData.hemoglobin}
                onChange={(e) => handleChange('hemoglobin', parseFloat(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="plt">Platelet Count (×10³/μL)</Label>
              <Input
                id="plt"
                type="number"
                min="10"
                max="1000"
                value={formData.platelet_count}
                onChange={(e) => handleChange('platelet_count', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="cr">Creatinine (mg/dL)</Label>
              <Input
                id="cr"
                type="number"
                step="0.01"
                min="0.1"
                max="15"
                value={formData.creatinine}
                onChange={(e) => handleChange('creatinine', parseFloat(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="na">Sodium (mEq/L)</Label>
              <Input
                id="na"
                type="number"
                min="110"
                max="170"
                value={formData.sodium}
                onChange={(e) => handleChange('sodium', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="k">Potassium (mEq/L)</Label>
              <Input
                id="k"
                type="number"
                step="0.1"
                min="2"
                max="8"
                value={formData.potassium}
                onChange={(e) => handleChange('potassium', parseFloat(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="glucose">Glucose (mg/dL)</Label>
              <Input
                id="glucose"
                type="number"
                min="30"
                max="600"
                value={formData.glucose}
                onChange={(e) => handleChange('glucose', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-field">
              <Label htmlFor="lactate">Lactate (mmol/L)</Label>
              <Input
                id="lactate"
                type="number"
                step="0.1"
                min="0"
                max="20"
                value={formData.lactate}
                onChange={(e) => handleChange('lactate', parseFloat(e.target.value))}
                required
              />
            </div>
          </div>
        </TabsContent>

        {/* Clinical Presentation */}
        <TabsContent value="clinical" className="form-section">
          <div className="checkbox-grid">
            {[
              { key: 'chest_pain', label: 'Chest Pain' },
              { key: 'dyspnea', label: 'Dyspnea' },
              { key: 'altered_consciousness', label: 'Altered Consciousness' },
              { key: 'seizure', label: 'Seizure' },
              { key: 'abdominal_pain', label: 'Abdominal Pain' },
              { key: 'trauma', label: 'Trauma' }
            ].map(item => (
              <div key={item.key} className="checkbox-field">
                <input
                  type="checkbox"
                  id={item.key}
                  checked={formData[item.key] === 1}
                  onChange={(e) => handleChange(item.key, e.target.checked ? 1 : 0)}
                />
                <Label htmlFor={item.key}>{item.label}</Label>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* Medical History */}
        <TabsContent value="history" className="form-section">
          <div className="checkbox-grid">
            {[
              { key: 'diabetes', label: 'Diabetes Mellitus' },
              { key: 'hypertension', label: 'Hypertension' },
              { key: 'cad', label: 'Coronary Artery Disease' },
              { key: 'copd', label: 'COPD' },
              { key: 'ckd', label: 'Chronic Kidney Disease' },
              { key: 'stroke_history', label: 'Stroke History' }
            ].map(item => (
              <div key={item.key} className="checkbox-field">
                <input
                  type="checkbox"
                  id={item.key}
                  checked={formData[item.key] === 1}
                  onChange={(e) => handleChange(item.key, e.target.checked ? 1 : 0)}
                />
                <Label htmlFor={item.key}>{item.label}</Label>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Action Buttons */}
      <div className="form-actions">
        <Button type="button" variant="outline" onClick={resetForm} disabled={loading}>
          <RotateCcw className="w-4 h-4 mr-2" />
          Reset Form
        </Button>
        <Button type="submit" disabled={loading} className="btn-primary">
          <Activity className="w-4 h-4 mr-2" />
          {loading ? 'Analyzing...' : 'Generate Prediction'}
        </Button>
      </div>
    </form>
  );
};

export default PatientForm;
