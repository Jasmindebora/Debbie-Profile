#!/usr/bin/env python3
"""
Backend API Testing for NP-CDSS and Portfolio Website
Tests all API endpoints including health check, contact form, admin endpoints, and CDSS prediction endpoints
"""

import requests
import json
import os
from datetime import datetime
import time

# Load environment variables
def load_env_vars():
    """Load environment variables from frontend/.env"""
    env_path = "/app/frontend/.env"
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value.strip('"')
        return env_vars
    except Exception as e:
        print(f"Error loading environment variables: {e}")
        return {}

# Get backend URL
env_vars = load_env_vars()
BACKEND_URL = env_vars.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing backend API at: {API_BASE_URL}")

class BackendTester:
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        self.passed_tests = []
        
    def log_test(self, test_name, success, details=""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests.append(test_name)
            print(f"✅ PASS: {test_name}")
        else:
            self.failed_tests.append(test_name)
            print(f"❌ FAIL: {test_name} - {details}")
            
        if details:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test GET /api/ health check endpoint"""
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["message", "status", "version", "models_loaded", "available_predictions"]
                
                if all(key in data for key in expected_keys):
                    if data.get("status") == "operational":
                        models_loaded = data.get("models_loaded", 0)
                        available_predictions = data.get("available_predictions", [])
                        self.log_test("Health Check", True, f"Status: {data.get('status')}, Version: {data.get('version')}, Models: {models_loaded}, Predictions: {available_predictions}")
                    else:
                        self.log_test("Health Check", False, f"Status not operational: {data.get('status')}")
                else:
                    self.log_test("Health Check", False, f"Missing expected keys. Got: {list(data.keys())}")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
    
    def test_contact_form_valid_submission(self):
        """Test POST /api/contact with valid data"""
        valid_data = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "subject": "Collaboration Opportunity",
            "message": "Hello Dr. Jasmin, I would like to discuss a potential research collaboration in AI healthcare."
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/contact",
                json=valid_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                expected_keys = ["success", "message", "id"]
                
                if all(key in data for key in expected_keys):
                    if data.get("success") is True and data.get("id"):
                        self.log_test("Contact Form Valid Submission", True, f"Message ID: {data.get('id')}")
                        return data.get("id")  # Return ID for database verification
                    else:
                        self.log_test("Contact Form Valid Submission", False, f"Invalid response data: {data}")
                else:
                    self.log_test("Contact Form Valid Submission", False, f"Missing expected keys. Got: {list(data.keys())}")
            else:
                self.log_test("Contact Form Valid Submission", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Form Valid Submission", False, f"Request failed: {str(e)}")
        
        return None
    
    def test_contact_form_validation_errors(self):
        """Test POST /api/contact with various invalid data"""
        
        # Test invalid email format
        invalid_email_data = {
            "name": "John Smith",
            "email": "invalid-email",
            "subject": "Test Subject",
            "message": "This is a test message with enough characters."
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/contact",
                json=invalid_email_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 422:
                self.log_test("Contact Form Invalid Email", True, "Validation error returned as expected")
            else:
                self.log_test("Contact Form Invalid Email", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Invalid Email", False, f"Request failed: {str(e)}")
        
        # Test missing required fields
        missing_fields_data = {
            "name": "",
            "email": "test@example.com",
            "subject": "",
            "message": ""
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/contact",
                json=missing_fields_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 422:
                self.log_test("Contact Form Missing Fields", True, "Validation error returned as expected")
            else:
                self.log_test("Contact Form Missing Fields", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Missing Fields", False, f"Request failed: {str(e)}")
        
        # Test message too short
        short_message_data = {
            "name": "John Smith",
            "email": "john@example.com",
            "subject": "Test",
            "message": "Short"  # Less than 10 characters
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/contact",
                json=short_message_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 422:
                self.log_test("Contact Form Short Message", True, "Validation error returned as expected")
            else:
                self.log_test("Contact Form Short Message", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Short Message", False, f"Request failed: {str(e)}")
    
    def test_get_contact_submissions(self):
        """Test GET /api/contact/submissions (admin endpoint)"""
        try:
            # Test without parameters
            response = requests.get(f"{API_BASE_URL}/contact/submissions", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Contact Submissions", True, f"Retrieved {len(data)} submissions")
                else:
                    self.log_test("Get Contact Submissions", False, f"Expected list, got {type(data)}")
            else:
                self.log_test("Get Contact Submissions", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Contact Submissions", False, f"Request failed: {str(e)}")
        
        # Test with query parameters
        try:
            params = {"limit": 10, "skip": 0}
            response = requests.get(f"{API_BASE_URL}/contact/submissions", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) <= 10:
                    self.log_test("Get Contact Submissions with Params", True, f"Retrieved {len(data)} submissions with limit=10")
                else:
                    self.log_test("Get Contact Submissions with Params", False, f"Unexpected response: {len(data) if isinstance(data, list) else type(data)}")
            else:
                self.log_test("Get Contact Submissions with Params", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Contact Submissions with Params", False, f"Request failed: {str(e)}")
    
    def test_get_contact_count(self):
        """Test GET /api/contact/count"""
        try:
            response = requests.get(f"{API_BASE_URL}/contact/count", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["total", "new", "read"]
                
                if all(key in data for key in expected_keys):
                    if all(isinstance(data[key], int) for key in expected_keys):
                        self.log_test("Get Contact Count", True, f"Total: {data['total']}, New: {data['new']}, Read: {data['read']}")
                    else:
                        self.log_test("Get Contact Count", False, f"Non-integer values in response: {data}")
                else:
                    self.log_test("Get Contact Count", False, f"Missing expected keys. Got: {list(data.keys())}")
            else:
                self.log_test("Get Contact Count", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Contact Count", False, f"Request failed: {str(e)}")
    
    def verify_database_storage(self, submission_id):
        """Verify that data is properly stored in MongoDB by checking submissions endpoint"""
        if not submission_id:
            self.log_test("Database Storage Verification", False, "No submission ID to verify")
            return
        
        try:
            # Get all submissions and look for our submission
            response = requests.get(f"{API_BASE_URL}/contact/submissions", timeout=10)
            
            if response.status_code == 200:
                submissions = response.json()
                found_submission = None
                
                for submission in submissions:
                    if submission.get("id") == submission_id:
                        found_submission = submission
                        break
                
                if found_submission:
                    # Verify required fields
                    required_fields = ["id", "name", "email", "subject", "message", "timestamp", "status"]
                    if all(field in found_submission for field in required_fields):
                        if found_submission.get("status") == "new":
                            self.log_test("Database Storage Verification", True, f"Submission found with correct status: {found_submission.get('status')}")
                        else:
                            self.log_test("Database Storage Verification", False, f"Incorrect default status: {found_submission.get('status')}")
                    else:
                        missing_fields = [field for field in required_fields if field not in found_submission]
                        self.log_test("Database Storage Verification", False, f"Missing fields: {missing_fields}")
                else:
                    self.log_test("Database Storage Verification", False, f"Submission with ID {submission_id} not found in database")
            else:
                self.log_test("Database Storage Verification", False, f"Failed to retrieve submissions: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Database Storage Verification", False, f"Request failed: {str(e)}")
    
    def test_cdss_predict_high_risk_patient(self):
        """Test POST /api/cdss/predict with high-risk patient data"""
        high_risk_patient = {
            "age": 75,
            "gender": "Male",
            "heart_rate": 125,
            "systolic_bp": 85,
            "diastolic_bp": 55,
            "respiratory_rate": 28,
            "spo2": 88,
            "temperature": 101.5,
            "gcs_score": 12,
            "wbc_count": 18.5,
            "hemoglobin": 9.2,
            "platelet_count": 120,
            "creatinine": 2.8,
            "sodium": 132,
            "potassium": 5.8,
            "glucose": 280,
            "lactate": 5.2,
            "chest_pain": 1,
            "dyspnea": 1,
            "altered_consciousness": 1,
            "seizure": 0,
            "abdominal_pain": 0,
            "trauma": 0,
            "diabetes": 1,
            "hypertension": 1,
            "cad": 1,
            "copd": 1,
            "ckd": 1,
            "stroke_history": 0,
            "triage_category": 1
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/cdss/predict",
                json=high_risk_patient,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                expected_keys = ["patient_id", "timestamp", "predictions", "overall_risk_score", "recommendations"]
                
                if all(key in data for key in expected_keys):
                    predictions = data.get("predictions", {})
                    expected_outcomes = ["icu_admission", "intubation", "cardiac_arrest", "inotropic_usage"]
                    
                    # Check all 4 outcomes are present
                    if all(outcome in predictions for outcome in expected_outcomes):
                        # Validate prediction structure
                        valid_predictions = True
                        for outcome, prediction in predictions.items():
                            if not all(key in prediction for key in ["outcome_name", "prediction", "probability", "risk_level"]):
                                valid_predictions = False
                                break
                            
                            # Check probability is between 0 and 1
                            prob = prediction.get("probability", -1)
                            if not (0 <= prob <= 1):
                                valid_predictions = False
                                break
                            
                            # Check risk level is valid
                            risk_level = prediction.get("risk_level", "")
                            if risk_level not in ["Low", "Moderate", "High", "Critical"]:
                                valid_predictions = False
                                break
                        
                        if valid_predictions:
                            overall_risk = data.get("overall_risk_score", -1)
                            recommendations = data.get("recommendations", [])
                            
                            if 0 <= overall_risk <= 1 and isinstance(recommendations, list) and len(recommendations) > 0:
                                self.log_test("CDSS High-Risk Patient Prediction", True, 
                                            f"All 4 outcomes predicted, Overall risk: {overall_risk:.3f}, Recommendations: {len(recommendations)}")
                                return data.get("patient_id")
                            else:
                                self.log_test("CDSS High-Risk Patient Prediction", False, 
                                            f"Invalid overall risk score ({overall_risk}) or empty recommendations")
                        else:
                            self.log_test("CDSS High-Risk Patient Prediction", False, "Invalid prediction structure or values")
                    else:
                        missing_outcomes = [o for o in expected_outcomes if o not in predictions]
                        self.log_test("CDSS High-Risk Patient Prediction", False, f"Missing outcomes: {missing_outcomes}")
                else:
                    self.log_test("CDSS High-Risk Patient Prediction", False, f"Missing expected keys. Got: {list(data.keys())}")
            else:
                self.log_test("CDSS High-Risk Patient Prediction", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("CDSS High-Risk Patient Prediction", False, f"Request failed: {str(e)}")
        
        return None
    
    def test_cdss_predict_low_risk_patient(self):
        """Test POST /api/cdss/predict with low-risk patient data"""
        low_risk_patient = {
            "age": 35,
            "gender": "Female",
            "heart_rate": 80,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "respiratory_rate": 16,
            "spo2": 98,
            "temperature": 98.6,
            "gcs_score": 15,
            "wbc_count": 7.5,
            "hemoglobin": 13.5,
            "platelet_count": 250,
            "creatinine": 0.9,
            "sodium": 140,
            "potassium": 4.0,
            "glucose": 95,
            "lactate": 1.2,
            "chest_pain": 0,
            "dyspnea": 0,
            "altered_consciousness": 0,
            "seizure": 0,
            "abdominal_pain": 1,
            "trauma": 0,
            "diabetes": 0,
            "hypertension": 0,
            "cad": 0,
            "copd": 0,
            "ckd": 0,
            "stroke_history": 0,
            "triage_category": 4
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/cdss/predict",
                json=low_risk_patient,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                predictions = data.get("predictions", {})
                overall_risk = data.get("overall_risk_score", -1)
                
                # For low-risk patient, expect lower overall risk score
                if 0 <= overall_risk <= 1:
                    self.log_test("CDSS Low-Risk Patient Prediction", True, 
                                f"Low-risk patient processed, Overall risk: {overall_risk:.3f}")
                else:
                    self.log_test("CDSS Low-Risk Patient Prediction", False, 
                                f"Invalid overall risk score: {overall_risk}")
            else:
                self.log_test("CDSS Low-Risk Patient Prediction", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("CDSS Low-Risk Patient Prediction", False, f"Request failed: {str(e)}")
    
    def test_cdss_predict_invalid_data(self):
        """Test POST /api/cdss/predict with invalid patient data"""
        invalid_patient = {
            "age": -5,  # Invalid age
            "gender": "Unknown",  # Invalid gender
            "heart_rate": 300,  # Invalid heart rate
            "systolic_bp": 50,  # Invalid BP
            "diastolic_bp": 200,  # Invalid BP
            "respiratory_rate": 0,  # Invalid RR
            "spo2": 150,  # Invalid SpO2
            "temperature": 50,  # Invalid temperature
            "gcs_score": 20,  # Invalid GCS
            # Missing required fields
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/cdss/predict",
                json=invalid_patient,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 422:
                self.log_test("CDSS Invalid Patient Data", True, "Validation error returned as expected")
            else:
                self.log_test("CDSS Invalid Patient Data", False, f"Expected 422, got {response.status_code}")
                
        except Exception as e:
            self.log_test("CDSS Invalid Patient Data", False, f"Request failed: {str(e)}")
    
    def test_cdss_model_performance(self):
        """Test GET /api/cdss/models/performance"""
        try:
            response = requests.get(f"{API_BASE_URL}/cdss/models/performance", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "performance" in data and isinstance(data["performance"], list):
                    performance_data = data["performance"]
                    
                    if len(performance_data) > 0:
                        # Check structure of performance data
                        valid_performance = True
                        expected_metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
                        
                        for model_perf in performance_data:
                            if not all(metric in model_perf for metric in expected_metrics):
                                valid_performance = False
                                break
                            
                            # Check metric values are reasonable (0-1 range)
                            for metric in expected_metrics:
                                value = model_perf.get(metric, -1)
                                if not (0 <= value <= 1):
                                    valid_performance = False
                                    break
                        
                        if valid_performance:
                            self.log_test("CDSS Model Performance", True, 
                                        f"Retrieved performance for {len(performance_data)} models")
                        else:
                            self.log_test("CDSS Model Performance", False, "Invalid performance metrics structure or values")
                    else:
                        self.log_test("CDSS Model Performance", False, "No performance data returned")
                else:
                    self.log_test("CDSS Model Performance", False, f"Invalid response structure. Got: {list(data.keys())}")
            else:
                self.log_test("CDSS Model Performance", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("CDSS Model Performance", False, f"Request failed: {str(e)}")
    
    def test_cdss_statistics(self):
        """Test GET /api/cdss/statistics"""
        try:
            response = requests.get(f"{API_BASE_URL}/cdss/statistics", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["total_predictions", "predictions_last_24h", "high_risk_predictions", "models_active"]
                
                if all(key in data for key in expected_keys):
                    # Check all values are non-negative integers
                    valid_stats = True
                    for key in expected_keys:
                        value = data.get(key, -1)
                        if not isinstance(value, int) or value < 0:
                            valid_stats = False
                            break
                    
                    if valid_stats:
                        self.log_test("CDSS Statistics", True, 
                                    f"Total: {data['total_predictions']}, Last 24h: {data['predictions_last_24h']}, "
                                    f"High-risk: {data['high_risk_predictions']}, Models: {data['models_active']}")
                    else:
                        self.log_test("CDSS Statistics", False, "Invalid statistics values")
                else:
                    self.log_test("CDSS Statistics", False, f"Missing expected keys. Got: {list(data.keys())}")
            else:
                self.log_test("CDSS Statistics", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("CDSS Statistics", False, f"Request failed: {str(e)}")
    
    def verify_cdss_database_storage(self, patient_id):
        """Verify CDSS prediction is stored in MongoDB by checking statistics"""
        if not patient_id:
            self.log_test("CDSS Database Storage Verification", False, "No patient ID to verify")
            return
        
        try:
            # Check if statistics show increased prediction count
            response = requests.get(f"{API_BASE_URL}/cdss/statistics", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_predictions = data.get("total_predictions", 0)
                
                if total_predictions > 0:
                    self.log_test("CDSS Database Storage Verification", True, 
                                f"CDSS predictions stored in database. Total: {total_predictions}")
                else:
                    self.log_test("CDSS Database Storage Verification", False, 
                                "No predictions found in database")
            else:
                self.log_test("CDSS Database Storage Verification", False, 
                            f"Failed to retrieve statistics: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("CDSS Database Storage Verification", False, f"Request failed: {str(e)}")
    
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 60)
        print("STARTING BACKEND API TESTS")
        print("=" * 60)
        
        # Test 1: Health Check
        print("\n1. Testing Health Check Endpoint...")
        self.test_health_check()
        
        # Test 2: Valid Contact Form Submission
        print("\n2. Testing Valid Contact Form Submission...")
        submission_id = self.test_contact_form_valid_submission()
        
        # Test 3: Contact Form Validation
        print("\n3. Testing Contact Form Validation...")
        self.test_contact_form_validation_errors()
        
        # Test 4: Get Contact Submissions
        print("\n4. Testing Get Contact Submissions...")
        self.test_get_contact_submissions()
        
        # Test 5: Get Contact Count
        print("\n5. Testing Get Contact Count...")
        self.test_get_contact_count()
        
        # Test 6: Database Storage Verification
        print("\n6. Testing Database Storage...")
        self.verify_database_storage(submission_id)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        print(f"Success Rate: {(passed_count/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print("\nFAILED TESTS:")
            for test in self.failed_tests:
                print(f"  ❌ {test}")
        
        if self.passed_tests:
            print("\nPASSED TESTS:")
            for test in self.passed_tests:
                print(f"  ✅ {test}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()