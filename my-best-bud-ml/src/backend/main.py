
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os


# 1. App setup

app = FastAPI(title="My Best Bud Hybrid AI Agent")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/model.joblib")


# 2. Load ML spam model

spam_model = joblib.load(MODEL_PATH)


# 3. Load HF model ONCE

MODEL_NAME = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
hf_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Device (Mac optimized)
device = "mps" if torch.backends.mps.is_available() else "cpu"
hf_model = hf_model.to(device)
hf_model.eval()


# 4. Request schema

class ChatRequest(BaseModel):
    message: str


# 5. Helper functions

def check_spam(text: str):
    return spam_model.predict([text])[0]

def generate_ai_reply(text: str, max_tokens: int = 50):
    inputs = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = hf_model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    # Remove prompt from output
    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    reply = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    return reply.strip()


# 6. API endpoint

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    msg = request.message
    msg_lower = msg.lower()

    # --- Spam check ---
    if msg_lower.startswith("check spam:"):
        text = msg[len("check spam:"):].strip()
        pred = check_spam(text)
        return {"intent": "spam_check", "ml_prediction": pred}

    # --- Learning mode ---
    if "learn ml" in msg_lower or "teach me ml" in msg_lower:
        reply = generate_ai_reply(
            "Explain machine learning to a beginner in simple language."
        )
        return {"intent": "learn_ml", "ai_reply": reply}

    if "dataset" in msg_lower:
        reply = generate_ai_reply(
            "Explain what datasets are in machine learning, with examples."
        )
        return {"intent": "learn_ml", "ai_reply": reply}

    # --- Normal chat ---
    reply = generate_ai_reply(
        f"You are My Best Bud, a friendly agent. Respond helpfully. User said: {msg}"
    )
    reply = reply.strip()
    if not reply:
        reply = "Sorry, I didn't understand that. Can you rephrase?"

    return {"intent": "chat", "ai_reply": reply}


# 7. Health check

@app.get("/")
def root():
    return {"status": "My Best Bud backend is running"}
