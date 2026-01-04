import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class NPCDSSModel:
    """
    NP-CDSS Machine Learning Model Trainer and Evaluator
    """
    
    def __init__(self, outcome_name, random_state=42):
        self.outcome_name = outcome_name
        self.random_state = random_state
        self.models = {}
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.results = {}
        
    def initialize_models(self):
        """Initialize all ML models for comparison"""
        self.models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'XGBoost': XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                eval_metric='logloss'
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=8,
                min_samples_split=5,
                random_state=self.random_state
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=self.random_state
            ),
            'Naive Bayes': GaussianNB(),
            'Neural Network': MLPClassifier(
                hidden_layer_sizes=(64, 32),
                activation='relu',
                max_iter=500,
                random_state=self.random_state
            )
        }
        
    def prepare_data(self, X, y, test_size=0.2):
        """Split and scale the data"""
        self.feature_names = X.columns.tolist()
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")
        print(f"Positive cases: {self.y_train.sum()} ({self.y_train.mean()*100:.1f}%)")
        
    def train_models(self):
        """Train all models and evaluate performance"""
        print(f"\n{'='*60}")
        print(f"Training models for: {self.outcome_name}")
        print(f"{'='*60}\n")
        
        for model_name, model in self.models.items():
            print(f"Training {model_name}...")
            
            # Train model
            if model_name in ['SVM', 'Neural Network', 'Naive Bayes']:
                model.fit(self.X_train_scaled, self.y_train)
                y_pred = model.predict(self.X_test_scaled)
                y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            else:
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_test)
                y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(self.y_test, y_pred),
                'precision': precision_score(self.y_test, y_pred, zero_division=0),
                'recall': recall_score(self.y_test, y_pred, zero_division=0),
                'f1_score': f1_score(self.y_test, y_pred, zero_division=0),
                'roc_auc': roc_auc_score(self.y_test, y_pred_proba),
                'specificity': self._calculate_specificity(self.y_test, y_pred)
            }
            
            self.results[model_name] = {
                'metrics': metrics,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred).tolist(),
                'classification_report': classification_report(self.y_test, y_pred, output_dict=True)
            }
            
            print(f"  Accuracy: {metrics['accuracy']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall: {metrics['recall']:.4f}")
            print(f"  Specificity: {metrics['specificity']:.4f}")
            print(f"  ROC-AUC: {metrics['roc_auc']:.4f}\n")
        
    def _calculate_specificity(self, y_true, y_pred):
        """Calculate specificity (True Negative Rate)"""
        cm = confusion_matrix(y_true, y_pred)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            return specificity
        return 0
    
    def get_best_model(self):
        """Get the best performing model based on ROC-AUC"""
        best_model_name = max(self.results.items(), 
                             key=lambda x: x[1]['metrics']['roc_auc'])[0]
        return best_model_name, self.models[best_model_name]
    
    def save_models(self, output_dir='models'):
        """Save all trained models and results"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save scaler
        joblib.dump(self.scaler, output_path / f'scaler_{self.outcome_name}.pkl')
        
        # Save each model
        for model_name, model in self.models.items():
            safe_name = model_name.replace(' ', '_').lower()
            joblib.dump(model, output_path / f'{safe_name}_{self.outcome_name}.pkl')
        
        # Save feature names
        with open(output_path / f'features_{self.outcome_name}.json', 'w') as f:
            json.dump(self.feature_names, f)
        
        # Save results
        with open(output_path / f'results_{self.outcome_name}.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Models and results saved to {output_path}/")
        
    def generate_comparison_report(self):
        """Generate a comparison report of all models"""
        report = []
        for model_name, result in self.results.items():
            metrics = result['metrics']
            report.append({
                'model': model_name,
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'specificity': metrics['specificity'],
                'f1_score': metrics['f1_score'],
                'roc_auc': metrics['roc_auc']
            })
        
        df_report = pd.DataFrame(report)
        df_report = df_report.sort_values('roc_auc', ascending=False)
        return df_report

def train_all_outcomes(X, y_dict, output_dir='models'):
    """
    Train models for all outcome variables
    """
    all_results = {}
    
    for outcome_name, y in y_dict.items():
        print(f"\n\n{'#'*70}")
        print(f"# Processing Outcome: {outcome_name.upper()}")
        print(f"{'#'*70}")
        
        # Initialize and train
        cdss_model = NPCDSSModel(outcome_name)
        cdss_model.initialize_models()
        cdss_model.prepare_data(X, y)
        cdss_model.train_models()
        
        # Save models
        cdss_model.save_models(output_dir)
        
        # Get comparison report
        comparison_df = cdss_model.generate_comparison_report()
        print(f"\nModel Comparison for {outcome_name}:")
        print(comparison_df.to_string(index=False))
        
        all_results[outcome_name] = {
            'comparison': comparison_df.to_dict('records'),
            'best_model': cdss_model.get_best_model()[0]
        }
    
    # Save overall results
    with open(Path(output_dir) / 'all_outcomes_summary.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    return all_results

if __name__ == '__main__':
    from data_generator import generate_synthetic_ed_data, prepare_features_targets
    
    print("Generating synthetic data...")
    df = generate_synthetic_ed_data(n_samples=10000)
    
    print("Preparing features and targets...")
    X, y_df, feature_cols, target_cols = prepare_features_targets(df)
    
    # Create dictionary of target variables
    y_dict = {
        'icu_admission': y_df['icu_admission'],
        'intubation': y_df['intubation'],
        'cardiac_arrest': y_df['cardiac_arrest'],
        'inotropic_usage': y_df['inotropic_usage']
    }
    
    # Train models for all outcomes
    results = train_all_outcomes(X, y_dict, output_dir='models')
    
    print("\n\n" + "="*70)
    print("Training Complete!")
    print("="*70)
