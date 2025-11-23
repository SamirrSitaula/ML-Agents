from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.logic import agent_response

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(req: Message):
    return agent_response(req.message)
