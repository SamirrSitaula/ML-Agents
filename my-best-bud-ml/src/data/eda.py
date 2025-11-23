"""
eda.py
------
Performs basic EDA on cleaned data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CLEAN_FILE = "data/cleaned/sms_cleaned.csv"

def run_eda():
    df = pd.read_csv(CLEAN_FILE)

    print(df.head())
    print(df["label"].value_counts())

    df["length"] = df["text"].str.len()
    print(df["length"].describe())

    # Plot distribution
    sns.histplot(df["length"], bins=50)
    plt.title("Message Length Distribution")
    plt.show()

if __name__ == "__main__":
    run_eda()
