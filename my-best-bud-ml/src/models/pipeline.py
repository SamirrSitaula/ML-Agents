"""
pipeline.py
-----------
Defines ML pipeline: TF-IDF + Logistic Regression
"""

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def create_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("model", LogisticRegression(max_iter=300))
    ])
