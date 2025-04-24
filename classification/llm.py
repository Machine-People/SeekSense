# # llm_integration.py
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# from typing import List, Dict
# from llama_cpp import Llama
# # TODO use the llama cpp for the inference
# class BengaliLLM:
#     def __init__(self, model_name="unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"):
#         """Initialize Bengali LLM for response generation."""
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = Llama.from_pretrained(repo_id="mradermacher/BanglaLLama-3.1-8b-bangla-alpaca-orca-instruct-v0.0.1-GGUF", filename="BanglaLLama-3.1-8b-bangla-alpaca-orca-instruct-v0.0.1.Q6_K.gguf", local_dir="/media/escobar/C85A85AC5A8597B8/Hackathon/Poridhi_Hacka/SeekSense/models")
#         # self.model.to(self.device)
#         # self.model.eval()
        
#     def generate_response(self, query: str, context_docs: List[Dict], max_length: int = 512) -> str:
#         """Generate a response based on query and retrieved documents."""
#         # Build prompt with context
#         context_text = "\n\n".join([f"পণ্যের শিরোনাম: {doc['title']}\nবিবরণ: {doc['content']}" 
#                                   for doc in context_docs])
        
#         prompt = f"""নিম্নলিখিত পণ্যের তথ্য ব্যবহার করে প্রশ্নের উত্তর দিন:

# {context_text}

# গ্রাহকের প্রশ্ন: {query}

# উত্তর:"""
        
#         # Generate response
#         # inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        
#         outputs = self.model.create_chat_completion(messages=[{"role": "user", "content": prompt}])

#         print(outputs)
#         import time
#         # time.sleep(100)    
#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         # Extract just the generated answer part
#         answer = response.split("উত্তর:")[-1].strip()
        
#         return outputs


# llm_integration.py
from typing import List, Dict
from llama_cpp import Llama

class BengaliLLM:
    def __init__(self, model_path=None):
        """Initialize Bengali LLM for response generation.
        
        Args:
            model_path: Optional custom path to the model file. If None, uses default path.
        """
        # Initialize the model using llama-cpp
        default_path = "/media/escobar/C85A85AC5A8597B8/Hackathon/Poridhi_Hacka/SeekSense/models"
        
        self.model = Llama.from_pretrained(
            repo_id="mradermacher/BanglaLLama-3.2-3b-bangla-alpaca-orca-instruct-v0.0.1-GGUF", 
            filename="BanglaLLama-3.2-3b-bangla-alpaca-orca-instruct-v0.0.1.Q8_0.gguf", 
            local_dir=model_path or default_path,
            # Setting context window and other parameters
            n_ctx=2048,  # Increased context window
            verbose=False
        )
    
    def generate_response(self, query: str, context_docs: List[Dict], max_tokens: int = 512) -> str:
        """Generate a response based on query and retrieved documents.
        
        Args:
            query: The user query in Bengali
            context_docs: List of document dictionaries with 'title' and 'content' fields
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            The generated response text
        """
        # Build prompt with context
        context_text = "\n\n".join([
            f"পণ্যের শিরোনাম: {doc.get('title', '')}\nবিবরণ: {doc.get('content', '')}"
            for doc in context_docs
        ])
        
        # Shorter context if too long
        if len(context_text) > 4000:
            # Take most relevant docs based on score
            sorted_docs = sorted(context_docs, key=lambda x: x.get('score', 0), reverse=True)
            context_text = "\n\n".join([
                f"পণ্যের শিরোনাম: {doc.get('title', '')}\nবিবরণ: {doc.get('content', '')[:500]}..." 
                for doc in sorted_docs[:2]
            ])
        
        prompt = f"""নিম্নলিখিত পণ্যের তথ্য ব্যবহার করে প্রশ্নের উত্তর দিন:

{context_text}

গ্রাহকের প্রশ্ন: {query}

উত্তর:"""

        try:
            # Generate response using chat completion
            print(prompt)
            response = self.model.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
            )
            
            # Extract the assistant's message from the response
            if response and "choices" in response and len(response["choices"]) > 0:
                answer = response["choices"][0]["message"]["content"].strip()
                return answer
            else:
                return "দুঃখিত, আমি এই প্রশ্নের উত্তর দিতে পারছি না।"  # Sorry, I can't answer this question
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"  # Sorry, an error occurred
