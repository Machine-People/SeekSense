# vector_store.py
from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema, utility
import numpy as np
from typing import List, Dict, Optional, Union
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class MilvusVectorStore:
    def __init__(self, host: str = "milvus", port: str = "19530", collection_name: str = "bengali_products"):
        """Initialize connection to Milvus."""
        self.host = host
        self.port = port
        self.collection_name = collection_name
        connections.connect(host=self.host, port=self.port)
        self._ensure_collection()
        
    def _ensure_collection(self, dim: int = 768):
        """Create collection if it doesn't exist."""
        if utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name)
        else:
            # Define fields for the collection
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
                FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="chunk_index", dtype=DataType.INT64),
                FieldSchema(name="total_chunks", dtype=DataType.INT64),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
            ]
            
            schema = CollectionSchema(fields=fields, description="Bengali product descriptions")
            self.collection = Collection(self.collection_name, schema=schema)
            
            # Create index for vector field
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            self.collection.create_index(field_name="embedding", index_params=index_params)
        
        # Load collection into memory for search
        self.collection.load()
    
    def insert_documents(self, documents: List[Dict], embeddings: Dict[str, np.ndarray]):
        """Insert documents with embeddings into Milvus."""
        entities = []
        
        # Prepare data for insertion
        ids = []
        titles = []
        contents = []
        chunk_indices = []
        total_chunks_list = []
        embedding_vectors = []
        
        MAX_TITLE_LENGTH = 1000
        MAX_CONTENT_LENGTH = 10000

        for doc in documents:
            doc_id = doc["id"]
            if doc_id in embeddings:
                ids.append(doc_id)
                # Truncate title and content to allowed lengths
                titles.append(doc["title"][:MAX_TITLE_LENGTH])
                contents.append(doc["content"][:MAX_CONTENT_LENGTH])
                chunk_indices.append(doc["chunk_index"])
                total_chunks_list.append(doc["total_chunks"])
                embedding_vectors.append(embeddings[doc_id].tolist())
        
        # Insert data
        entities = [
            ids, 
            titles, 
            contents, 
            chunk_indices, 
            total_chunks_list, 
            embedding_vectors
        ]
        
        self.collection.insert(entities)
        self.collection.flush()
    
    def similarity_search(self, query_embedding: np.ndarray, limit: int = 3) -> List[Dict]:
        """Search for similar documents using vector similarity."""
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        
        results = self.collection.search(
            data=[query_embedding.tolist()],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            output_fields=["id", "title", "content", "chunk_index", "total_chunks"]
        )
        
        hits = []
        for hit in results[0]:
            hits.append({
                "id": hit.id,
                "title": hit.entity.get("title"),
                "content": hit.entity.get("content"),
                "chunk_index": hit.entity.get("chunk_index"),
                "total_chunks": hit.entity.get("total_chunks"),
                "score": hit.score
            })
            
        return hits
