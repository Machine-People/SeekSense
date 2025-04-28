# embedding.py
import json
import requests
import numpy as np
import os
from typing import List, Dict, Optional
from tqdm import tqdm

class JinaAIEmbeddingModel:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "jina-embeddings-v3"):
        """
        Initialize Jina AI API client for multilingual embeddings.
        
        Args:
            api_key: Jina AI API key. If None, uses JINA_API_KEY environment variable.
            model_name: The model to use for embeddings. Default is jina-embeddings-v3.
        """
        # self.api_key = api_key or os.environ.get("JINA_API_KEY")
        self.api_key = "jina_5ce13dfc61794c60a38dbdc68b05f3c9Hh_1aVZrLFZm9yQUCBUUjCzol5_F"
        if not self.api_key:
            raise ValueError("API key required. Provide directly or set JINA_API_KEY environment variable.")
        
        self.model_name = model_name
        self.api_url = 'https://api.jina.ai/v1/embeddings'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def encode(self, texts: List[str], batch_size: int = 16, show_progress: bool = False) -> np.ndarray:
        """
        Generate embeddings for a list of Bengali texts using Jina AI API.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call
            show_progress: Whether to show a progress bar
            
        Returns:
            numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        all_embeddings = []
        
        # Process in batches with optional progress bar
        # TODO add overlap
        batches = range(0, len(texts), batch_size)
        if show_progress:
            batches = tqdm(batches, desc="Generating embeddings")
            
        for i in batches:
            batch = texts[i:i+batch_size]
            
            # Prepare the input data
            data = {
                "model": self.model_name,
                "input": [{"text": text} for text in batch]
            }
            
            try:
                # Make the API request
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    data=json.dumps(data),
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract embeddings from response
                batch_embeddings = [item["embedding"] for item in result["data"]]
                all_embeddings.extend(batch_embeddings)
                
            except requests.exceptions.RequestException as e:
                raise Exception(f"API request failed: {str(e)}")
            except (KeyError, IndexError, ValueError) as e:
                raise Exception(f"Failed to parse API response: {str(e)}")
        
        if not all_embeddings:
            raise Exception("No embeddings were generated")
            
        return np.array(all_embeddings)
    
    def encode_documents(self, documents: List[Dict], text_field: str = "content") -> Dict[str, np.ndarray]:
        """
        Generate embeddings for a list of document dictionaries.
        
        Args:
            documents: List of document dictionaries
            text_field: Field name containing the text to embed
            
        Returns:
            Dictionary mapping document IDs to embeddings
        """
        texts = [doc[text_field] for doc in documents]
        ids = [doc["id"] for doc in documents]
        
        embeddings = self.encode(texts, show_progress=True)
        
        return dict(zip(ids, embeddings))
    
    def compute_similarity(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between query and document embeddings.
        
        Args:
            query_embedding: Query embedding
            doc_embeddings: Document embeddings
            
        Returns:
            Similarity scores
        """
        # Ensure embeddings are 2D
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # Normalize embeddings if needed
        query_norm = np.linalg.norm(query_embedding, axis=1, keepdims=True)
        doc_norm = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        
        if not np.all(np.isclose(query_norm, 1.0)) or not np.all(np.isclose(doc_norm, 1.0)):
            query_embedding = query_embedding / query_norm
            doc_embeddings = doc_embeddings / doc_norm
        
        # Compute cosine similarity
        similarity = np.dot(query_embedding, doc_embeddings.T)
        return similarity.flatten() * 100  # Scale to match Jina's scoring
