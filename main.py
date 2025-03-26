from fastapi import FastAPI
import requests

import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_story(prompt: str):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.get("/generate")
def generate(name: str, user_input: str):
    prompt = f"Imagine a student at VIT named {name}. They describe themselves as '{user_input}'. Generate a fun alternate university life story for them."
    result = generate_story(prompt)
    return {"character_story": result}
