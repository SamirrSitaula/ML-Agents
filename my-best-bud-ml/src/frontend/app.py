import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — Hybrid ML + AI Agent")

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/chat"  # use local URL for testing

# Initialize history
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

# Input box
msg = st.text_input("Type your message here:")

if st.button("Send") and msg:
    try:
        response = requests.post(BACKEND_URL, json={"message": msg})
        st.session_state.history.append((msg, response.json()))
        st.experimental_rerun()  # rerun safely
    except Exception as e:
        st.error(f"Error calling backend: {e}")
