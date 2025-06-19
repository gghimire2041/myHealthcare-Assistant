import json
import os
from typing import List, Dict, Any
import sqlite3
from datetime import datetime
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorStore:
    """Local vector storage for medical documents using SQLite and TF-IDF"""
    
    def __init__(self, db_path: str = "data/health_documents.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Load existing documents for vectorization
        self._update_vectorizer()
    
    def _init_database(self):
        """Initialize SQLite database for document storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    content TEXT NOT NULL,
                    document_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS document_vectors (
                    document_id INTEGER,
                    vector_data TEXT,
                    FOREIGN KEY (document_id) REFERENCES documents (id)
                )
            ''')
            
            conn.commit()
    
    def add_document(self, filename: str, content: str, document_type: str = None, metadata: Dict = None) -> int:
        """Add a document to the vector store"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert document
                cursor.execute('''
                    INSERT INTO documents (filename, content, document_type, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (filename, content, document_type, json.dumps(metadata or {})))
                
                document_id = cursor.lastrowid
                conn.commit()
                
                # Update vectorizer with new document
                self._update_vectorizer()
                
                self.logger.info(f"Document '{filename}' added with ID {document_id}")
                return document_id
                
        except Exception as e:
            self.logger.error(f"Error adding document: {str(e)}")
            return -1
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents using TF-IDF similarity"""
        try:
            # Get all documents
            documents = self.list_documents()
            
            if not documents:
                return []
            
            # Prepare document texts
            doc_texts = [doc['content'] for doc in documents]
            
            # Add query to the corpus and vectorize
            all_texts = doc_texts + [query]
            
            # Fit and transform the texts
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Calculate similarity between query and documents
            query_vector = tfidf_matrix[-1]  # Last vector is the query
            doc_vectors = tfidf_matrix[:-1]  # All others are documents
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # Get top-k most similar documents
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    doc = documents[idx].copy()
                    doc['similarity'] = float(similarities[idx])
                    results.append(doc)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def list_documents(self) -> List[Dict]:
        """List all documents in the store"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, filename, content, document_type, timestamp, metadata
                    FROM documents
                    ORDER BY timestamp DESC
                ''')
                
                documents = []
                for row in cursor.fetchall():
                    doc = {
                        'id': row[0],
                        'filename': row[1],
                        'content': row[2],
                        'document_type': row[3],
                        'timestamp': row[4],
                        'metadata': json.loads(row[5]) if row[5] else {}
                    }
                    documents.append(doc)
                
                return documents
                
        except Exception as e:
            self.logger.error(f"Error listing documents: {str(e)}")
            return []
    
    def get_document(self, document_id: int) -> Dict:
        """Get a specific document by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, filename, content, document_type, timestamp, metadata
                    FROM documents
                    WHERE id = ?
                ''', (document_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'filename': row[1],
                        'content': row[2],
                        'document_type': row[3],
                        'timestamp': row[4],
                        'metadata': json.loads(row[5]) if row[5] else {}
                    }
                
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting document {document_id}: {str(e)}")
            return {}
    
    def delete_document(self, document_id: int) -> bool:
        """Delete a document from the store"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete from both tables
                cursor.execute('DELETE FROM document_vectors WHERE document_id = ?', (document_id,))
                cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
                
                conn.commit()
                
                # Update vectorizer
                self._update_vectorizer()
                
                self.logger.info(f"Document {document_id} deleted")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False
    
    def _update_vectorizer(self):
        """Update the TF-IDF vectorizer with current documents"""
        try:
            documents = self.list_documents()
            
            if documents:
                texts = [doc['content'] for doc in documents]
                self.vectorizer.fit(texts)
                
        except Exception as e:
            self.logger.error(f"Error updating vectorizer: {str(e)}")
    
    def get_document_stats(self) -> Dict:
        """Get statistics about the document store"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total documents
                cursor.execute('SELECT COUNT(*) FROM documents')
                total_docs = cursor.fetchone()[0]
                
                # Documents by type
                cursor.execute('''
                    SELECT document_type, COUNT(*) 
                    FROM documents 
                    GROUP BY document_type
                ''')
                by_type = dict(cursor.fetchall())
                
                # Recent documents (last 7 days)
                cursor.execute('''
                    SELECT COUNT(*) FROM documents 
                    WHERE timestamp > datetime('now', '-7 days')
                ''')
                recent_docs = cursor.fetchone()[0]
                
                return {
                    'total_documents': total_docs,
                    'documents_by_type': by_type,
                    'recent_documents': recent_docs
                }
                
        except Exception as e:
            self.logger.error(f"Error getting document stats: {str(e)}")
            return {}