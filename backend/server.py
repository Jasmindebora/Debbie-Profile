from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import joblib
import json
import pandas as pd
import numpy as np

from cdss_models import (
    ContactSubmissionCreate,
    ContactSubmission,
    ContactSubmissionResponse,
    ErrorResponse,
    PatientData,
    OutcomePrediction,
    CDSSPredictionResponse,
    ModelPerformance
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="NP-CDSS - Nurse Practitioner Clinical Decision Support System")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load ML models and scalers
MODELS_DIR = Path('models')
ML_MODELS = {}
SCALERS = {}
FEATURE_NAMES = {}

def load_ml_models():
    """Load all trained ML models"""
    outcomes = ['icu_admission', 'intubation', 'cardiac_arrest', 'inotropic_usage']
    
    for outcome in outcomes:
        try:
            # Load Random Forest model (best performing)
            model_path = MODELS_DIR / f'random_forest_{outcome}.pkl'
            scaler_path = MODELS_DIR / f'scaler_{outcome}.pkl'
            features_path = MODELS_DIR / f'features_{outcome}.json'
            
            if model_path.exists():
                ML_MODELS[outcome] = joblib.load(model_path)
                SCALERS[outcome] = joblib.load(scaler_path)
                
                with open(features_path, 'r') as f:
                    FEATURE_NAMES[outcome] = json.load(f)
                
                logger.info(f"Loaded model for {outcome}")
        except Exception as e:
            logger.error(f"Error loading model for {outcome}: {str(e)}")

# Load models at startup
load_ml_models()

# Health check endpoint
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "NP-CDSS API - Active",
        "status": "operational",
        "version": "1.0.0",
        "models_loaded": len(ML_MODELS),
        "available_predictions": list(ML_MODELS.keys())
    }

# Contact form endpoints (existing)
@api_router.post(
    "/contact",
    response_model=ContactSubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
async def submit_contact_form(submission: ContactSubmissionCreate):
    """Submit a contact form message"""
    try:
        contact_data = ContactSubmission(
            name=submission.name,
            email=submission.email,
            subject=submission.subject,
            message=submission.message,
            timestamp=datetime.utcnow(),
            status="new"
        )
        
        result = await db.contact_submissions.insert_one(contact_data.dict())
        logger.info(f"Contact form submitted by {submission.email}")
        
        return ContactSubmissionResponse(
            success=True,
            message="Message sent successfully. Thank you for reaching out!",
            id=contact_data.id
        )
    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form"
        )

@api_router.get("/contact/submissions", response_model=List[ContactSubmission])
async def get_contact_submissions(limit: int = 50, skip: int = 0, status_filter: str = None):
    """Get all contact form submissions"""
    try:
        query = {}
        if status_filter:
            query["status"] = status_filter
        
        submissions = await db.contact_submissions.find(
            query,
            {"_id": 0, "id": 1, "name": 1, "email": 1, "subject": 1, "message": 1, "timestamp": 1, "status": 1}
        ).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
        
        return [ContactSubmission(**sub) for sub in submissions]
    except Exception as e:
        logger.error(f"Error fetching contact submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch contact submissions"
        )

@api_router.get("/contact/count")
async def get_contact_count():
    """Get total count of contact submissions"""
    try:
        total = await db.contact_submissions.count_documents({})
        new = await db.contact_submissions.count_documents({"status": "new"})
        
        return {"total": total, "new": new, "read": total - new}
    except Exception as e:
        logger.error(f"Error counting submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get submission count"
        )

# NP-CDSS Prediction Endpoints
@api_router.post("/cdss/predict", response_model=CDSSPredictionResponse, status_code=status.HTTP_201_CREATED)
async def predict_patient_outcomes(patient: PatientData):
    """
    Predict patient outcomes using ML models
    
    Returns predictions for:
    - ICU Admission
    - Intubation
    - In-Hospital Cardiac Arrest
    - Inotropic Usage
    """
    try:
        # Convert patient data to DataFrame
        patient_dict = patient.dict()
        patient_dict['gender_encoded'] = 1 if patient.gender == 'Male' else 0
        
        patient_df = pd.DataFrame([patient_dict])
        
        predictions = {}
        probabilities = []
        
        outcome_display_names = {
            'icu_admission': 'ICU Admission',
            'intubation': 'Intubation',
            'cardiac_arrest': 'In-Hospital Cardiac Arrest',
            'inotropic_usage': 'Inotropic Usage'
        }
        
        for outcome, model in ML_MODELS.items():
            # Prepare features
            features = FEATURE_NAMES[outcome]
            X = patient_df[features]
            
            # Make prediction
            prediction = int(model.predict(X)[0])
            probability = float(model.predict_proba(X)[0][1])
            probabilities.append(probability)
            
            # Get risk level
            risk_level = get_risk_level(probability)
            
            # Get feature importance (top contributors)
            feature_importance = []
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                for i, feature in enumerate(features):
                    feature_importance.append({
                        'feature': feature,
                        'value': float(X.iloc[0, i]),
                        'importance': float(importances[i])
                    })
                feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            predictions[outcome] = OutcomePrediction(
                outcome_name=outcome_display_names[outcome],
                prediction=prediction,
                probability=probability,
                risk_level=risk_level,
                top_contributors=feature_importance[:10]
            )
        
        # Calculate overall risk score
        overall_risk_score = float(np.mean(probabilities))
        
        # Generate recommendations
        recommendations = generate_recommendations(predictions, patient)
        
        # Save prediction to database
        prediction_record = {
            "patient_data": patient.dict(),
            "predictions": {k: v.dict() for k, v in predictions.items()},
            "overall_risk_score": overall_risk_score,
            "timestamp": datetime.utcnow()
        }
        await db.cdss_predictions.insert_one(prediction_record)
        
        return CDSSPredictionResponse(
            patient_id=f"PT{str(abs(hash(str(patient.dict()))))[:8]}",
            timestamp=datetime.utcnow(),
            predictions=predictions,
            overall_risk_score=overall_risk_score,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to make prediction: {str(e)}"
        )

