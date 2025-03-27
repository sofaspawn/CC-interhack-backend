from fastapi import FastAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_story(user_prompt: str):
    system_prompt = (
        "You are an AI storyteller creating immersive university life stories. "
        "Write in the present tense and engage the user naturally. "
        "You are talking to user directly, address them in second person. "
        "Keep events realistic and within campus life, unless a supernatural or mystery element emerges. "
        "Continue the story based on the user's input naturally, without listing choices."
        "The story should be short i.e 5-6 lines and engaging, witha a cliffhanger. "
        "The story should take place in VIT Vellore campus. "
        "Instead of using the user's name, use 'you' or 'your' to refer to the user. "
        "Do not make the responses sound robotic. "
    )

    full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nContinue the story:"

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([full_prompt])

    if not response.candidates:
        return {"character_story": "Something feels off. The story refuses to unfold. Try again?"}

    generated_text = response.candidates[0].content.parts[0].text.strip()

    return {"character_story": generated_text}

@app.post("/generate")
def generate(data: dict):
    name = data.get("name", "Anonymous")
    user_input = data.get("user_input", "a run-of-the-mill kid stuck in the trials and tribulations of college life")

    prompt = f"Create a story about {name}, who is {user_input}. What bewildering and out-of-the-world situation are they in right now?"
    return generate_story(prompt)

@app.post("/continue")
def continue_story(data: dict):
    previous_story = data.get("previous_story", "")
    user_input = data.get("user_input", "")

    prompt = f"Previous situation: {previous_story}\nUser wants to continue with: {user_input}\n\nContinue the story."

    return generate_story(prompt)

