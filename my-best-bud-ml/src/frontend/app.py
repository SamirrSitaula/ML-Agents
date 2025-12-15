

import streamlit as st
import requests


# Page setup

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("🤖 My Best Bud — Hybrid ML + AI Agent")

# BACKEND_URL = "http://127.0.0.1:8001/chat"
BACKEND_URL = "https://my-best-bud.onrender.com"


# Session state

if "history" not in st.session_state:
    st.session_state.history = []


# Display chat history

for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")

    if reply["intent"] == "spam_check":
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply.get('ai_reply', 'No response')}")

st.markdown("---")


# Input

msg = st.text_input("Type your message:")

if st.button("Send") and msg:
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": msg},
            timeout=120
        )
        response.raise_for_status()
        st.session_state.history.append((msg, response.json()))
        st.rerun()

    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")
