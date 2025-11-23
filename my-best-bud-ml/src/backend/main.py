from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.logic import agent_response

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow any domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(req: Message):
    return agent_response(req.message)
