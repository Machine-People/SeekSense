import os
import csv
import logging
from data_processing.embedding_jina_ai import JinaAIEmbeddingModel
from data_processing.preprocessing import process_bengali_document
from data_processing.embedding import BengaliEmbeddingModel
from databases.vector_store import MilvusVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get environment variables
    milvus_host = os.environ.get("MILVUS_HOST", "localhost")
    milvus_port = os.environ.get("MILVUS_PORT", "19530")
    data_path = os.environ.get("DATA_PATH", "data_source/preprocess_dataset.csv")
    
    logger.info(f"Starting indexing from {data_path}")
    
    # Initialize components
    embedding_model = JinaAIEmbeddingModel()
    vector_store = MilvusVectorStore(host=milvus_host, port=milvus_port)
    
    # Load data from CSV
    documents = []
    with open(data_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Each row contains paired product data
            documents.append({
                "id": row["id"],
                "title_left": row["title_left"],
                "category_left": row["category_left"],
                "description_left": row["description_left"],
                "title_right": row["title_right"], 
                "category_right": row["category_right"],
                "description_right": row["description_right"]
            })

    logger.info(f"Loaded {len(documents)} product comparison pairs from CSV")
    
    # Process in batches
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        # Process documents - need to update process_bengali_document to handle paired structure
        processed_docs = []
        for doc in batch:
            # For each document pair, create a combined representation for embedding
            combined_text = f"{doc['title_left']} {doc['category_left']} {doc['description_left']} {doc['title_right']} {doc['category_right']} {doc['description_right']}"
            
            # Create a document object for vector storage
            processed_doc = {
                "id": doc["id"],
                "title_left": doc["title_left"],
                "category_left": doc["category_left"],
                "description_left": doc["description_left"],
                "title_right": doc["title_right"],
                "category_right": doc["category_right"],
                "description_right": doc["description_right"],
                "content": combined_text  # For embedding purposes
            }
            processed_docs.append(processed_doc)
        
        logger.info(f"Processed batch {i//batch_size + 1}, created {len(processed_docs)} documents")
        
        # Generate embeddings based on combined text
        embeddings = embedding_model.encode_documents(processed_docs)
        
        # Store in vector database
        vector_store.insert_documents(processed_docs, embeddings)
        
        logger.info(f"Indexed batch {i//batch_size + 1}")
    
    logger.info("Indexing completed")

if __name__ == "__main__":
    main()