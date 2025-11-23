import streamlit as st
import requests

st.title("My Best Bud — ML + Agent")

msg = st.text_area("Enter message")

if st.button("Send"):
    # resp = requests.post("http://localhost:8000/chat", json={"message": msg}) #for local
    BACKEND_URL = "https://ml-agents.onrender.com/chat" #updated url for render
    resp = requests.post(BACKEND_URL, json={"message": msg})

    st.json(resp.json())

