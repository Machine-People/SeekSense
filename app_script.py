# debug_search.py

import json
import numpy as np
from typing import List, Dict, Optional

# Import your existing modules
from data_processing.preprocessing import normalize_bengali_text, process_bengali_document
from data_processing.embedding_jina_ai import JinaAIEmbeddingModel
from databases.vector_store import MilvusVectorStore
from classification.intent_classification import BengaliIntentClassifier
from classification.llm import BengaliLLM

def main():
    """Main function to debug the RAG pipeline."""
    # Initialize components
    print("Initializing components...")
    embedding_model = JinaAIEmbeddingModel()
    vector_store = MilvusVectorStore(host="localhost", port="19530")
    intent_classifier = BengaliIntentClassifier()
    llm = BengaliLLM()
    
    # Get user query
    # query = "সবচেয়ে ছোট অর্গানিক মধু"
    query = "উৎসবের জন্য শাড়ি"
    top_k = 3
    
    try:
        print("\n===== PROCESSING QUERY =====")
        print(f"Original query: {query}")
        
        # 1. Normalize query (commenting out due to the utf-8 error in your normalize_bengali_text function)
        query = normalize_bengali_text(query)
        print(f"Normalized query: {query}")
        
        # 2. Classify intent
        print("\n===== INTENT CLASSIFICATION =====")
        intent, confidence = intent_classifier.classify_intent(query)
        print(f"Detected intent: {intent} (confidence: {confidence:.4f})")
        
        # 3. Extract entities
        entities = intent_classifier.extract_entities(query)
        print(f"Extracted entities: {entities}")
        
        # 4. Generate query embedding
        print("\n===== GENERATING EMBEDDINGS =====")
        print("Generating query embedding...")
        query_embedding = embedding_model.encode([query])[0]
        print(f"Embedding shape: {query_embedding.shape}")
        
        # 5. Search for relevant documents
        print("\n===== VECTOR SEARCH =====")
        print(f"Searching for top {top_k} relevant documents...")
        search_results = vector_store.similarity_search(
            query_embedding,
            limit=top_k
        )
        search_results1 = vector_store.similarity_search_with_reassembly(query_embedding=query_embedding, limit=top_k)
        print(f"Found {len(search_results)} results")
        
        # Display search results
        for i, doc in enumerate(search_results):
            print(f"\nResult {i+1}:")
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Content: {doc.get('content', 'N/A')[:100]}...")
            # print(f"  Score: {doc.get('score', 0):.4f}")
        for i, doc in enumerate(search_results1):
            print(f"\nResult {i+1}:")
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Content: {doc.get('content', 'N/A')[:100]}...")
            # print(f"  Score: {doc.get('score', 0):.4f}")
        # 6. Generate response using LLM
        print("\n===== LLM RESPONSE GENERATION =====")
        # TODO query into the data using the title and get the description quantity, price etc
        # data = {
        #     description: doc.get('content', 'N/A'),
        # }

        print("Generating response...")
        response = llm.generate_response(query, search_results1) # pass the data into the llm 
        
        # 7. Display final results
        print("\n===== FINAL RESULTS =====")
        print(f"Query: {query}")
        print(f"Intent: {intent} (confidence: {confidence:.4f})")
        print(f"Entities: {entities}")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
