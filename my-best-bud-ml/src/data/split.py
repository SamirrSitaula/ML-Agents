"""
split.py
--------
Creates train/test CSV files.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os

CLEAN_FILE = "data/cleaned/sms_cleaned.csv"

def split_data():
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv(CLEAN_FILE)

    train, test = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

    train.to_csv("data/processed/train.csv", index=False)
    test.to_csv("data/processed/test.csv", index=False)

    print("Saved train/test to data/processed")

if __name__ == "__main__":
    split_data()
