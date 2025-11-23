"""
clean.py
--------
Converts raw tab-separated SMS data to a clean CSV file.
"""

import os
import csv
import pandas as pd

RAW_FILE = "raw/SMSSpamCollection"
CLEAN_PATH = "cleaned/sms_cleaned.csv"

def clean_data():
    os.makedirs("data/cleaned", exist_ok=True)

    cleaned_rows = []

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            label, text = line.split("\t")
            cleaned_rows.append([label, text.strip()])

    df = pd.DataFrame(cleaned_rows, columns=["label", "text"])
    df.to_csv(CLEAN_PATH, index=False)

    print("Cleaned dataset saved to:", CLEAN_PATH)

if __name__ == "__main__":
    clean_data()
