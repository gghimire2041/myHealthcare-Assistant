import pytest
import sys
import os

# Add src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_lab_data():
    """Sample lab data for testing"""
    return {
        'glucose': 95.0,
        'total_cholesterol': 180.0,
        'hdl_cholesterol': 45.0,
        'ldl_cholesterol': 100.0,
        'triglycerides': 120.0,
        'hemoglobin': 14.0,
        'wbc': 7.0,
        'platelets': 250.0,
        'creatinine': 1.0
    }

@pytest.fixture
def sample_medical_text():
    """Sample medical document text for testing"""
    return """
    PATIENT: John Doe
    DATE: 2024-12-15
    
    LABORATORY RESULTS:
    Glucose: 95 mg/dL (Normal: 70-99)
    Total Cholesterol: 185 mg/dL
    HDL Cholesterol: 45 mg/dL
    
    MEDICATIONS:
    - Metformin 500mg twice daily
    - Aspirin 81mg daily
    
    RECOMMENDATIONS:
    Continue current medications and follow up in 3 months.
    """

if __name__ == '__main__':
    unittest.main()