import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "input_msg" not in st.session_state:
    st.session_state.input_msg = ""  # preserve text area content

# Display conversation history
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")

st.markdown("---")

# Text area bound to session state
st.session_state.input_msg = st.text_area("Type your message here:", height=50, value=st.session_state.input_msg)

# Send button
if st.button("Send") and st.session_state.input_msg.strip():
    try:
        resp = requests.post(BACKEND_URL, json={"message": st.session_state.input_msg})
        st.session_state.history.append((st.session_state.input_msg, resp.json()))
        st.session_state.input_msg = ""  # clear text area after sending
        # No rerun needed; Streamlit auto-reruns
    except Exception as e:
        st.error(f"Error calling backend: {e}")
