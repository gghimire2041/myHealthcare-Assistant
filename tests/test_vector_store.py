import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vector_store import VectorStore

class TestVectorStore(unittest.TestCase):
    
    def setUp(self):
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.store = VectorStore(db_path=self.temp_db.name)
    
    def tearDown(self):
        # Cleanup temporary database
        os.unlink(self.temp_db.name)
    
    def test_add_and_retrieve_document(self):
        """Test adding and retrieving documents"""
        filename = "test_document.txt"
        content = "This is a test medical document about diabetes and glucose levels."
        
        # Add document
        doc_id = self.store.add_document(filename, content, "Test Document")
        
        self.assertGreater(doc_id, 0)
        
        # Retrieve document
        retrieved_doc = self.store.get_document(doc_id)
        
        self.assertEqual(retrieved_doc['filename'], filename)
        self.assertEqual(retrieved_doc['content'], content)
        self.assertEqual(retrieved_doc['document_type'], "Test Document")
    
    def test_search_documents(self):
        """Test document search functionality"""
        # Add test documents
        self.store.add_document("doc1.txt", "This document discusses diabetes and blood sugar management.", "Medical")
        self.store.add_document("doc2.txt", "Information about cholesterol and heart health.", "Medical")
        self.store.add_document("doc3.txt", "Prescription for blood pressure medication.", "Prescription")
        
        # Search for diabetes-related content
        results = self.store.search_documents("diabetes blood sugar")
        
        self.assertGreater(len(results), 0)
        self.assertIn("diabetes", results[0]['content'].lower())
    
    def test_document_stats(self):
        """Test document statistics"""
        # Add test documents
        self.store.add_document("doc1.txt", "Content 1", "Type A")
        self.store.add_document("doc2.txt", "Content 2", "Type B")
        self.store.add_document("doc3.txt", "Content 3", "Type A")
        
        stats = self.store.get_document_stats()
        
        self.assertEqual(stats['total_documents'], 3)
        self.assertEqual(stats['documents_by_type']['Type A'], 2)
        self.assertEqual(stats['documents_by_type']['Type B'], 1)