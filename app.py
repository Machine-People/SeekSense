import json
from fastapi import FastAPI, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi import FastAPI, Query
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import cachetools
import requests
import json
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import numpy as np
from fastapi import HTTPException
app = FastAPI()
import pandas as pd
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(
    "./VecDB", 
    embeddings, 
    allow_dangerous_deserialization=True
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are  Intelligence System, an expert assistant. "
         "Your responses should always be accurate, concise, and relevant to the query."),
        

        ("assistant", 
         "Hello! I am an Intelligence. How can I assist you today?"),

        ("user", "Question: {input}\n   Context: {context}")
    ]
)
output_parser=StrOutputParser()

llm = Ollama(model="llama3.2")
document_chain = create_stuff_documents_chain(llm, prompt)
from functools import lru_cache
@lru_cache(maxsize=100) 
def cached_retrieval_chain(question: str):
    retriever = db.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    retrieval_chain = retrieval_chain.invoke({"input": question})
    return retrieval_chain['answer']

@app.get("/query/")
async def query_llm(question: str):
    try:

        answer = cached_retrieval_chain(question)
        formatted_response = answer.replace("AI:", "")\
                                    .replace("System:", "")\
                                    .replace("Answers:", "")\
                                    .replace("Answer:", "")\
                                    .replace("Human:", "")
        
        return {"response": formatted_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
