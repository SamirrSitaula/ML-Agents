"""
evaluate.py
-----------
Checks model performance in detail.
"""

import pandas as pd
import joblib
from sklearn.metrics import classification_report

TEST_FILE = "data/processed/test.csv"
MODEL_FILE = "models/model.joblib"

def evaluate():
    df = pd.read_csv(TEST_FILE)
    model = joblib.load(MODEL_FILE)

    preds = model.predict(df["text"])

    print(classification_report(df["label"], preds))

if __name__ == "__main__":
    evaluate()
