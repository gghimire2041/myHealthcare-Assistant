import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

@dataclass
class LabReference:
    """Reference ranges for lab values"""
    name: str
    normal_range: tuple
    unit: str
    description: str

class HealthInterpreter:
    """Interprets health documents and provides medical information"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.lab_references = self._load_lab_references()
        self.medication_db = self._load_medication_database()
        
    def _load_lab_references(self) -> Dict[str, LabReference]:
        """Load reference ranges for common lab tests"""
        return {
            'glucose': LabReference('Glucose', (70, 99), 'mg/dL', 'Fasting blood sugar'),
            'total_cholesterol': LabReference('Total Cholesterol', (0, 199), 'mg/dL', 'Total cholesterol'),
            'hdl_cholesterol': LabReference('HDL Cholesterol', (40, 200), 'mg/dL', 'Good cholesterol'),
            'ldl_cholesterol': LabReference('LDL Cholesterol', (0, 99), 'mg/dL', 'Bad cholesterol'),
            'triglycerides': LabReference('Triglycerides', (0, 149), 'mg/dL', 'Blood fats'),
            'hemoglobin': LabReference('Hemoglobin', (12.0, 17.5), 'g/dL', 'Oxygen-carrying protein'),
            'wbc': LabReference('White Blood Cells', (4.0, 11.0), 'K/μL', 'Infection-fighting cells'),
            'platelets': LabReference('Platelets', (150, 450), 'K/μL', 'Blood clotting cells'),
            'creatinine': LabReference('Creatinine', (0.6, 1.3), 'mg/dL', 'Kidney function marker'),
        }
    
    def _load_medication_database(self) -> Dict[str, Dict]:
        """Load medication information database"""
        return {
            'aspirin': {
                'generic_name': 'Acetylsalicylic acid',
                'drug_class': 'NSAID / Antiplatelet',
                'primary_use': 'Pain relief, anti-inflammatory, heart attack prevention',
                'common_side_effects': ['Stomach upset', 'Heartburn', 'Nausea'],
                'warnings': ['May increase bleeding risk', 'Avoid with stomach ulcers']
            },
            'metformin': {
                'generic_name': 'Metformin hydrochloride',
                'drug_class': 'Biguanide antidiabetic',
                'primary_use': 'Type 2 diabetes management',
                'common_side_effects': ['Diarrhea', 'Nausea', 'Stomach upset'],
                'warnings': ['Monitor kidney function', 'Risk of lactic acidosis']
            },
            'lisinopril': {
                'generic_name': 'Lisinopril',
                'drug_class': 'ACE inhibitor',
                'primary_use': 'High blood pressure, heart failure',
                'common_side_effects': ['Dry cough', 'Dizziness', 'Fatigue'],
                'warnings': ['Monitor kidney function', 'May cause hyperkalemia']
            },
            'atorvastatin': {
                'generic_name': 'Atorvastatin calcium',
                'drug_class': 'Statin',
                'primary_use': 'High cholesterol management',
                'common_side_effects': ['Muscle pain', 'Headache', 'Nausea'],
                'warnings': ['Monitor liver function', 'Risk of muscle problems']
            },
            'ibuprofen': {
                'generic_name': 'Ibuprofen',
                'drug_class': 'NSAID',
                'primary_use': 'Pain relief, anti-inflammatory, fever reduction',
                'common_side_effects': ['Stomach upset', 'Dizziness', 'Heartburn'],
                'warnings': ['May increase cardiovascular risk', 'Avoid with kidney problems']
            }
        }
    
    def analyze_document(self, text: str) -> Dict[str, Any]:
        """Analyze medical document and extract key information"""
        analysis = {
            'document_type': self._identify_document_type(text),
            'key_findings': [],
            'medications': [],
            'lab_values': [],
            'recommendations': []
        }
        
        # Extract medications
        medications = self._extract_medications(text)
        analysis['medications'] = medications
        
        # Extract lab values
        lab_values = self._extract_lab_values(text)
        analysis['lab_values'] = lab_values
        
        # Generate key findings
        analysis['key_findings'] = self._generate_key_findings(text, medications, lab_values)
        
        return analysis
    
    def _identify_document_type(self, text: str) -> str:
        """Identify the type of medical document"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['lab', 'laboratory', 'blood test', 'urinalysis']):
            return 'Laboratory Results'
        elif any(term in text_lower for term in ['prescription', 'medication', 'pharmacy']):
            return 'Prescription'
        elif any(term in text_lower for term in ['discharge', 'summary', 'hospital']):
            return 'Discharge Summary'
        elif any(term in text_lower for term in ['radiology', 'x-ray', 'ct scan', 'mri']):
            return 'Imaging Report'
        else:
            return 'Medical Document'
    
    def _extract_medications(self, text: str) -> List[str]:
        """Extract medication names from text"""
        medications = []
        
        # Common medication patterns
        patterns = [
            r'\b(aspirin|ibuprofen|acetaminophen|metformin|lisinopril|atorvastatin|amlodipine|metoprolol|omeprazole|losartan)\b',
            r'\b\w+\s+\d+\s*mg\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            medications.extend(matches)
        
        return list(set(medications))
    
    def _extract_lab_values(self, text: str) -> List[str]:
        """Extract lab values from text"""
        lab_values = []
        
        patterns = [
            r'glucose\s*:?\s*(\d+\.?\d*)\s*mg/dl',
            r'cholesterol\s*:?\s*(\d+\.?\d*)\s*mg/dl',
            r'hemoglobin\s*:?\s*(\d+\.?\d*)\s*g/dl',
            r'(\w+)\s*:?\s*(\d+\.?\d*)\s*(mg/dl|g/dl|mmol/l)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    lab_values.append(f"{match[0]}: {match[1]} {match[2] if len(match) > 2 else ''}")
                else:
                    lab_values.append(match)
        
        return lab_values
    
    def _generate_key_findings(self, text: str, medications: List[str], lab_values: List[str]) -> List[str]:
        """Generate key findings based on document content"""
        findings = []
        
        if medications:
            findings.append(f"Document mentions {len(medications)} medications")
        
        if lab_values:
            findings.append(f"Contains {len(lab_values)} laboratory values")
        
        # Look for concerning terms
        concerning_terms = ['abnormal', 'elevated', 'low', 'high', 'critical']
        for term in concerning_terms:
            if term in text.lower():
                findings.append(f"Document contains '{term}' - review recommended")
                break
        
        return findings
    
    def interpret_lab_results(self, lab_data: Dict[str, float]) -> Dict[str, Dict]:
        """Interpret lab results against reference ranges"""
        interpretations = {}
        
        for test_name, value in lab_data.items():
            if test_name in self.lab_references:
                ref = self.lab_references[test_name]
                
                if ref.normal_range[0] <= value <= ref.normal_range[1]:
                    status = 'normal'
                    interpretation = f"Within normal range ({ref.normal_range[0]}-{ref.normal_range[1]} {ref.unit})"
                elif value < ref.normal_range[0]:
                    status = 'low'
                    interpretation = f"Below normal range (Normal: {ref.normal_range[0]}-{ref.normal_range[1]} {ref.unit})"
                else:
                    status = 'high'
                    interpretation = f"Above normal range (Normal: {ref.normal_range[0]}-{ref.normal_range[1]} {ref.unit})"
                
                # Special cases
                if test_name == 'glucose' and value > 125:
                    status = 'high'
                    interpretation += " - Consult healthcare provider about diabetes risk"
                elif test_name == 'total_cholesterol' and 200 <= value <= 239:
                    status = 'borderline'
                    interpretation = f"Borderline high (200-239 {ref.unit}) - lifestyle changes recommended"
                
                interpretations[test_name] = {
                    'value': f"{value} {ref.unit}",
                    'status': status,
                    'interpretation': interpretation,
                    'description': ref.description
                }
        
        return interpretations
    
    def get_medication_info(self, medication_name: str) -> Optional[Dict]:
        """Get information about a medication"""
        med_name = medication_name.lower().strip()
        
        # Direct lookup
        if med_name in self.medication_db:
            return self.medication_db[med_name]
        
        # Partial matching
        for drug_name, info in self.medication_db.items():
            if med_name in drug_name or drug_name in med_name:
                return info
        
        return None
    
    def answer_question(self, question: str, relevant_docs: List[Dict] = None) -> str:
        """Answer health-related questions"""
        question_lower = question.lower()
        
        # Simple keyword-based responses
        if any(word in question_lower for word in ['cholesterol', 'ldl', 'hdl']):
            return """Cholesterol is a waxy substance found in your blood. Your body needs cholesterol to build healthy cells, but high levels can increase your risk of heart disease. 
            
LDL (low-density lipoprotein) is often called "bad" cholesterol because it can build up in artery walls. HDL (high-density lipoprotein) is "good" cholesterol because it helps transport cholesterol to your liver for disposal.

Normal ranges:
- Total cholesterol: Less than 200 mg/dL
- LDL: Less than 100 mg/dL  
- HDL: 40 mg/dL or higher for men, 50 mg/dL or higher for women"""
        
        elif any(word in question_lower for word in ['glucose', 'blood sugar', 'diabetes']):
            return """Blood glucose (blood sugar) is the amount of sugar in your blood. Your body uses glucose for energy, and it comes from the food you eat.

Normal fasting blood glucose levels are between 70-99 mg/dL. Levels of 100-125 mg/dL may indicate prediabetes, while levels of 126 mg/dL or higher on two separate occasions indicate diabetes.

Factors that can affect blood glucose include:
- Food intake
- Physical activity  
- Medications
- Stress
- Illness

Regular monitoring is important for people with diabetes or prediabetes."""
        
        elif any(word in question_lower for word in ['blood pressure', 'hypertension']):
            return """Blood pressure measures the force of blood against your artery walls. It's recorded as two numbers:
- Systolic (top number): pressure when your heart beats
- Diastolic (bottom number): pressure when your heart rests between beats

Blood pressure categories:
- Normal: Less than 120/80 mmHg
- Elevated: 120"""