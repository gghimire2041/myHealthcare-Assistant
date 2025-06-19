import unittest
import tempfile
import os
from PIL import Image
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = DocumentProcessor()
    
    def test_extract_medical_entities(self):
        """Test extraction of medical entities from text"""
        text = """
        Patient is taking aspirin 81mg daily and metformin 500mg twice daily.
        Lab results show glucose: 95 mg/dl and cholesterol: 180 mg/dl.
        Appointment scheduled for 12/15/2024.
        """
        
        entities = self.processor.extract_medical_entities(text)
        
        self.assertIn('aspirin', [med.lower() for med in entities['medications']])
        self.assertTrue(len(entities['lab_values']) > 0)
        self.assertTrue(len(entities['dates']) > 0)
    
    def test_image_preprocessing(self):
        """Test image preprocessing for OCR"""
        # Create a simple test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Create a simple white image with black text
            img = Image.new('RGB', (200, 100), color='white')
            img.save(tmp_file.name)
            
            # Test preprocessing
            processed_img = self.processor._preprocess_image(img)
            
            # Should convert to grayscale
            self.assertEqual(processed_img.mode, 'L')
            
        # Cleanup
        os.unlink(tmp_file.name)