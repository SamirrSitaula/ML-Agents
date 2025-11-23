import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")
st.title("My Best Bud — ML + Agent")

BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history from top to bottom
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:  # spam_check response
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")
st.markdown("---")

# Form for user input (sticks to bottom)
with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_input("Type your message here:")
    submit = st.form_submit_button("Send")

    if submit and msg:
        try:
            resp = requests.post(BACKEND_URL, json={"message": msg})
            st.session_state.history.append((msg, resp.json()))
            # Streamlit automatically reruns and keeps new message visible
        except Exception as e:
            st.error(f"Error calling backend: {e}")

# Auto-scroll to bottom using a little trick
st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)
st.markdown("<script>document.getElementById('bottom').scrollIntoView();</script>", unsafe_allow_html=True)
