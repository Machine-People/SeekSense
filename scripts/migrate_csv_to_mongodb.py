#!/usr/bin/env python
# csv_to_mongodb.py

import csv
import os
import argparse
from pymongo import MongoClient
from tqdm import tqdm

def import_csv_to_mongodb(csv_file, mongodb_uri, db_name, collection_name):
    """
    Import data from a CSV file into MongoDB.
    
    Args:
        csv_file: Path to the CSV file
        mongodb_uri: MongoDB connection URI (e.g., mongodb://localhost:27017)
        db_name: MongoDB database name
        collection_name: MongoDB collection name
    """
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Read the CSV file and count total rows for progress bar
    with open(csv_file, 'r', encoding='utf-8') as f:
        total_rows = sum(1 for _ in f)
    
    # Process the CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Insert documents in batches for better performance
        batch_size = 1000
        batch = []
        
        for row in tqdm(reader, total=total_rows-1, desc="Importing data"):
            # Clean up the row - convert empty strings to None
            cleaned_row = {k: (v if v != "" else None) for k, v in row.items()}
            batch.append(cleaned_row)
            
            if len(batch) >= batch_size:
                collection.insert_many(batch)
                batch = []
        
        # Insert any remaining documents
        if batch:
            collection.insert_many(batch)
    
    print(f"Successfully imported {total_rows-1} documents into {db_name}.{collection_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import CSV data into MongoDB")
    parser.add_argument("--csv", required=True, help="Path to the CSV file")
    parser.add_argument("--uri", default="mongodb://localhost:27017", help="MongoDB connection URI")
    parser.add_argument("--db", required=True, help="MongoDB database name")
    parser.add_argument("--collection", required=True, help="MongoDB collection name")
    
    args = parser.parse_args()
    
    import_csv_to_mongodb(args.csv, args.uri, args.db, args.collection)