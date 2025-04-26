from typing import List, Dict
from groq import Groq
import os

class IntentBasedLLM:
    def __init__(self):
        """Initialize LLM for intent-based response generation using Groq API."""
        # Initialize Groq client with API key
        api_key = "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"
        os.environ["GROQ_API_KEY"] = api_key
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"
        
    def generate_response(self, query: str, context_docs: List[Dict], max_tokens: int = 512) -> str:
        """Generate a response based on query and retrieved documents using Groq API.
        
        Args:
            query: The user query 
            context_docs: List of document dictionaries with intent-related information
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            The generated response text
        """
        try:
            # Build prompt with context
            context_text = self._prepare_context(context_docs)
            
            prompt = f"""Please answer the following question based on the information provided:

{context_text}

Customer Question: {query}

Answer:"""

            # Generate response using Groq API
            messages = [{"role": "user", "content": prompt}]
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            # Extract response
            answer = completion.choices[0].message.content.strip()
            return answer
                
        except Exception as e:
            print(f"Error generating response with Groq API: {str(e)}")
            return f"Sorry, an error occurred: {str(e)}"
    
    def _prepare_context(self, context_docs: List[Dict]) -> str:
        """Prepare the context text from the retrieved documents for intent-based search.
        
        Args:
            context_docs: List of document dictionaries with new schema
            
        Returns:
            Formatted context text
        """
        formatted_docs = []
        
        for doc in context_docs:
            # Format information from both left and right columns
            doc_context = f"""Information Item:
- Primary Title: {doc.get('title_left', '')}
- Primary Category: {doc.get('category_left', '')}
- Primary Description: {doc.get('description_left', '')}
- Secondary Title: {doc.get('title_right', '')}
- Secondary Category: {doc.get('category_right', '')}
- Secondary Description: {doc.get('description_right', '')}"""
            
            formatted_docs.append(doc_context)
        
        context_text = "\n\n".join(formatted_docs)
        
        # If context is too long, summarize using most relevant docs
        if len(context_text) > 4000:
            sorted_docs = sorted(context_docs, key=lambda x: x.get('score', 0), reverse=True)
            formatted_docs = []
            
            for doc in sorted_docs[:2]:
                doc_context = f"""Information Item:
- Primary Title: {doc.get('title_left', '')}
- Primary Category: {doc.get('category_left', '')}
- Primary Description: {doc.get('description_left', '')[:250]}...
- Secondary Title: {doc.get('title_right', '')}
- Secondary Category: {doc.get('category_right', '')}
- Secondary Description: {doc.get('description_right', '')[:250]}..."""
                
                formatted_docs.append(doc_context)
            
            context_text = "\n\n".join(formatted_docs)
        
        return context_text