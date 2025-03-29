from fastapi import FastAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash") # model being used is gemini 1.5 flash

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
        "The story should be short i.e 5-6 lines and engaging, with a cliffhanger. "
        "The story should take place in VIT Vellore campus. "
        "Instead of using the user's name, use 'you' or 'your' to refer to the user. "
        "Do not make the responses sound robotic. "
        "Do not use words, phrases or sentences that break the immersion of the user. "
        "Always end the story with a question asking the user about their decision. "
    )

    vit_specific_guidelines = (
        "The following are the rules of VIT which should be taken into consideration while forming a story: "
        "1. You cannot drink/smoke or indulge in any kind of recreational drugs on campus. "
        "2. No adult content or explicit language. "
        "3. No political or religious content. "
        "4. No public display-of-affection is tolerated by the vit officials. "
        "The user must be allowed to make any choices they want, however, whatever choices they make should be met with appropriate consequences. "
        "The following are some phrases with their associated meanings that should be used in the story whenever applicable: "
        "1. 'VITians' - Students of VIT. "
        "2. 'VIT campus' - The VIT Vellore campus. "
        "3. 'VIT officials' - The authorities of VIT. "
        "4. 'hostels' - The residential buildings of VIT. "
        "5. 'food court' - The food court of VIT. "
        "6. 'library' - The study area of VIT. "
        "7. 'Red Tag Anna' - The disciplinary personnel of VIT. "
        "8. 'shuttle' - The transportation service of VIT. "
        "9. 'vit clinic' - The medical facility of VIT. "
    )

    full_prompt = f"{system_prompt}\n\n{vit_specific_guidelines}\n\n{user_prompt}\n\nContinue the story:"

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([full_prompt])

    if not response.candidates:
        return {"character_story": "Something feels off. The story refuses to unfold. Try again?"}

    generated_text = response.candidates[0].content.parts[0].text.strip()

    return {"character_story": generated_text}


# --------------------------------- POST (/generate) ---------------------------------
# {
#     "name": <name-of-the-user>,
#     "user_input": <characteristic-of-the-user> (if any)
# }
@app.post("/generate")
def generate(data: dict):
    name = data.get("name", "Anonymous")
    user_input = data.get("user_input", "a run-of-the-mill kid stuck in the trials and tribulations of college life")

    prompt = f"Create a story about {name}, who is {user_input}. What bewildering and out-of-the-world situation are they in right now? The user is the one playing right now."
    return generate_story(prompt)
# --------------------------------- POST (/generate) ---------------------------------


# --------------------------------- POST (/continue) ---------------------------------
# {
#     "previous_story": <story-generated-in-the-previous-step>,
#     "user_choice": <choice-made-by-the-user> (if any)
# }
@app.post("/continue")
def continue_story(data: dict):
    previous_story = data.get("previous_story", "")
    user_choice = data.get("user_choice", "")

    prompt = f"Previous situation: {previous_story}\nUser wants to continue with: {user_choice}\n\nContinue the story."

    return generate_story(prompt)
# --------------------------------- POST (/continue) ---------------------------------

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)


## figure out the multiplayer shit
## turn based multiplayer
## instead of creating user accounts, i can have the users as characters in the story
