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
        self._ensure_collection(dim=1024)
        
    def _ensure_collection(self, dim: int = 1024):
        """Create collection if it doesn't exist."""
        if utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name)
        else:
            # Define fields for the collection
            id,title_left,category_left,description_left,title_right,category_right,description_right
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
                FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="category_left", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="description_left", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="title_right", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="category_right", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="description_right", dtype=DataType.VARCHAR, max_length=65535),
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
        category_lefts = []
        description_lefts = []
        title_rights = []
        category_rights = []
        description_rights = []
        chunk_indices = []
        total_chunks_list = []
        embedding_vectors = []
        
        MAX_TEXT_LENGTH = 100000

        for doc in documents:
            doc_id = doc["id"]
            if doc_id in embeddings:
                ids.append(doc_id)
                # Truncate fields to allowed lengths
                titles.append(doc.get("title", "")[:MAX_TEXT_LENGTH])
                category_lefts.append(doc.get("category_left", "")[:MAX_TEXT_LENGTH])
                description_lefts.append(doc.get("description_left", "")[:MAX_TEXT_LENGTH])
                title_rights.append(doc.get("title_right", "")[:MAX_TEXT_LENGTH])
                category_rights.append(doc.get("category_right", "")[:MAX_TEXT_LENGTH])
                description_rights.append(doc.get("description_right", "")[:MAX_TEXT_LENGTH])
                chunk_indices.append(doc.get("chunk_index", 0))
                total_chunks_list.append(doc.get("total_chunks", 1))
                embedding_vectors.append(embeddings[doc_id].tolist())
        
        # Insert data
        entities = [
            ids, 
            titles, 
            category_lefts,
            description_lefts,
            title_rights,
            category_rights,
            description_rights,
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
            output_fields=["id", "title", "category_left", "description_left", "title_right", "category_right", "description_right", "chunk_index", "total_chunks"]
        )
        
        hits = []
        for hit in results[0]:
            hits.append({
                "id": hit.id,
                "title": hit.entity.get("title"),
                "category_left": hit.entity.get("category_left"),
                "description_left": hit.entity.get("description_left"),
                "title_right": hit.entity.get("title_right"),
                "category_right": hit.entity.get("category_right"),
                "description_right": hit.entity.get("description_right"),
                "chunk_index": hit.entity.get("chunk_index"),
                "total_chunks": hit.entity.get("total_chunks"),
                "score": hit.score
            })
            
        return hits

    def similarity_search_with_reassembly(self, query_embedding: np.ndarray, limit: int = 3, reassemble: bool = True) -> List[Dict]:
        """
        Search for similar documents and reassemble full documents when needed.
        
        Args:
            query_embedding: Embedding vector for the query
            limit: Maximum number of reassembled documents to return
            reassemble: Whether to reassemble chunks into complete documents
            
        Returns:
            List of documents with reassembled content when possible
        """
        # First get matching chunks (higher initial limit to account for duplicates)
        initial_limit = limit * 3 if reassemble else limit
        chunk_hits = self.similarity_search(query_embedding, limit=initial_limit)
        
        if not reassemble:
            return chunk_hits[:limit]
        
        # Group by document (assuming id format is {base_id}_chunk_{i})
        docs_by_id = {}
        for hit in chunk_hits:
            # Extract base_id from chunk id
            if "_chunk_" not in hit["id"]:
                # Not a chunked document
                base_id = hit["id"]
                if base_id not in docs_by_id:
                    docs_by_id[base_id] = {
                        "base_id": base_id,
                        "title": hit["title"],
                        "category_left": hit["category_left"],
                        "description_left": hit["description_left"],
                        "title_right": hit["title_right"],
                        "category_right": hit["category_right"],
                        "description_right": hit["description_right"],
                        "chunks": [{"content": "", "chunk_index": 0, "score": hit["score"]}],
                        "top_score": hit["score"]
                    }
                continue
                
            base_id = hit["id"].rsplit("_chunk_", 1)[0]
            if base_id not in docs_by_id:
                docs_by_id[base_id] = {
                    "base_id": base_id,
                    "title": hit["title"], 
                    "category_left": hit["category_left"],
                    "description_left": hit["description_left"],
                    "title_right": hit["title_right"],
                    "category_right": hit["category_right"],
                    "description_right": hit["description_right"],
                    "chunks": [],
                    "top_score": hit["score"]  # Keep track of best chunk score
                }
            docs_by_id[base_id]["chunks"].append({
                "content": "",
                "chunk_index": hit["chunk_index"],
                "score": hit["score"]
            })
            # Update top score if this chunk has a better score
            if hit["score"] > docs_by_id[base_id]["top_score"]:
                docs_by_id[base_id]["top_score"] = hit["score"]
        
        # Reassemble documents
        reassembled_docs = []
        for doc_id, doc in docs_by_id.items():
            # Sort chunks by index
            doc["chunks"].sort(key=lambda x: x["chunk_index"])
            
            # Check if we have all chunks
            have_all_chunks = False
            if len(doc["chunks"]) == 1 and "total_chunks" not in chunk_hits[0]:
                # Single chunk document
                have_all_chunks = True
            else:
                # Get the total chunks from any chunk in this document
                total_chunks = None
                for hit in chunk_hits:
                    if hit["id"].startswith(doc_id + "_chunk_"):
                        total_chunks = hit["total_chunks"]
                        break
                
                if total_chunks is not None and len(doc["chunks"]) >= total_chunks:
                    have_all_chunks = True
            
            # If we don't have all chunks, fetch the missing ones
            if not have_all_chunks:
                missing_chunks = self._fetch_missing_chunks(doc_id, doc["chunks"], total_chunks)
                # Integrate missing chunks
                doc["chunks"].extend(missing_chunks)
                # Resort chunks after adding missing ones
                doc["chunks"].sort(key=lambda x: x["chunk_index"])
            
            # Reassemble content
            full_content = ""
            
            reassembled_docs.append({
                "id": doc_id,
                "title": doc["title"],
                "category_left": doc["category_left"],
                "description_left": doc["description_left"],
                "title_right": doc["title_right"],
                "category_right": doc["category_right"],
                "description_right": doc["description_right"],
                "content": full_content,
                "score": doc["top_score"]
            })
        
        # Sort by score and limit results
        reassembled_docs.sort(key=lambda x: x["score"], reverse=True)
        return reassembled_docs[:limit]

    def _fetch_missing_chunks(self, base_id: str, existing_chunks: List[Dict], total_chunks: int = None) -> List[Dict]:
        """
        Fetch missing chunks for a document.
        
        Args:
            base_id: Base document ID
            existing_chunks: Chunks we already have
            total_chunks: Total number of chunks in the document
            
        Returns:
            List of missing chunks
        """
        # If we don't know the total number of chunks, try to find out
        if total_chunks is None:
            # Try to get it from an existing chunk
            for chunk in existing_chunks:
                if hasattr(chunk, 'total_chunks'):
                    total_chunks = chunk.total_chunks
                    break
                    
            if total_chunks is None:
                # Query for any chunk to get total_chunks
                results = self.collection.query(
                    expr=f'id like "{base_id}_chunk_%" limit 1',
                    output_fields=["total_chunks"]
                )
                if results and "total_chunks" in results[0]:
                    total_chunks = results[0]["total_chunks"]
                else:
                    # Can't determine total chunks, return what we have
                    return []
        
        # Determine which chunks we're missing
        existing_indices = {chunk["chunk_index"] for chunk in existing_chunks}
        missing_indices = [i for i in range(total_chunks) if i not in existing_indices]
        
        if not missing_indices:
            return []
        
        # Construct query to get all missing chunks in one operation
        chunk_ids = [f'"{base_id}_chunk_{idx}"' for idx in missing_indices]
        id_list = ", ".join(chunk_ids)
        expr = f'id in [{id_list}]'
        
        try:
            results = self.collection.query(
                expr=expr,
                output_fields=["id", "chunk_index"]
            )
        except Exception as e:
            # If the query is too long or has other issues, fall back to individual queries
            results = []
            for idx in missing_indices:
                try:
                    chunk_results = self.collection.query(
                        expr=f'id == "{base_id}_chunk_{idx}"',
                        output_fields=["id", "chunk_index"]
                    )
                    results.extend(chunk_results)
                except Exception:
                    pass
        
        missing_chunks = []
        for result in results:
            missing_chunks.append({
                "content": "",
                "chunk_index": result["chunk_index"],
                "score": 0  # These weren't in the initial results
            })
        
        return missing_chunks
