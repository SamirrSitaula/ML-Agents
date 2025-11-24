# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# -------------------------------
# 1. Setup
# -------------------------------
app = FastAPI(title="My Best Bud Hybrid AI Agent")

# Get path to project root (my-best-bud-ml)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # from src/ -> my-best-bud-ml
MODEL_PATH = os.path.join(BASE_DIR, "models/model.joblib")
# Load your trained ML spam model
spam_model = joblib.load(MODEL_PATH)

# Load Hugging Face LLaMA-2 7B (chat)
token = os.getenv("HF_TOKEN")  # grab your token from the environment

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token=token
)
hf_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    device_map="auto",  # automatically uses GPU if available
    use_auth_token=token
)

# -------------------------------
# 2. Request schema
# -------------------------------
class ChatRequest(BaseModel):
    message: str

# -------------------------------
# 3. Helper functions
# -------------------------------
def check_spam(message: str):
    """
    Use your ML model to predict spam.
    """
    pred = spam_model.predict([message])[0]
    return pred

def generate_ai_reply(message: str, max_tokens: int = 100):
    """
    Use LLaMA-2 to generate a response.
    """
    inputs = tokenizer(message, return_tensors="pt")
    inputs = {k: v.to(hf_model.device) for k, v in inputs.items()}

    outputs = hf_model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7,
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply

# -------------------------------
# 4. API endpoint
# -------------------------------
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    message = request.message

    # 1. ML spam detection
    spam_prediction = check_spam(message)

    # 2. AI response
    ai_reply = generate_ai_reply(message)

    # 3. Return both results
    return {
        "intent": "chat_hybrid",
        "ml_prediction": spam_prediction,
        "ai_reply": ai_reply
    }

# -------------------------------
# 5. Root endpoint (optional)
# -------------------------------
@app.get("/")
def root():
    return {"message": "My Best Bud Hybrid AI Agent is live!"}
#token export HF_TOKEN="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"