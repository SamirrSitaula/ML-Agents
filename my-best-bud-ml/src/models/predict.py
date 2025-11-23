"""
predict.py
----------
For backend agent to use model predictions.
"""

import joblib

MODEL_FILE = "models/model.joblib"
model = joblib.load(MODEL_FILE)

def predict_text(text: str):
    pred = model.predict([text])[0]
    prob = model.predict_proba([text])[0].tolist()
    return pred, prob
