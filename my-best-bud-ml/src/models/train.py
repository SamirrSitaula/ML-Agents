from fastapi import FastAPI
import joblib
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

# Load your ML spam model
spam_model = joblib.load("/Users/samirsitaula/Documents/Data-ML-Agents/my-best-bud-ml/models/model.joblib")

# Load Hugging Face LLaMA-2
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
hf_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

@app.post("/chat")
def chat_endpoint(message: str):
    # 1. Check spam
    ml_pred = spam_model.predict([message])[0]

    # 2. Generate AI response (simplified)
    inputs = tokenizer(message, return_tensors="pt")
    outputs = hf_model.generate(**inputs, max_new_tokens=50)
    hf_reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "ml_prediction": ml_pred,
        "ai_reply": hf_reply
    }
