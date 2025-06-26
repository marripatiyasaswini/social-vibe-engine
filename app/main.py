from fastapi import FastAPI
from fastapi import APIRouter
from .schemas.user import UserData
from pathlib import Path
from .compliment_generator import generate_compliment
from .nudge_engine import generate_buddy_nudges

app = FastAPI()
router_v1 = APIRouter()
#inorder to differentiate between the various versions of the router api

@router_v1.get("/health")
def health():
   return { "message" : "status: ok" }


@router_v1.get("/version")
def v():
   return { "message" : "model_version: 1.0.0" }

#to interact with inactive buddies
@router_v1.post("/generate-social-nudges")
def generate_social_nudges(data:UserData):
    nudges = generate_buddy_nudges(data.dict())
    compliment = generate_compliment(data.dict())
    
    return {
        "user_id": data.user_id,
        "buddy_nudges": nudges,
        "compliment": compliment,
        "status": "generated"
    }
   
app.include_router(router_v1)


