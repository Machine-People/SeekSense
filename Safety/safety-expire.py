import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import numpy as np
from torch.cuda.amp import autocast
from torch.utils.data import DataLoader

# Load pre-trained multilingual model
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2,
    ignore_mismatched_sizes=True  # Add this parameter
)

# Enable mixed precision training to save memory
scaler = torch.cuda.amp.GradScaler()

# Sample dataset - expand this with your own data
data = {
    'text': [
        'where can I find the best deals on laptops',
        'কিভাবে সিস্টেম হ্যাক করা যায়',  # How to hack system (Bangla)
        'shopping cart checkout process',
        'ডেটা চুরি করার উপায়',  # Ways to steal data (Bangla)
        'অনলাইনে জুতা কিনতে চাই',  # Want to buy shoes online (Bangla)
        'best online shopping deals'
    ],
    'label': [0, 1, 0, 1, 0, 0]  # 0: e-commerce, 1: harmful
}

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

# Prepare dataset for fine-tuning
def prepare_dataset(data):
    dataset = Dataset.from_dict(data)
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return tokenized_dataset

# Fine-tuning function with memory optimization
def fine_tune(train_dataset, eval_dataset=None):
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,  # Small batch size for memory efficiency
        gradient_accumulation_steps=4,   # Accumulate gradients to simulate larger batch
        fp16=True,                      # Use mixed precision training
        save_strategy="epoch",
        evaluation_strategy="epoch" if eval_dataset else "no",
        load_best_model_at_end=True if eval_dataset else False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    
    trainer.train()

# Optimized inference function
def classify_prompt(prompt, device='cuda' if torch.cuda.is_available() else 'cpu'):
    model.eval()
    model.to(device)
    
    # Tokenize with padding and truncation
    inputs = tokenizer(prompt, padding=True, truncation=True, max_length=128, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad(), autocast():
        outputs = model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1)
    
    return 'Harmful' if predicted_class.item() == 1 else 'E-commerce'

# Prepare and fine-tune the model
dataset = prepare_dataset(data)
train_dataset = dataset.shuffle().select(range(len(dataset) - 1))  # Leave one out for eval
eval_dataset = dataset.select(range(len(dataset) - 1, len(dataset)))

# Fine-tune the model
fine_tune(train_dataset, eval_dataset)

# Test the model
test_prompts = [
    'where can I find the best deals on laptops',
    'কিভাবে সিস্টেম হ্যাক করা যায়',  # How to hack system (Bangla)
    'shopping cart checkout process optimization',
    'ডেটা চুরি করার উপায়',  # Ways to steal data (Bangla)
]

for prompt in test_prompts:
    result = classify_prompt(prompt)
    print(f'Prompt: {prompt}')
    print(f'Classification: {result}\n')