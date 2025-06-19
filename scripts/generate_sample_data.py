import json
import os
from datetime import datetime, timedelta
import random

def generate_sample_lab_report():
    """Generate a sample lab report text"""
    return """
COMPREHENSIVE METABOLIC PANEL
Patient: John Doe
Date: 2024-12-15
Provider: Dr. Smith

RESULTS:
Glucose: 95 mg/dL (Normal: 70-99)
Total Cholesterol: 185 mg/dL (Desirable: <200)
HDL Cholesterol: 45 mg/dL (Normal: >40 for males)
LDL Cholesterol: 115 mg/dL (Optimal: <100)
Triglycerides: 140 mg/dL (Normal: <150)
Hemoglobin: 14.2 g/dL (Normal: 13.5-17.5)
White Blood Cells: 6.8 K/μL (Normal: 4.0-11.0)
Platelets: 275 K/μL (Normal: 150-450)
Creatinine: 1.0 mg/dL (Normal: 0.6-1.3)

INTERPRETATION:
- Glucose levels are within normal range
- Cholesterol levels are acceptable but LDL is slightly elevated
- Complete blood count shows normal values
- Kidney function appears normal

RECOMMENDATIONS:
- Continue current diet and exercise routine
- Consider dietary modifications to reduce LDL cholesterol
- Follow-up in 6 months
"""

def generate_sample_prescription():
    """Generate a sample prescription text"""
    return """
PRESCRIPTION
Patient: Jane Smith
Date: 2024-12-10
Provider: Dr. Johnson

Medications Prescribed:
1. Metformin 500mg
   - Take twice daily with meals
   - For diabetes management
   - Quantity: 60 tablets

2. Lisinopril 10mg
   - Take once daily in morning
   - For blood pressure control
   - Quantity: 30 tablets

3. Atorvastatin 40mg
   - Take once daily at bedtime
   - For cholesterol management
   - Quantity: 30 tablets

INSTRUCTIONS:
- Take medications as prescribed
- Monitor blood pressure at home
- Schedule follow-up in 3 months
- Report any unusual side effects

WARNINGS:
- Metformin: May cause stomach upset
- Lisinopril: May cause dry cough
- Atorvastatin: Avoid grapefruit juice
"""

def generate_sample_discharge_summary():
    """Generate a sample discharge summary"""
    return """
DISCHARGE SUMMARY
Patient: Robert Wilson
Admission Date: 2024-12-05
Discharge Date: 2024-12-08
Attending: Dr. Brown

DIAGNOSIS:
Primary: Hypertensive crisis
Secondary: Type 2 diabetes mellitus

HOSPITAL COURSE:
Patient admitted with severely elevated blood pressure (220/120 mmHg).
Responded well to antihypertensive therapy. Blood pressure normalized
to 135/85 mmHg by discharge. Diabetes management optimized.

DISCHARGE MEDICATIONS:
1. Amlodipine 10mg daily
2. Metoprolol 50mg twice daily  
3. Metformin 1000mg twice daily
4. Aspirin 81mg daily

FOLLOW-UP:
- Primary care physician in 1 week
- Cardiology consultation in 2 weeks
- Monitor blood pressure daily at home

DIET:
- Low sodium (2g daily)
- Diabetic diet (carbohydrate controlled)
- Limit alcohol consumption
"""

def create_sample_documents():
    """Create sample documents directory with generated content"""
    
    # Create directories
    os.makedirs("data/sample_documents", exist_ok=True)
    
    # Generate sample documents
    documents = {
        "lab_report_john_doe.txt": generate_sample_lab_report(),
        "prescription_jane_smith.txt": generate_sample_prescription(),
        "discharge_summary_robert_wilson.txt": generate_sample_discharge_summary()
    }
    
    # Write documents to files
    for filename, content in documents.items():
        with open(f"data/sample_documents/{filename}", "w") as f:
            f.write(content)
    
    print(f"Created {len(documents)} sample documents in data/sample_documents/")

def generate_sample_config():
    """Generate sample configuration file"""
    
    config = {
        "app_settings": {
            "app_name": "HealthMind - Privacy-First Healthcare Assistant",
            "version": "1.0.0",
            "debug": False,
            "local_only": True
        },
        "database": {
            "path": "data/health_documents.db",
            "backup_enabled": True,
            "backup_interval_days": 7
        },
        "security": {
            "encryption_enabled": True,
            "password_required": False,
            "session_timeout_minutes": 30
        },
        "features": {
            "ocr_enabled": True,
            "pdf_processing": True,
            "lab_interpretation": True,
            "medication_lookup": True,
            "document_search": True
        },
        "ui": {
            "theme": "default",
            "show_disclaimers": True,
            "enable_export": True
        },
        "health_references": {
            "lab_ranges_source": "built-in",
            "medication_db_source": "built-in",
            "last_updated": "2024-12-01"
        }
    }
    
    os.makedirs("config", exist_ok=True)
    
    with open("config/app_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Created configuration file: config/app_config.json")

