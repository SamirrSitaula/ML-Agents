import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []
if "current_msg" not in st.session_state:
    st.session_state.current_msg = ""
if "send_flag" not in st.session_state:
    st.session_state.send_flag = False

# Display conversation history
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")
st.markdown("---")

# Text input
st.session_state.current_msg = st.text_input("Type your message here:", st.session_state.current_msg, key="input_box")

# Detect send
if st.button("Send"):
    if st.session_state.current_msg.strip():
        st.session_state.send_flag = True

# Call backend only once per send
if st.session_state.send_flag:
    try:
        resp = requests.post(BACKEND_URL, json={"message": st.session_state.current_msg})
        st.session_state.history.append((st.session_state.current_msg, resp.json()))
    except Exception as e:
        st.error(f"Error calling backend: {e}")
    # Reset input and flag
    st.session_state.current_msg = ""
    st.session_state.send_flag = False
    st.experimental_rerun()
