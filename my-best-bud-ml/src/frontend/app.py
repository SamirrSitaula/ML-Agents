import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Text input with session state
if "current_msg" not in st.session_state:
    st.session_state.current_msg = ""

def send_message():
    msg = st.session_state.current_msg.strip()
    if msg:
        try:
            resp = requests.post(BACKEND_URL, json={"message": msg})
            st.session_state.history.append((msg, resp.json()))
            st.session_state.current_msg = ""  # clear input
        except Exception as e:
            st.error(f"Error calling backend: {e}")

# Input box with on_change callback
st.text_input("Type your message here:", key="current_msg", on_change=send_message)

# Display conversation
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")
