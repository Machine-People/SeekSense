# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import numpy as np
from typing import List, Dict, Optional

from data_processing.preprocessing import normalize_bengali_text, process_bengali_document
from data_processing.embedding import BengaliEmbeddingModel
from databases.vector_store import MilvusVectorStore
from classification.intent_classification import BengaliIntentClassifier
from classification.llm import BengaliLLM

app = FastAPI()

# Initialize components
embedding_model = BengaliEmbeddingModel()
vector_store = MilvusVectorStore(host="localhost", port="19530")
intent_classifier = BengaliIntentClassifier()
llm = BengaliLLM()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class IndexRequest(BaseModel):
    documents: List[Dict]

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a Bengali query using the RAG pipeline."""
    try:
        # Normalize query
        query = normalize_bengali_text(request.query)
        
        # Classify intent
        intent, confidence = intent_classifier.classify_intent(query)
        
        # Extract entities if needed
        entities = intent_classifier.extract_entities(query)
        
        # Generate query embedding
        query_embedding = embedding_model.encode([query])[0]
        
        # Search for relevant documents
        search_results = vector_store.similarity_search(
            query_embedding,
            limit=request.top_k
        )
        
        # Generate response using LLM
        response = llm.generate_response(query, search_results)
        
        return {
            "query": query,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "search_results": search_results,
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
async def index_documents(request: IndexRequest):
    """Index Bengali documents into the vector store."""
    try:
        # Process documents
        processed_docs = []
        for doc in request.documents:
            chunks = process_bengali_document(doc)
            processed_docs.extend(chunks)
        
        # Generate embeddings
        embeddings = embedding_model.encode_documents(processed_docs)
        
        # Store in vector database
        vector_store.insert_documents(processed_docs, embeddings)
        
        return {"status": "success", "indexed_count": len(processed_docs)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
