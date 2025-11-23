import streamlit as st
import requests

st.title("My Best Bud — ML + Agent")

# Your deployed backend URL
BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize session state to store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Text area for user message
msg = st.text_area("Enter message")

# Button to send the message
if st.button("Send") and msg:
    try:
        # Call the backend once per message
        resp = requests.post(BACKEND_URL, json={"message": msg})
        # Append user message and backend reply to history
        st.session_state.history.append((msg, resp.json()))
    except Exception as e:
        st.error(f"Error calling backend: {e}")

# Display conversation history
for user_msg, reply in st.session_state.history:
    st.write(f"**You:** {user_msg}")
    st.json(reply)
