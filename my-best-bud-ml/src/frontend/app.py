# import streamlit as st
# import requests

# st.title("My Best Bud — ML + Agent")

# # Your deployed backend URL
# BACKEND_URL = "https://ml-agents.onrender.com/chat"

# # Initialize session state to store conversation history
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Text area for user message
# msg = st.text_area("Enter message")

# # Button to send the message
# if st.button("Send") and msg:
#     try:
#         # Call the backend once per message
#         resp = requests.post(BACKEND_URL, json={"message": msg})
#         # Append user message and backend reply to history
#         st.session_state.history.append((msg, resp.json()))
#     except Exception as e:
#         st.error(f"Error calling backend: {e}")

# # Display conversation history
# for user_msg, reply in st.session_state.history:
#     st.write(f"**You:** {user_msg}")
#     st.json(reply)
import streamlit as st
import requests

st.set_page_config(page_title="My Best Bud Agent", layout="wide")

st.title("My Best Bud — ML + Agent")

# Your deployed backend URL
BACKEND_URL = "https://ml-agents.onrender.com/chat"

# Initialize session state to store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history first (so latest messages are visible)
for user_msg, reply in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    if "ml_prediction" in reply:  # spam_check response
        st.json(reply)
    else:
        st.markdown(f"**Agent:** {reply['reply']}")

# Add a horizontal line for separation
st.markdown("---")

# Text input at the bottom
msg = st.text_area("Type your message here:", height=50)


#depreciated 
# if st.button("Send") and msg:
#     try:
#         resp = requests.post(BACKEND_URL, json={"message": msg})
#         st.session_state.history.append((msg, resp.json()))
#         st.experimental_rerun()  # rerun script so input stays at bottom
#     except Exception as e:
#         st.error(f"Error calling backend: {e}")
