from fastapi import FastAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai

import re

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

def generate_story(user_prompt: str, include_choices: bool = False):
    system_prompt = (
        "You are an AI storyteller creating immersive university life stories. "
        "Write in the present tense and engage the user naturally. "
        "Keep events realistic and within campus life, unless a supernatural or mystery element emerges."
    )

    if include_choices:
        system_prompt += (
            " After narrating the scene, end with **three new choices** for what the protagonist can do next. "
            "Ensure these choices are **unique** and logically follow from the story. Format them as:"
            "\n- Choice A: [A brief but clear action]"
            "\n- Choice B: [A different but valid action]"
            "\n- Choice C: [Another possible action]"
        )

    
    full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nContinue the story:"

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(full_prompt)

    generated_text = response.text.strip() if hasattr(response, "text") else ""

    if not generated_text:
        return {
            "character_story": "Something feels off. The story refuses to unfold. Try again?",
            "choices": [
                "A) Investigate your surroundings",
                "B) Examine the glowing book",
                "C) Call out to see if anyone else is here"
            ]
        }



    parts = re.split(r"\n-\s*Choice\s*A:", generated_text)
    story = parts[0].strip()

    if len(parts) > 1:
        choices_text = "- Choice A:" + parts[1]
        choices = re.findall(r"- Choice [A-C]: .*", choices_text)
    else:
        choices = [
            "A) Explore more of the campus",
            "B) Talk to nearby students",
            "C) Head to the library"
        ]

    return {
        "character_story": story,
        "choices": choices
    }

@app.post("/generate")
def generate(data: dict):
    name = data.get("name", "Anonymous")
    user_input = data.get("user_input", "a run-of-the-mill kid stuck in the trials and tribulations of college life")

    prompt = f"Create a story about {name}, who is {user_input}. What bewildering and out-of-the-world situation are they in right now?"
    return generate_story(prompt)

@app.post("/continue")
def continue_story(data: dict):
    name = data.get("name", "")
    user_input = data.get("user_input", "")
    previous_story = data.get("previous_story", "")
    selected_choice = data.get("selected_choice", "")

    prompt = (
        f"Previous situation: {previous_story}\n"
        f"{name} decided to: {selected_choice}\n"
        f"Context: {user_input}\n"
        f"What happens next?"
    )

    return generate_story(prompt)

