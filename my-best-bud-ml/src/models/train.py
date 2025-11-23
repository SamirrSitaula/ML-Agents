"""
train.py
--------
Trains ML model and saves model.joblib
"""

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from pipeline import create_pipeline
import os

TRAIN_FILE = "data/processed/train.csv"
TEST_FILE = "data/processed/test.csv"
MODEL_OUT = "models/model.joblib"

def train():
    os.makedirs("models", exist_ok=True)

    train = pd.read_csv(TRAIN_FILE)
    test = pd.read_csv(TEST_FILE)

    X_train = train["text"]
    y_train = train["label"]

    X_test = test["text"]
    y_test = test["label"]

    model = create_pipeline()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("Accuracy:", acc)

    joblib.dump(model, MODEL_OUT)
    print("Saved model to:", MODEL_OUT)

if __name__ == "__main__":
    train()
