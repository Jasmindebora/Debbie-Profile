import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_synthetic_ed_data(n_samples=10000, seed=42):
    """
    Generate synthetic Emergency Department patient data for NP-CDSS
    Based on Indian tertiary hospital ED characteristics
    """
    np.random.seed(seed)
    random.seed(seed)
    
    data = {}
    
    # Patient Demographics
    data['patient_id'] = [f'ED{str(i).zfill(6)}' for i in range(1, n_samples + 1)]
    data['age'] = np.random.normal(55, 18, n_samples).clip(18, 95).astype(int)
    data['gender'] = np.random.choice(['Male', 'Female'], n_samples, p=[0.55, 0.45])
    
    # Vital Signs (realistic ranges for ED patients)
    data['heart_rate'] = np.random.normal(85, 20, n_samples).clip(40, 180).astype(int)
    data['systolic_bp'] = np.random.normal(135, 25, n_samples).clip(80, 220).astype(int)
    data['diastolic_bp'] = np.random.normal(85, 15, n_samples).clip(50, 130).astype(int)
    data['respiratory_rate'] = np.random.normal(18, 5, n_samples).clip(10, 40).astype(int)
    data['spo2'] = np.random.normal(95, 5, n_samples).clip(70, 100).astype(int)
    data['temperature'] = np.random.normal(98.6, 1.5, n_samples).clip(95, 105).round(1)
    data['gcs_score'] = np.random.choice([15, 14, 13, 12, 11, 10, 9, 8, 7, 6], n_samples, 
                                         p=[0.70, 0.10, 0.05, 0.04, 0.03, 0.03, 0.02, 0.01, 0.01, 0.01])
    
    # Lab Values
    data['wbc_count'] = np.random.normal(9, 4, n_samples).clip(2, 30).round(1)
    data['hemoglobin'] = np.random.normal(12.5, 2.5, n_samples).clip(5, 18).round(1)
    data['platelet_count'] = np.random.normal(250, 80, n_samples).clip(50, 500).astype(int)
    data['creatinine'] = np.random.exponential(1.2, n_samples).clip(0.5, 10).round(2)
    data['sodium'] = np.random.normal(140, 5, n_samples).clip(120, 160).astype(int)
    data['potassium'] = np.random.normal(4.2, 0.6, n_samples).clip(2.5, 7).round(1)
    data['glucose'] = np.random.normal(140, 50, n_samples).clip(50, 500).astype(int)
    data['lactate'] = np.random.exponential(2, n_samples).clip(0.5, 15).round(1)
    
    # Clinical Presentation
    data['chest_pain'] = np.random.choice([0, 1], n_samples, p=[0.70, 0.30])
    data['dyspnea'] = np.random.choice([0, 1], n_samples, p=[0.65, 0.35])
    data['altered_consciousness'] = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    data['seizure'] = np.random.choice([0, 1], n_samples, p=[0.92, 0.08])
    data['abdominal_pain'] = np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
    data['trauma'] = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    
    # Comorbidities
    data['diabetes'] = np.random.choice([0, 1], n_samples, p=[0.65, 0.35])
    data['hypertension'] = np.random.choice([0, 1], n_samples, p=[0.55, 0.45])
    data['cad'] = np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
    data['copd'] = np.random.choice([0, 1], n_samples, p=[0.80, 0.20])
    data['ckd'] = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    data['stroke_history'] = np.random.choice([0, 1], n_samples, p=[0.88, 0.12])
    
    # Triage Category (based on acuity)
    data['triage_category'] = np.random.choice([1, 2, 3, 4, 5], n_samples, 
                                               p=[0.05, 0.20, 0.40, 0.25, 0.10])
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate outcomes based on risk factors (realistic correlations)
    # ICU Admission
    icu_risk = (
        (df['age'] > 65).astype(int) * 0.15 +
        (df['gcs_score'] < 13).astype(int) * 0.25 +
        (df['spo2'] < 92).astype(int) * 0.20 +
        (df['systolic_bp'] < 90).astype(int) * 0.20 +
        (df['lactate'] > 4).astype(int) * 0.18 +
        df['altered_consciousness'] * 0.15 +
        (df['triage_category'] <= 2).astype(int) * 0.20
    )
    df['icu_admission'] = (icu_risk + np.random.normal(0, 0.1, n_samples) > 0.4).astype(int)
    
    # Intubation
    intubation_risk = (
        (df['respiratory_rate'] > 30).astype(int) * 0.20 +
        (df['spo2'] < 88).astype(int) * 0.25 +
        (df['gcs_score'] < 10).astype(int) * 0.30 +
        df['altered_consciousness'] * 0.15 +
        (df['lactate'] > 5).astype(int) * 0.15
    )
    df['intubation'] = (intubation_risk + np.random.normal(0, 0.1, n_samples) > 0.5).astype(int)
    
    # In-Hospital Cardiac Arrest
    cardiac_arrest_risk = (
        (df['age'] > 70).astype(int) * 0.10 +
        (df['systolic_bp'] < 80).astype(int) * 0.20 +
        (df['heart_rate'] > 130).astype(int) * 0.15 +
        (df['potassium'] > 6).astype(int) * 0.20 +
        (df['lactate'] > 6).astype(int) * 0.20 +
        df['cad'] * 0.10 +
        (df['gcs_score'] < 8).astype(int) * 0.15
    )
    df['cardiac_arrest'] = (cardiac_arrest_risk + np.random.normal(0, 0.08, n_samples) > 0.6).astype(int)
    
    # Inotropic Usage
    inotropic_risk = (
        (df['systolic_bp'] < 85).astype(int) * 0.25 +
        (df['lactate'] > 4).astype(int) * 0.20 +
        df['icu_admission'] * 0.20 +
        (df['heart_rate'] > 120).astype(int) * 0.15 +
        (df['age'] > 65).astype(int) * 0.10
    )
    df['inotropic_usage'] = (inotropic_risk + np.random.normal(0, 0.1, n_samples) > 0.5).astype(int)
    
    return df

