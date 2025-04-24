# indexing_script.py
import os
import csv
import logging
from data_processing.preprocessing import process_bengali_document
from data_processing.embedding_jina_ai import JinaAIEmbeddingModel
from databases.vector_store import MilvusVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get environment variables
    milvus_host = os.environ.get("MILVUS_HOST", "localhost")
    milvus_port = os.environ.get("MILVUS_PORT", "19530")
    data_path = os.environ.get("DATA_PATH", "data_source/output_final.csv")
    
    logger.info(f"Starting indexing from {data_path}")
    
    # Initialize components
    embedding_model = JinaAIEmbeddingModel()
    vector_store = MilvusVectorStore(host=milvus_host, port=milvus_port)
    
    # Load data from CSV
    documents = []
    with open(data_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Each row: {"title": ..., "description": ...}
            documents.append({"title": row["title"], "description": row["description"]})

    logger.info(f"Loaded {len(documents)} documents from CSV")
    
    # Process in batches
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        # Process documents
        processed_docs = []
        for doc in batch:
            chunks = process_bengali_document(doc)
            processed_docs.extend(chunks)
        
        logger.info(f"Processed batch {i//batch_size + 1}, created {len(processed_docs)} chunks")
        
        # Generate embeddings
        embeddings = embedding_model.encode_documents(processed_docs)
        
        # Store in vector database
        vector_store.insert_documents(processed_docs, embeddings)
        
        logger.info(f"Indexed batch {i//batch_size + 1}")
    
    logger.info("Indexing completed")

if __name__ == "__main__":
    main()
