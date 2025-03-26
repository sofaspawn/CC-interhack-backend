from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_story(user_prompt: str):
    system_prompt = (
        "You are an advanced AI storyteller specializing in creating engaging and immersive university life stories. "
        "You will craft a unique alternate life story for a VIT student based on their name and self-description."
    )
    
    full_prompt = f"{system_prompt}\nUser Input: {user_prompt}\nStory:"
    
    payload = {"inputs": full_prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    response_data = response.json()
    
    generated_text = response_data[0]["generated_text"] if isinstance(response_data, list) else response_data.get("generated_text", "")
    
    cleaned_story = generated_text.split("Story:")[-1].strip() if "Story:" in generated_text else generated_text
    
    return {"character_story": cleaned_story}

@app.post("/generate")
def generate(data: dict):
    name = data.get("name", "Anonymous")
    user_input = data.get("user_input", "a curious student exploring VIT.")

    prompt = f"Imagine a student at VIT named {name}. They describe themselves as '{user_input}'. Generate a fun alternate university life story for them."
    result = generate_story(prompt)

    return {"character_story": result}

