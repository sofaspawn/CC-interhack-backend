# CC Interhack Backend  
Backend for Interhack  

## TODO:  
- [x] Setup basic script  
- [x] Find a functioning AI model  
- [x] Implement the AI model  
- [x] Improve system prompt  
- [x] Get the model to hold context  
- [x] Generate better stories  

- [x] Add VIT guidelines  
- [ ] Improve VIT guidelines  

- [x] Implement multiplayer (turn-based system)  
- [ ] Refine multiplayer mechanics  

## 📡 API Endpoints  

| Method  | Endpoint     | Request Format | Response Format |
|---------|-------------|----------------|----------------|
| **POST** | `/addplayers`  | `{ "player_names": ["<player1>", "<player2>", ...] }` | `{ "message": "Players added successfully.", "current_players": ["<player1>", "<player2>", ...], "current_turn": "<player>" }` |
| **POST** | `/generate`  | `{ "user_input": "<optional-character-trait>" }` | `{ "character_story": "<generated-story>", "current_turn": "<player>" }` |
| **POST** | `/continue`  | `{ "previous_story": "<story-generated-in-the-previous-step>", "user_choice": "<optional-choice-made-by-the-user>", "end_story": "True" \| "False" (default: "False") }` | `{ "character_story": "<continued-story>", "current_turn": "<next-player>" }` |

### 📝 Notes:
- **Turn-based Multiplayer**: The system cycles through players, allowing each to contribute to the story sequentially.
- **Context Retention**: The AI remembers previous events and choices to maintain continuity.
- **VIT-Themed Stories**: Stories are set in VIT, incorporating campus culture, rules, and references.
