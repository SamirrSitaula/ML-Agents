import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:  # spam_check response
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")

st.markdown("---")

# Use a form with a key for consistent input
with st.form(key="chat_form"):
    msg = st.text_input("Type your message here:")
    submit = st.form_submit_button("Send")

if submit and msg:
    try:
        resp = requests.post(BACKEND_URL, json={"message": msg})
        st.session_state.history.append((msg, resp.json()))
        # Force the page to rerun immediately
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error calling backend: {e}")