@api_router.get("/cdss/models/performance")
async def get_model_performance():
    """Get performance metrics for all models"""
    try:
        performance_data = []
        
        for outcome in ML_MODELS.keys():
            results_path = MODELS_DIR / f'results_{outcome}.json'
            if results_path.exists():
                with open(results_path, 'r') as f:
                    results = json.load(f)
                
                # Get Random Forest performance
                if 'Random Forest' in results:
                    metrics = results['Random Forest']['metrics']
                    performance_data.append({
                        'outcome': outcome.replace('_', ' ').title(),
                        'model': 'Random Forest',
                        **metrics
                    })
        
        return {"performance": performance_data}
    except Exception as e:
        logger.error(f"Error fetching model performance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch model performance"
        )

@api_router.get("/cdss/statistics")
async def get_cdss_statistics():
    """Get CDSS usage statistics"""
    try:
        total_predictions = await db.cdss_predictions.count_documents({})
        
        # Get predictions from last 24 hours
        from datetime import timedelta
        last_24h = datetime.utcnow() - timedelta(hours=24)
        recent_predictions = await db.cdss_predictions.count_documents({
            "timestamp": {"$gte": last_24h}
        })
        
        # Get high-risk predictions
        high_risk_count = await db.cdss_predictions.count_documents({
            "overall_risk_score": {"$gte": 0.5}
        })
        
        return {
            "total_predictions": total_predictions,
            "predictions_last_24h": recent_predictions,
            "high_risk_predictions": high_risk_count,
            "models_active": len(ML_MODELS)
        }
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch statistics"
        )

def get_risk_level(probability: float) -> str:
    """Categorize risk level based on probability"""
    if probability < 0.2:
        return 'Low'
    elif probability < 0.5:
        return 'Moderate'
    elif probability < 0.75:
        return 'High'
    else:
        return 'Critical'

def generate_recommendations(predictions: Dict, patient: PatientData) -> List[str]:
    """Generate clinical recommendations based on predictions"""
    recommendations = []
    
    # Check each outcome
    if predictions['icu_admission'].risk_level in ['High', 'Critical']:
        recommendations.append("Consider early ICU consultation and bed reservation")
    
    if predictions['intubation'].risk_level in ['High', 'Critical']:
        recommendations.append("Prepare for possible intubation - ensure airway equipment ready")
        recommendations.append("Consider early respiratory therapy consultation")
    
    if predictions['cardiac_arrest'].risk_level in ['Moderate', 'High', 'Critical']:
        recommendations.append("Ensure continuous cardiac monitoring")
        recommendations.append("Keep resuscitation equipment immediately available")
    
    if predictions['inotropic_usage'].risk_level in ['High', 'Critical']:
        recommendations.append("Monitor blood pressure closely")
        recommendations.append("Prepare vasopressor/inotrope infusions")
    
    # Vital sign-based recommendations
    if patient.spo2 < 92:
        recommendations.append("Initiate supplemental oxygen therapy")
    
    if patient.systolic_bp < 90:
        recommendations.append("Assess for shock - consider fluid resuscitation")
    
    if patient.gcs_score < 13:
        recommendations.append("Frequent neurological assessments required")
    
    if patient.lactate > 4:
        recommendations.append("High lactate detected - assess for sepsis/shock")
    
    if not recommendations:
        recommendations.append("Continue standard ED monitoring and care")
    
    return recommendations

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    client.close()
    logger.info("Database connection closed")

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("NP-CDSS API started successfully")
    logger.info(f"Models loaded: {len(ML_MODELS)}")
