# client.py
import requests
import json
import sys

def query_system(query, url="http://localhost:8000/query"):
    """Send a query to the Bengali search system."""
    response = requests.post(
        url,
        json={"query": query, "top_k": 3}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Query: {result['query']}")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print(f"Entities: {json.dumps(result['entities'], ensure_ascii=False)}")
        print("\nSearch Results:")
        for i, doc in enumerate(result['search_results']):
            print(f"  {i+1}. {doc['title']} (score: {doc['score']:.2f})")
            print(f"     {doc['content'][:100]}...")
        print("\nResponse:")
        print(result['response'])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("Enter your Bengali query: ")
    
    query_system(query)
