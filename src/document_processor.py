import PyPDF2
import pytesseract
from PIL import Image
import io
import os
import logging
from typing import Optional

class DocumentProcessor:
    """Handles document text extraction from PDFs and images"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Configure Tesseract path if needed (Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from PDF or image file"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                return self._extract_from_image(file_path)
            else:
                self.logger.error(f"Unsupported file type: {file_extension}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return None
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            # If PDF text extraction yields little content, try OCR
            if len(text.strip()) < 100:
                self.logger.info("PDF text extraction yielded minimal content, attempting OCR...")
                return self._ocr_pdf(pdf_path)
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Error reading PDF: {str(e)}")
            # Fallback to OCR
            return self._ocr_pdf(pdf_path)
    
    def _extract_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            
            # Preprocess image for better OCR results
            image = self._preprocess_image(image)
            
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Error performing OCR on image: {str(e)}")
            return ""
    
    def _ocr_pdf(self, pdf_path: str) -> str:
        """Perform OCR on PDF pages"""
        try:
            # Convert PDF pages to images and OCR them
            # This is a simplified version - in production, you'd use pdf2image
            return "OCR functionality for PDF requires pdf2image library"
        except Exception as e:
            self.logger.error(f"Error performing OCR on PDF: {str(e)}")
            return ""
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # You can add more preprocessing here:
            # - Noise reduction
            # - Contrast enhancement
            # - Binarization
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            return image
    
    def extract_medical_entities(self, text: str) -> dict:
        """Extract medical entities from text using simple pattern matching"""
        import re
        
        entities = {
            'medications': [],
            'lab_values': [],
            'dates': [],
            'measurements': []
        }
        
        # Common medication patterns
        med_patterns = [
            r'\b(aspirin|ibuprofen|acetaminophen|metformin|lisinopril|atorvastatin|amlodipine|metoprolol|omeprazole|losartan)\b',
            r'\b\w+\s+\d+\s*mg\b',  # Drug with dosage
        ]
        
        for pattern in med_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['medications'].extend(matches)
        
        # Lab value patterns
        lab_patterns = [
            r'glucose\s*:?\s*(\d+\.?\d*)\s*mg/dl',
            r'cholesterol\s*:?\s*(\d+\.?\d*)\s*mg/dl',
            r'hemoglobin\s*:?\s*(\d+\.?\d*)\s*g/dl',
            r'(\w+)\s*:?\s*(\d+\.?\d*)\s*(mg/dl|g/dl|mmol/l)',
        ]
        
        for pattern in lab_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['lab_values'].extend(matches)
        
        # Date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{2,4}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['dates'].extend(matches)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities