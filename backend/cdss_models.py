from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
import uuid

# Existing models
class ContactSubmissionCreate(BaseModel):
    """Model for creating a new contact submission"""
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('subject')
    def subject_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Subject cannot be empty')
        return v.strip()
    
    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ContactSubmission(BaseModel):
    """Complete contact submission model with metadata"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    subject: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContactSubmissionResponse(BaseModel):
    """Response model for contact submission"""
    success: bool
    message: str
    id: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str

# NP-CDSS Models
class PatientData(BaseModel):
    """Patient data input for NP-CDSS prediction"""
    # Demographics
    age: int = Field(..., ge=18, le=120, description="Patient age in years")
    gender: str = Field(..., description="Patient gender (Male/Female)")
    
    # Vital Signs
    heart_rate: int = Field(..., ge=30, le=200, description="Heart rate (bpm)")
    systolic_bp: int = Field(..., ge=60, le=250, description="Systolic BP (mmHg)")
    diastolic_bp: int = Field(..., ge=30, le=150, description="Diastolic BP (mmHg)")
    respiratory_rate: int = Field(..., ge=5, le=50, description="Respiratory rate (breaths/min)")
    spo2: int = Field(..., ge=50, le=100, description="Oxygen saturation (%)")
    temperature: float = Field(..., ge=90, le=110, description="Temperature (°F)")
    gcs_score: int = Field(..., ge=3, le=15, description="Glasgow Coma Scale")
    
    # Lab Values
    wbc_count: float = Field(..., ge=0, le=50, description="WBC count (×10³/μL)")
    hemoglobin: float = Field(..., ge=3, le=20, description="Hemoglobin (g/dL)")
    platelet_count: int = Field(..., ge=10, le=1000, description="Platelet count (×10³/μL)")
    creatinine: float = Field(..., ge=0.1, le=15, description="Creatinine (mg/dL)")
    sodium: int = Field(..., ge=110, le=170, description="Sodium (mEq/L)")
    potassium: float = Field(..., ge=2, le=8, description="Potassium (mEq/L)")
    glucose: int = Field(..., ge=30, le=600, description="Glucose (mg/dL)")
    lactate: float = Field(..., ge=0, le=20, description="Lactate (mmol/L)")
    
    # Clinical Presentation
    chest_pain: int = Field(..., ge=0, le=1, description="Chest pain (0=No, 1=Yes)")
    dyspnea: int = Field(..., ge=0, le=1, description="Dyspnea (0=No, 1=Yes)")
    altered_consciousness: int = Field(..., ge=0, le=1, description="Altered consciousness (0=No, 1=Yes)")
    seizure: int = Field(..., ge=0, le=1, description="Seizure (0=No, 1=Yes)")
    abdominal_pain: int = Field(..., ge=0, le=1, description="Abdominal pain (0=No, 1=Yes)")
    trauma: int = Field(..., ge=0, le=1, description="Trauma (0=No, 1=Yes)")
    
    # Comorbidities
    diabetes: int = Field(..., ge=0, le=1, description="Diabetes (0=No, 1=Yes)")
    hypertension: int = Field(..., ge=0, le=1, description="Hypertension (0=No, 1=Yes)")
    cad: int = Field(..., ge=0, le=1, description="Coronary artery disease (0=No, 1=Yes)")
    copd: int = Field(..., ge=0, le=1, description="COPD (0=No, 1=Yes)")
    ckd: int = Field(..., ge=0, le=1, description="Chronic kidney disease (0=No, 1=Yes)")
    stroke_history: int = Field(..., ge=0, le=1, description="Stroke history (0=No, 1=Yes)")
    
    # Triage
    triage_category: int = Field(..., ge=1, le=5, description="Triage category (1=Critical, 5=Non-urgent)")

class OutcomePrediction(BaseModel):
    """Prediction for a single outcome"""
    outcome_name: str
    prediction: int  # 0 or 1
    probability: float  # 0 to 1
    risk_level: str  # Low, Moderate, High, Critical
    top_contributors: List[Dict]

class CDSSPredictionResponse(BaseModel):
    """Complete CDSS prediction response"""
    patient_id: str
    timestamp: datetime
    predictions: Dict[str, OutcomePrediction]
    overall_risk_score: float
    recommendations: List[str]

class ModelPerformance(BaseModel):
    """Model performance metrics"""
    model_name: str
    outcome: str
    accuracy: float
    precision: float
    recall: float
    specificity: float
    f1_score: float
    roc_auc: float
