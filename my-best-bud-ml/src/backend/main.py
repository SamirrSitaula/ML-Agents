# from fastapi import FastAPI
# from pydantic import BaseModel
# from src.agent.logic import agent_response

# app = FastAPI()

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   # Allow any domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class Message(BaseModel):
#     message: str

# @app.post("/chat")
# def chat(req: Message):
#     return agent_response(req.message)
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load your ML model (already trained)
model = joblib.load("models/spam_classifier.pkl")

app = FastAPI()

class Message(BaseModel):
    message: str

# Simple keyword-based intent detection
def detect_intent(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["spam", "check", "ham"]):
        return "spam_check"
    elif any(word in text_lower for word in ["ml", "machine learning", "ai", "learn"]):
        return "learn_ml"
    elif any(word in text_lower for word in ["hi", "hello", "how are you"]):
        return "small_talk"
    else:
        return "general"

@app.post("/chat")
def chat(msg: Message):
    intent = detect_intent(msg.message)
    
    if intent == "spam_check":
        prediction = model.predict([msg.message])[0]
        probabilities = model.predict_proba([msg.message])[0]
        return {
            "intent": intent,
            "ml_prediction": prediction,
            "probabilities": {"ham": float(probabilities[0]), "spam": float(probabilities[1])}
        }
    
    elif intent == "learn_ml":
        reply = "I can help you learn ML! Ask me about datasets, models, or deployment."
    elif intent == "small_talk":
        reply = "Hey! I am your Best Bud agent. How can I help you today?"
    else:  # general
        reply = "I am your Best Bud agent. Ask me to check spam, learn ML, or help with AI!"
    
    return {"intent": intent, "reply": reply}
