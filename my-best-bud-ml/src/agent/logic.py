"""
logic.py
--------
Very simple agent logic combining:
- intent detection
- ML classifier calls
"""

from src.models.predict import predict_text

def detect_intent(message: str):
    msg = message.lower()

    if "spam" in msg:
        return "spam_check"
    if "learn" in msg:
        return "learning"
    return "general"

def agent_response(message: str):
    intent = detect_intent(message)

    if intent == "spam_check":
        pred, prob = predict_text(message)
        
        # prob is a list like: [prob_ham, prob_spam]
        return {
            "intent": intent,
            "ml_prediction": pred,
            "probabilities": {
                "ham": prob[0],
                "spam": prob[1]
            }
        }

    return {
        "intent": intent,
        "reply": "I am your Best Bud agent. Ask me to check spam, learn ML, or help with AI!"
    }