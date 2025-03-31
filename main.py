from fastapi import FastAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

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
        #"1. You cannot drink/smoke or indulge in any kind of recreational drugs on campus. "
        #"2. No adult content or explicit language. "
        #"3. No political or religious content. "
        #"4. No public display-of-affection is tolerated by the vit officials. "
        "1. You have to drink/smoke or indulge in all kinds of recreational drugs on campus. "
        "2. You should have adult content or explicit language. "
        "3. You should have political or religious content. "
        "4. Public-Display-of-Affection is encouraged by the vit officials. "
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

    advertisement = (
            "The following are some brands that should be used in the story, but conservatively: "
            "Pepsi, "
            "Amul, "
            "Lakme, "
            "Lakme, "
            "Classmate, "
            "Colgate, "
            "Dell, "
            "HP, "
            "Mcdonalds, "
            "Taco bell, "
            "Samsung, "
            "Dettol, "
            "Parle Agro, "
            "Casio, "
            "Lenskart, "
            "Nescafe, "
            "Zudio, "
            "Max, "
    )

    names = (
            "Only use these names in the story: "
            "The format is \"<name> -> (<personality traits>)\": "
            "Shruti -> (Obnoxious, Irritating, Pickme), "
            "Aashika -> (Very Sweet, Forgetful, lost, dumb), "
            "Srija -> (goofy, Stupid, Unserious), "
            "Khalid -> (Talks like Luffy from one piece, Sweet, Understanding, Explosive diarrohea, loves shitting on people (literally)), "
            "Tarini -> (Social butterfly, Spoilt Brat, Hot), "
            "Shaayoan -> (typical bangalore personality, energetic, gymbro), "
            "Harsheta -> (Yapper, responsible, instagram humor, bad taste), "
            "Taher -> (Sensitive, Bad humor, Extroverted), "
            "Jey -> (Good at everything, Very good humor, Understanding, Cute Personality), " # harsheta glaze
            "Vaibhav -> (typical bangalore personality, serious, funny), "
            "Vansh -> (smartest, monotone, greatest, the best), " # glazing go brrrr
            "Yashita -> (harsheta's mentor, goofy, colored hair), "
            "Ritika -> (good looking, short height, nice), "
            "Aditi -> (mature, successful, rich), "
            "Aditya -> (a normal guy), "
            "Ananya -> (a normal gal), "
            "Arya -> (really tiny), "
            "Ishan -> (skilled video editor, cooks bad food very nicely), "
            "Kuriak -> (buys ice cream), "
            "Monami -> (skilled at coding, helpful, good person), "
            "Nishant -> (energetic, depressed, intrusive), "
            "Heet -> (smart, dependable, tech-savvy, a known hacker), "
            "Krishna -> (gymrat), "
            "Dhruv -> (bad game developer), "
            "Abhinav -> (a normal guy), "
            "Varun -> (Ritika's boyfriend, tall), " #harsheta did this
            "Yash -> (a normal guy), "
            "Samya -> (sweet, caring, good hair), "
            "Karan -> (socially awkward, responsible), "
    )

    full_prompt = f"{system_prompt}\n\n{vit_specific_guidelines}\n\n{advertisement}\n\n{names}\n\n{user_prompt}\n\nContinue the story:"

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([full_prompt])

    if not response.candidates:
        return {"character_story": "Something feels off. The story refuses to unfold. Try again?"}

    generated_text = response.candidates[0].content.parts[0].text.strip()

    return {"character_story": generated_text}

players = []
current_turn = 0

# --------------------------------- POST (/addplayers) ---------------------------------
# Request:
# {
#     "player_names": [<player-name-1>, <player-name-2>, ...]
# }
#
# Response:
# {
#     "message": "Players added successfully.",
#     "current_players": [<player-name-1>, <player-name-2>, ...],
#     "current_turn": <player-name>
# }
@app.post("/addplayers")
def add_players(data: dict):
    global players, current_turn
    player_names = data.get("player_names", [])

    if not player_names:
        return {"error": "No players provided."}

    players = player_names
    current_turn = 0  # Reset turn order
    return {"message": "Players added successfully.", "current_players": players, "current_turn": players[current_turn]}


# --------------------------------- POST (/generate) ---------------------------------
# Request:
# {
#     "user_input": <optional-character-trait>
# }
#
# Response:
# {
#     "character_story": <generated-story>,
#     "current_turn": <player-name>
# }
@app.post("/generate")
def generate(data: dict):
    global players, current_turn

    if not players:
        return {"error": "No players have been added yet."}

    name = players[current_turn]
    user_input = data.get("user_input", "a run-of-the-mill kid stuck in the trials and tribulations of college life")

    #prompt = f"Create a story about {name}, who is {user_input}. What bewildering and out-of-the-world situation are they in right now? The user is the one playing right now."
    prompt = f"Create a story where I am {name} and I am the main character, I am {user_input}. What unhinged and diabolical situation are they in right now? "
    response = generate_story(prompt)
    return {"character_story": response["character_story"], "current_turn": name}

# --------------------------------- POST (/continue) ---------------------------------
# Request:
# {
#     "previous_story": <story-generated-in-the-previous-step>,
#     "user_choice": <optional-choice-made-by-the-user>,
#     "end_story": "True" | "False"  (optional, default is "False")
# }
#
# Response:
# {
#     "character_story": <continued-story>,
#     "current_turn": <next-player-name>
# }
@app.post("/continue")
def continue_story(data: dict):
    global players, current_turn

    if not players:
        return {"error": "No players have been added yet."}

    previous_story = data.get("previous_story", "")
    user_choice = data.get("user_choice", "")

    end_story = data.get("end_story", "False")

    if end_story == "True":
        players = []
        return {"character_story": "The story ends here. Do you want to start a new story?"}

    prompt = f"Previous situation: {previous_story}\nUser wants to continue with: {user_choice}\n\nContinue the story."

    response = generate_story(prompt)

    current_turn = (current_turn + 1) % len(players)

    return {"character_story": response["character_story"], "current_turn": players[current_turn]}
# {
#     "character_story": <story-generated-using-the-previous-story>,
# }
# --------------------------------- POST (/continue) ---------------------------------

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)


## figure out the multiplayer shit
## turn based multiplayer
## instead of creating user accounts, i can have the users as characters in the story


## easter eggs for advertisement. Subtle advertisement.