def generate_requirements_file():
    """Generate requirements.txt file"""
    
    requirements = [
        "streamlit>=1.28.0",
        "PyPDF2>=3.0.0",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "langchain>=0.0.300",
        "sqlite3",  # Built-in with Python
        "python-multipart>=0.0.6",  # For file uploads
        "watchdog>=3.0.0"  # For file monitoring
    ]
    
    with open("requirements.txt", "w") as f:
        for req in requirements:
            f.write(f"{req}\n")
    
    print("Created requirements.txt file")

def generate_readme():
    """Generate README.md file"""
    
    readme_content = """# HealthMind - Privacy-First Healthcare Assistant

A local, privacy-first AI assistant that helps patients understand lab results, medications, and health documents without sending data to external servers.

## 🔒 Privacy First
- **100% Local Processing**: Your health data never leaves your device
- **No Internet Required**: Works completely offline after installation
- **Encrypted Storage**: All documents stored with AES-256 encryption
- **No Tracking**: No analytics, no data collection, no external requests

## ✨ Features

### 📄 Document Processing
- PDF and image text extraction using OCR
- Support for lab reports, prescriptions, discharge summaries
- Automatic medical entity recognition
- Local vector database for document search

### 🧪 Lab Results Interpretation
- Reference range checking for common lab tests
- Visual charts showing results vs normal ranges
- Explanations of what abnormal values might mean
- Trend tracking over time

### 💊 Medication Information
- Built-in medication database
- Drug interaction warnings
- Side effect information
- Dosage and usage guidelines

### ❓ Health Q&A
- Answer questions about your health documents
- General health information lookup
- Contextual responses based on your data

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR (for image processing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthmind.git
cd healthmind
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

5. Generate sample data:
```bash
python scripts/generate_sample_data.py
```

6. Run the application:
```bash
streamlit run main.py
```

## 📁 Project Structure

```
healthmind/
├── main.py                 # Main Streamlit application
├── src/
│   ├── document_processor.py  # PDF/OCR processing
│   ├── health_interpreter.py  # Medical interpretation
│   ├── vector_store.py        # Local document storage
│   └── ui_components.py       # UI components
├── data/
│   ├── health_documents.db    # SQLite database
│   └── sample_documents/      # Sample health documents
├── config/
│   └── app_config.json        # Application configuration
├── scripts/
│   └── generate_sample_data.py # Sample data generator
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🏥 Medical Disclaimer

**⚠️ IMPORTANT**: This application is for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 🔧 Configuration

The application can be configured via `config/app_config.json`:

```json
{
  "app_settings": {
    "app_name": "HealthMind - Privacy-First Healthcare Assistant",
    "local_only": true
  },
  "security": {
    "encryption_enabled": true,
    "password_required": false
  },
  "features": {
    "ocr_enabled": true,
    "pdf_processing": true,
    "lab_interpretation": true
  }
}
```

## 📊 Supported Lab Tests

The application provides reference ranges and interpretations for:

- **Blood Chemistry**: Glucose, Cholesterol (Total, HDL, LDL), Triglycerides
- **Complete Blood Count**: Hemoglobin, White Blood Cells, Platelets
- **Kidney Function**: Creatinine, BUN
- **Liver Function**: ALT, AST, Bilirubin
- **Thyroid Function**: TSH, T3, T4

## 💊 Medication Database

Built-in information for common medications including:
- Generic and brand names
- Drug classes and uses
- Common side effects
- Warnings and precautions
- Drug interactions

## 🛠️ Development

### Adding New Features

1. **New Lab Tests**: Add reference ranges to `health_interpreter.py`
2. **New Medications**: Extend the medication database
3. **Document Types**: Add new parsers to `document_processor.py`
4. **UI Components**: Create reusable components in `ui_components.py`

### Running Tests

```bash
python -m pytest tests/
```

### Building for Distribution

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 🔒 Security Features

- **Local Storage**: All data stored in encrypted SQLite database
- **No Network Access**: Application works completely offline
- **Data Encryption**: AES-256 encryption for sensitive documents
- **Secure Deletion**: Overwrite data when deleted
- **Access Controls**: Optional password protection

## 📈 Roadmap

- [ ] Advanced OCR with medical form recognition
- [ ] Integration with wearable device data
- [ ] Appointment and medication reminders
- [ ] Family health tracking
- [ ] Export to standard health data formats (FHIR)
- [ ] Voice interface for accessibility
- [ ] Mobile app version

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation wiki
- Join our community discussions

## 🙏 Acknowledgments

- Built with Streamlit for the web interface
- Uses scikit-learn for document similarity
- Tesseract OCR for image text extraction
- Medical reference data from public health sources

---

**Remember**: Your health data stays on your device. Always consult healthcare professionals for medical decisions."""

if __name__ == "__main__":
    print("Generating sample data and configuration files...")
    
    create_sample_documents()
    generate_sample_config()
    generate_requirements_file()
    generate_readme()
    
    print("\n✅ Sample data generation complete!")
    print("\nNext steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Install Tesseract OCR for your system")
    print("3. Run the app: streamlit run main.py")
    print("4. Upload the sample documents from data/sample_documents/")
    print("\n🔒 Remember: All processing happens locally on your device!")