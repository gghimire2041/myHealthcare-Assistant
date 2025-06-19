import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from health_interpreter import HealthInterpreter

class TestHealthInterpreter(unittest.TestCase):
    
    def setUp(self):
        self.interpreter = HealthInterpreter()
    
    def test_lab_result_interpretation_normal(self):
        """Test interpretation of normal lab values"""
        lab_data = {
            'glucose': 85.0,
            'total_cholesterol': 180.0,
            'hdl_cholesterol': 50.0
        }
        
        results = self.interpreter.interpret_lab_results(lab_data)
        
        self.assertEqual(results['glucose']['status'], 'normal')
        self.assertEqual(results['total_cholesterol']['status'], 'normal')
        self.assertEqual(results['hdl_cholesterol']['status'], 'normal')
    
    def test_lab_result_interpretation_high(self):
        """Test interpretation of high lab values"""
        lab_data = {
            'glucose': 130.0,
            'total_cholesterol': 250.0
        }
        
        results = self.interpreter.interpret_lab_results(lab_data)
        
        self.assertEqual(results['glucose']['status'], 'high')
        self.assertEqual(results['total_cholesterol']['status'], 'high')
    
    def test_medication_lookup(self):
        """Test medication information lookup"""
        med_info = self.interpreter.get_medication_info('aspirin')
        
        self.assertIsNotNone(med_info)
        self.assertEqual(med_info['generic_name'], 'Acetylsalicylic acid')
        self.assertEqual(med_info['drug_class'], 'NSAID / Antiplatelet')
    
    def test_medication_lookup_not_found(self):
        """Test medication lookup for unknown medication"""
        med_info = self.interpreter.get_medication_info('unknown_medication')
        
        self.assertIsNone(med_info)
    
    def test_document_type_identification(self):
        """Test document type identification"""
        lab_text = "LABORATORY RESULTS: Glucose: 95 mg/dL"
        prescription_text = "PRESCRIPTION: Metformin 500mg twice daily"
        
        lab_analysis = self.interpreter.analyze_document(lab_text)
        prescription_analysis = self.interpreter.analyze_document(prescription_text)
        
        self.assertEqual(lab_analysis['document_type'], 'Laboratory Results')
        self.assertEqual(prescription_analysis['document_type'], 'Prescription')