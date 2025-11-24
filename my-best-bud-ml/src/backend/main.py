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

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # from src/ -> my-best-bud-ml
MODEL_PATH = os.path.join(BASE_DIR, "models/model.joblib")

# Load spam ML model
spam_model = joblib.load(MODEL_PATH)

# Load Hugging Face LLaMA-2 model
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise RuntimeError("HF_TOKEN not set in environment")

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token=HF_TOKEN
)
hf_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    device_map="auto",
    token=HF_TOKEN
)

# -------------------------------
# 2. Request schema
# -------------------------------
class ChatRequest(BaseModel):
    message: str

# -------------------------------
# 3. Helper functions
# -------------------------------
def check_spam(text: str):
    pred = spam_model.predict([text])[0]
    return pred

def generate_ai_reply(text: str, max_tokens: int = 50):
    inputs = tokenizer(text, return_tensors="pt")
    inputs = {k: v.to(hf_model.device) for k, v in inputs.items()}

    outputs = hf_model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.strip()

# -------------------------------
# 4. API endpoint
# -------------------------------
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    msg = request.message
    msg_lower = msg.lower()

    # --- 1. Spam check ---
    if msg_lower.startswith("check spam:"):
        text = msg[len("check spam:"):].strip()
        pred = check_spam(text)
        return {"intent": "spam_check", "ml_prediction": pred}

    # --- 2. ML learning mode ---
    if "learn ml" in msg_lower or "teach me ml" in msg_lower:
        reply = generate_ai_reply("Explain machine learning to a beginner in simple language.")
        return {"intent": "learn_ml", "ai_reply": reply}

    if "dataset" in msg_lower:
        reply = generate_ai_reply("Explain what datasets are in machine learning, with examples.")
        return {"intent": "learn_ml", "ai_reply": reply}

    # --- 3. Normal chat ---
    reply = generate_ai_reply(f"You are My Best Bud, a friendly agent. Respond helpfully. User said: {msg}")
    return {"intent": "chat", "ai_reply": reply}

# -------------------------------
# 5. Root endpoint
# -------------------------------
@app.get("/")
def root():
    return {"message": "My Best Bud Hybrid AI Agent is live!"}
