import numpy as np
import pandas as pd
import joblib
import json
import shap
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from pathlib import Path

class CDSSExplainer:
    """
    SHAP-based explainability for NP-CDSS predictions
    """
    
    def __init__(self, model_path, scaler_path, features_path):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        with open(features_path, 'r') as f:
            self.feature_names = json.load(f)
        
        self.explainer = None
        self._initialize_explainer()
    
    def _initialize_explainer(self):
        """Initialize SHAP explainer based on model type"""
        model_type = type(self.model).__name__
        
        if 'RandomForest' in model_type or 'XGB' in model_type or 'DecisionTree' in model_type:
            self.explainer = shap.TreeExplainer(self.model)
        else:
            # For SVM, Neural Network, etc., use KernelExplainer with background data
            # We'll create a small background dataset
            background = shap.sample(np.zeros((100, len(self.feature_names))), 100)
            self.explainer = shap.KernelExplainer(self.model.predict_proba, background)
    
    def explain_prediction(self, patient_data, top_n=10):
        """
        Generate SHAP explanations for a single patient prediction
        
        Args:
            patient_data: dict or DataFrame with patient features
            top_n: number of top features to return
            
        Returns:
            dict with prediction, probability, and feature contributions
        """
        # Convert to DataFrame if dict
        if isinstance(patient_data, dict):
            df = pd.DataFrame([patient_data])
        else:
            df = patient_data
        
        # Ensure all required features are present
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        # Select and order features
        X = df[self.feature_names]
        
        # Get prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X)
        
        # For binary classification, get positive class SHAP values
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Positive class
        
        # Get feature contributions
        feature_contributions = []
        for i, feature in enumerate(self.feature_names):
            contribution = float(shap_values[0][i])
            feature_contributions.append({
                'feature': feature,
                'value': float(X.iloc[0][i]),
                'contribution': contribution,
                'abs_contribution': abs(contribution)
            })
        
        # Sort by absolute contribution
        feature_contributions.sort(key=lambda x: x['abs_contribution'], reverse=True)
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': self._get_risk_level(probability),
            'top_contributors': feature_contributions[:top_n],
            'all_contributions': feature_contributions
        }
    
    def _get_risk_level(self, probability):
        """Categorize risk level based on probability"""
        if probability < 0.2:
            return 'Low'
        elif probability < 0.5:
            return 'Moderate'
        elif probability < 0.75:
            return 'High'
        else:
            return 'Critical'
    
    def generate_force_plot(self, patient_data):
        """
        Generate SHAP force plot for a patient
        Returns base64 encoded image
        """
        if isinstance(patient_data, dict):
            df = pd.DataFrame([patient_data])
        else:
            df = patient_data
        
        # Ensure all required features are present
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        X = df[self.feature_names]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Create force plot
        plt.figure(figsize=(20, 3))
        shap.force_plot(
            self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value,
            shap_values[0],
            X.iloc[0],
            matplotlib=True,
            show=False
        )
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def generate_waterfall_plot(self, patient_data, outcome_name='Outcome'):
        """
        Generate SHAP waterfall plot showing top feature contributions
        Returns base64 encoded image
        """
        if isinstance(patient_data, dict):
            df = pd.DataFrame([patient_data])
        else:
            df = patient_data
        
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        X = df[self.feature_names]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Create explanation object
        if isinstance(self.explainer.expected_value, list):
            base_value = self.explainer.expected_value[1]
        else:
            base_value = self.explainer.expected_value
        
        explanation = shap.Explanation(
            values=shap_values[0],
            base_values=base_value,
            data=X.iloc[0].values,
            feature_names=self.feature_names
        )
        
        # Create waterfall plot
        plt.figure(figsize=(10, 8))
        shap.waterfall_plot(explanation, max_display=15, show=False)
        plt.title(f'SHAP Waterfall Plot - {outcome_name}', fontsize=14, fontweight='bold')
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

class MultiOutcomeExplainer:
    """
    Explainer for all four outcomes
    """
    
    def __init__(self, models_dir='models'):
        self.models_dir = Path(models_dir)
        self.explainers = {}
        self.outcomes = ['icu_admission', 'intubation', 'cardiac_arrest', 'inotropic_usage']
        
        # Initialize explainers for each outcome (using best model - Random Forest)
        for outcome in self.outcomes:
            model_path = self.models_dir / f'random_forest_{outcome}.pkl'
            scaler_path = self.models_dir / f'scaler_{outcome}.pkl'
            features_path = self.models_dir / f'features_{outcome}.json'
            
            if model_path.exists():
                self.explainers[outcome] = CDSSExplainer(
                    str(model_path),
                    str(scaler_path),
                    str(features_path)
                )
    
    def explain_all_outcomes(self, patient_data):
        """
        Generate explanations for all outcomes
        """
        results = {}
        
        for outcome, explainer in self.explainers.items():
            try:
                explanation = explainer.explain_prediction(patient_data, top_n=10)
                results[outcome] = explanation
            except Exception as e:
                results[outcome] = {'error': str(e)}
        
        return results
    
    def get_waterfall_plots(self, patient_data):
        """
        Generate waterfall plots for all outcomes
        """
        plots = {}
        
        outcome_names = {
            'icu_admission': 'ICU Admission',
            'intubation': 'Intubation',
            'cardiac_arrest': 'Cardiac Arrest',
            'inotropic_usage': 'Inotropic Usage'
        }
        
        for outcome, explainer in self.explainers.items():
            try:
                plot = explainer.generate_waterfall_plot(patient_data, outcome_names[outcome])
                plots[outcome] = plot
            except Exception as e:
                plots[outcome] = None
        
        return plots
