from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

EMBEDDING_MODEL_NAME = 'l3cube-pune/bengali-sentence-similarity-sbert'

class BengaliEmbeddingModel:
    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        """Initialize Bengali embedding model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name)
        self.model.to(self.device)
        
    def encode(self, texts: List[str], batch_size: int = 8) -> np.ndarray:
        """Generate embeddings for a list of Bengali texts."""
        return self.model.encode(texts, batch_size=batch_size)
        
    def encode_documents(self, documents: List[Dict], text_field: str = "content") -> Dict[str, np.ndarray]:
        """Generate embeddings for a list of document dictionaries."""
        texts = [doc[text_field] for doc in documents]
        ids = [doc["id"] for doc in documents]
        
        embeddings = self.encode(texts)
        
        return dict(zip(ids, embeddings))
        
    def compute_similarity(self, embeddings1: np.ndarray, embeddings2: np.ndarray) -> np.ndarray:
        """Compute cosine similarity between two sets of embeddings."""
        return self.model.similarity(embeddings1, embeddings2)