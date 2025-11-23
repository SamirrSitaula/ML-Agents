import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")

st.markdown("---")

# Use a form for message input
with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_input("Type your message here:")
    submit = st.form_submit_button("Send")

    if submit and msg:
        try:
            resp = requests.post(BACKEND_URL, json={"message": msg})
            st.session_state.history.append((msg, resp.json()))
            # No need for st.experimental_rerun()
        except Exception as e:
            st.error(f"Error calling backend: {e}")
