import streamlit as st
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from document_processor import DocumentProcessor
from health_interpreter import HealthInterpreter
from vector_store import VectorStore
from ui_components import UIComponents

class HealthcareAssistant:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.health_interpreter = HealthInterpreter()
        self.vector_store = VectorStore()
        self.ui = UIComponents()
        
    def run(self):
        st.set_page_config(
            page_title="HealthMind - Privacy-First Health Assistant",
            page_icon="🏥",
            layout="wide"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #2E86AB;
            text-align: center;
            margin-bottom: 2rem;
        }
        .privacy-badge {
            background: linear-gradient(90deg, #28a745, #20c997);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown('<h1 class="main-header">🏥 HealthMind</h1>', unsafe_allow_html=True)
        st.markdown('<div class="privacy-badge">🔒 100% Local Processing - Your Data Never Leaves Your Device</div>', 
                   unsafe_allow_html=True)
        
        # Medical disclaimer
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ Medical Disclaimer:</strong> This tool is for educational purposes only. 
        Always consult with healthcare professionals for medical advice, diagnosis, or treatment decisions.
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.header("📋 Features")
            feature = st.selectbox("Choose a feature:", [
                "📄 Upload & Analyze Documents",
                "🧪 Lab Results Interpreter",
                "💊 Medication Information",
                "❓ Health Q&A",
                "📊 Document Library"
            ])
        
        # Main content area
        if feature == "📄 Upload & Analyze Documents":
            self.document_upload_page()
        elif feature == "🧪 Lab Results Interpreter":
            self.lab_results_page()
        elif feature == "💊 Medication Information":
            self.medication_page()
        elif feature == "❓ Health Q&A":
            self.qa_page()
        elif feature == "📊 Document Library":
            self.document_library_page()
    
    def document_upload_page(self):
        st.header("📄 Document Upload & Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload your medical document",
                type=['pdf', 'png', 'jpg', 'jpeg'],
                help="Supported formats: PDF, PNG, JPG, JPEG"
            )
            
            if uploaded_file:
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process document
                with st.spinner("Processing document..."):
                    extracted_text = self.doc_processor.extract_text(temp_path)
                    
                    if extracted_text:
                        # Store in vector database
                        self.vector_store.add_document(uploaded_file.name, extracted_text)
                        
                        # Analyze content
                        analysis = self.health_interpreter.analyze_document(extracted_text)
                        
                        st.success("Document processed successfully!")
                        
                        with col2:
                            st.subheader("📋 Analysis Results")
                            
                            if analysis.get('document_type'):
                                st.info(f"**Document Type:** {analysis['document_type']}")
                            
                            if analysis.get('key_findings'):
                                st.subheader("🔍 Key Findings")
                                for finding in analysis['key_findings']:
                                    st.write(f"• {finding}")
                            
                            if analysis.get('medications'):
                                st.subheader("💊 Medications Mentioned")
                                for med in analysis['medications']:
                                    st.write(f"• {med}")
                            
                            if analysis.get('lab_values'):
                                st.subheader("🧪 Lab Values")
                                for value in analysis['lab_values']:
                                    st.write(f"• {value}")
                
                # Cleanup
                os.remove(temp_path)
    
    def lab_results_page(self):
        st.header("🧪 Lab Results Interpreter")
        
        # Sample lab values form
        st.subheader("Enter your lab values:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=500.0, value=95.0)
            cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=0.0, max_value=400.0, value=180.0)
            hdl = st.number_input("HDL Cholesterol (mg/dL)", min_value=0.0, max_value=150.0, value=45.0)
        
        with col2:
            ldl = st.number_input("LDL Cholesterol (mg/dL)", min_value=0.0, max_value=300.0, value=100.0)
            triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=0.0, max_value=800.0, value=120.0)
            hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=20.0, value=14.0)
        
        with col3:
            wbc = st.number_input("White Blood Cells (K/μL)", min_value=0.0, max_value=50.0, value=7.0)
            platelets = st.number_input("Platelets (K/μL)", min_value=0.0, max_value=1000.0, value=250.0)
            creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, max_value=10.0, value=1.0)
        
        if st.button("🔍 Analyze Lab Results"):
            lab_data = {
                'glucose': glucose,
                'total_cholesterol': cholesterol,
                'hdl_cholesterol': hdl,
                'ldl_cholesterol': ldl,
                'triglycerides': triglycerides,
                'hemoglobin': hemoglobin,
                'wbc': wbc,
                'platelets': platelets,
                'creatinine': creatinine
            }
            
            interpretation = self.health_interpreter.interpret_lab_results(lab_data)
            
            st.subheader("📊 Results Interpretation")
            
            # Display results in colored boxes
            for test, result in interpretation.items():
                if result['status'] == 'normal':
                    st.success(f"**{test.replace('_', ' ').title()}**: {result['value']} - {result['interpretation']}")
                elif result['status'] == 'borderline':
                    st.warning(f"**{test.replace('_', ' ').title()}**: {result['value']} - {result['interpretation']}")
                else:
                    st.error(f"**{test.replace('_', ' ').title()}**: {result['value']} - {result['interpretation']}")
    
    def medication_page(self):
        st.header("💊 Medication Information")
        
        medication = st.text_input("Enter medication name:")
        
        if medication:
            med_info = self.health_interpreter.get_medication_info(medication)
            
            if med_info:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("ℹ️ General Information")
                    st.write(f"**Generic Name:** {med_info.get('generic_name', 'N/A')}")
                    st.write(f"**Drug Class:** {med_info.get('drug_class', 'N/A')}")
                    st.write(f"**Primary Use:** {med_info.get('primary_use', 'N/A')}")
                
                with col2:
                    st.subheader("⚠️ Important Notes")
                    
                    if med_info.get('common_side_effects'):
                        st.write("**Common Side Effects:**")
                        for effect in med_info['common_side_effects']:
                            st.write(f"• {effect}")
                    
                    if med_info.get('warnings'):
                        st.write("**Warnings:**")
                        for warning in med_info['warnings']:
                            st.write(f"⚠️ {warning}")
            else:
                st.warning("Medication information not found. Please consult your healthcare provider.")
    
    def qa_page(self):
        st.header("❓ Health Q&A")
        
        question = st.text_input("Ask a health-related question:")
        
        if question:
            # Search relevant documents first
            relevant_docs = self.vector_store.search_documents(question)
            
            # Generate answer
            answer = self.health_interpreter.answer_question(question, relevant_docs)
            
            st.subheader("💡 Answer")
            st.write(answer)
            
            if relevant_docs:
                st.subheader("📚 Related Documents")
                for doc in relevant_docs[:3]:
                    st.write(f"• {doc['filename']}")
    
    def document_library_page(self):
        st.header("📊 Document Library")
        
        documents = self.vector_store.list_documents()
        
        if documents:
            st.write(f"**Total Documents:** {len(documents)}")
            
            for doc in documents:
                with st.expander(f"📄 {doc['filename']}"):
                    st.write(f"**Added:** {doc.get('timestamp', 'Unknown')}")
                    st.write(f"**Preview:** {doc.get('content', '')[:200]}...")
        else:
            st.info("No documents uploaded yet. Use the 'Upload & Analyze Documents' feature to get started.")

if __name__ == "__main__":
    app = HealthcareAssistant()
    app.run()