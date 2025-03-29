# CC interhack backend
- backend for interhack
## TODO:
- [x] Setup basic script
- [x] find a functioning AI model
- [x] Implement the AI model
- [x] Improve system prompt
- [x] Get the model to hold context
- [x] Generate better stories

- [x] Add VIT guidelines
- [ ] Improve VIT guidelines

- [ ] Implement multiplayer


## 📡 API Endpoints

| Method  | Endpoint     | Request Format |
|---------|-------------|---------------|
| **POST** | `/generate`  | `{ "name": "<string>", "user_input": "<string>" }` |
| **POST** | `/continue`  | `{ "previous_story": "<string>", "user_choice": "<string>" }` |

