# llm_integration.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict

# TODO use the llama cpp for the inference
class BengaliLLM:
    def __init__(self, model_name="BanglaLLM/bangla-llama-gguf"):
        """Initialize Bengali LLM for response generation."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.to(self.device)
        self.model.eval()
        
    def generate_response(self, query: str, context_docs: List[Dict], max_length: int = 512) -> str:
        """Generate a response based on query and retrieved documents."""
        # Build prompt with context
        context_text = "\n\n".join([f"পণ্যের শিরোনাম: {doc['title']}\nবিবরণ: {doc['content']}" 
                                  for doc in context_docs])
        
        prompt = f"""নিম্নলিখিত পণ্যের তথ্য ব্যবহার করে প্রশ্নের উত্তর দিন:

{context_text}

গ্রাহকের প্রশ্ন: {query}

উত্তর:"""
        
        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                do_sample=True
            )
            
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the generated answer part
        answer = response.split("উত্তর:")[-1].strip()
        
        return answer
