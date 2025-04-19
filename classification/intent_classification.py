# intent_classification.py
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F
from typing import Dict, Tuple, List

class BengaliIntentClassifier:
    def __init__(self, model_name="sagorsarker/bangla-bert-base"):
        """Initialize Bengali intent classifier."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
        self.model.to(self.device)
        self.model.eval()
        
        # Intent labels - can be expanded as needed
        self.intent_labels = ["product_search", "feature_inquiry", "price_inquiry"]
        
    def classify_intent(self, query: str) -> Tuple[str, float]:
        """Classify the intent of a Bengali query."""
        inputs = self.tokenizer(
            query,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class].item()
            
        return self.intent_labels[predicted_class], confidence
    
    def extract_entities(self, query: str) -> Dict[str, str]:
        """Extract relevant entities from the query using rule-based approach."""
        # This is a simplified version - in production, you would use NER
        entities = {}
        
        # Example simple rules for extracting product categories
        if "মোবাইল" in query or "ফোন" in query:
            entities["category"] = "electronics"
        elif "জুতা" in query or "জামা" in query:
            entities["category"] = "clothing"
            
        return entities
