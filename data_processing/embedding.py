# embedding.py
from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
from typing import List, Dict

EMBEDDING_MODEL_NAME = 'emonnsl/embed_model'

class BengaliEmbeddingModel:
    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        """Initialize Bengali embedding model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        
    def encode(self, texts: List[str], batch_size: int = 8) -> np.ndarray:
        """Generate embeddings for a list of Bengali texts."""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            # Tokenize the batch
            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use CLS token embeddings as sentence representation
                embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                
            all_embeddings.append(embeddings)
            
        return np.vstack(all_embeddings)
        
    def encode_documents(self, documents: List[Dict], text_field: str = "content") -> Dict[str, np.ndarray]:
        """Generate embeddings for a list of document dictionaries."""
        texts = [doc[text_field] for doc in documents]
        ids = [doc["id"] for doc in documents]
        
        embeddings = self.encode(texts)
        
        return dict(zip(ids, embeddings))
