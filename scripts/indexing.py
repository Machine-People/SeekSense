# indexing_script.py
import os
import logging
from data_processing.preprocessing import process_bengali_document
from data_processing.embedding_jina_ai import JinaAIEmbeddingModel
from databases.vector_store import MilvusVectorStore
from utils.mongo_utils import connect_to_mongodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get environment variables
    milvus_host = os.environ.get("MILVUS_HOST", "localhost")
    milvus_port = os.environ.get("MILVUS_PORT", "19530")
    mongo_db_name = os.environ.get("MONGO_DB_NAME", "poridhi_hackathon")
    mongo_collection_name = os.environ.get("MONGO_COLLECTION", "product_data")
    batch_size = int(os.environ.get("BATCH_SIZE", "100"))
    
    logger.info(f"Starting indexing from MongoDB {mongo_db_name}.{mongo_collection_name}")
    
    # Initialize components
    embedding_model = JinaAIEmbeddingModel()
    vector_store = MilvusVectorStore(host=milvus_host, port=milvus_port)
    
    # Connect to MongoDB
    mongo_client = connect_to_mongodb()
    db = mongo_client[mongo_db_name]
    collection = db[mongo_collection_name]
    
    # Count total documents for logging
    total_docs = collection.count_documents({})
    logger.info(f"Found {total_docs} documents in MongoDB")
    
    # Load data from MongoDB in batches
    cursor = collection.find({})
    processed_batch_count = 0
    
    while True:
        # Get the next batch
        batch = list(cursor.limit(batch_size).skip(processed_batch_count * batch_size))
        if not batch:
            break
            
        # Convert MongoDB documents to the format expected by process_bengali_document
        documents = []
        for doc in batch:
            documents.append({
                "id": doc.get("id", str(doc["_id"])),  # Use product_id or _id as fallback
                "title_left": doc.get("title_left", ""),
                "category_left": doc.get("category_left", ""),
                'description_left': doc.get('description_left', ""),
                "title_right": doc.get("title_right", ""),
                "category_right": doc.get("category_right", ""),
                'description_right': doc.get('description_right', ""),
                # Include additional fields that might be useful
                "metadata": {
                    "price": doc.get("price", ""),
                    "quantity": doc.get("quantity", "")
                }
            })
        
        # Process documents
        processed_docs = []
        for doc in documents:
            chunks = process_bengali_document(doc, content_field="description", doc_uid=doc["id"])
            # Add metadata to each chunk
            for chunk in chunks:
                chunk["metadata"] = doc.get("metadata", {})
            processed_docs.extend(chunks)
        
        logger.info(f"Processed batch {processed_batch_count + 1}, created {len(processed_docs)} chunks")
        
        # Generate embeddings
        embeddings = embedding_model.encode_documents(processed_docs)
        
        # Store in vector database
        vector_store.insert_documents(processed_docs, embeddings)
        
        logger.info(f"Indexed batch {processed_batch_count + 1}")
        processed_batch_count += 1
        
        # Check if we've processed all documents
        if processed_batch_count * batch_size >= total_docs:
            break
    
    logger.info("Indexing completed")

if __name__ == "__main__":
    main()
