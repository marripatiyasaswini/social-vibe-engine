# Running the social-vibe-engine
Details : 
Its a plug-and-play microservice that: 

• Detects inactive, low-interaction buddies and suggests nudges

• Generates anonymous compliments or appreciation tokens based on peer activity (karma, answers, profile improvements)

 • Personalizes nudges and compliments using a scoring logic + templates

 • Is fully offline, configurable, FastAPI-based, and Dockerized


## Installation

```bash

git clone https://github.com/marripatiyasaswini/social-vibe-engine.git

uvicorn app.main:app --reload

```
## OR USE DOCKER(easier way)

```bash

docker pull chinmayeeyasaswinim/socialvibeengine:latest

docker run -d --name socialvibeengine_container -p 8000:8000 chinmayeeyasaswinim/socialvibeengine:latest

```
and then check http://localhost:8000/docs for all methods
## License

[MIT](https://choosealicense.com/licenses/mit/)