def prepare_features_targets(df):
    """
    Prepare features and target variables for ML training
    """
    # Feature columns (excluding patient_id and outcomes)
    feature_cols = [
        'age', 'heart_rate', 'systolic_bp', 'diastolic_bp', 'respiratory_rate',
        'spo2', 'temperature', 'gcs_score', 'wbc_count', 'hemoglobin',
        'platelet_count', 'creatinine', 'sodium', 'potassium', 'glucose',
        'lactate', 'chest_pain', 'dyspnea', 'altered_consciousness',
        'seizure', 'abdominal_pain', 'trauma', 'diabetes', 'hypertension',
        'cad', 'copd', 'ckd', 'stroke_history', 'triage_category'
    ]
    
    # Handle gender encoding
    df_processed = df.copy()
    df_processed['gender_encoded'] = (df_processed['gender'] == 'Male').astype(int)
    feature_cols.append('gender_encoded')
    
    # Target columns
    target_cols = ['icu_admission', 'intubation', 'cardiac_arrest', 'inotropic_usage']
    
    X = df_processed[feature_cols]
    y = df_processed[target_cols]
    
    return X, y, feature_cols, target_cols

if __name__ == '__main__':
    # Generate and save synthetic data
    print("Generating synthetic ED data...")
    df = generate_synthetic_ed_data(n_samples=10000)
    
    # Save to CSV
    df.to_csv('synthetic_ed_data.csv', index=False)
    print(f"Generated {len(df)} patient records")
    print(f"\nOutcome distribution:")
    print(f"ICU Admission: {df['icu_admission'].sum()} ({df['icu_admission'].mean()*100:.1f}%)")
    print(f"Intubation: {df['intubation'].sum()} ({df['intubation'].mean()*100:.1f}%)")
    print(f"Cardiac Arrest: {df['cardiac_arrest'].sum()} ({df['cardiac_arrest'].mean()*100:.1f}%)")
    print(f"Inotropic Usage: {df['inotropic_usage'].sum()} ({df['inotropic_usage'].mean()*100:.1f}%)")
