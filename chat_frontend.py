import streamlit as st

# Set page config for better mobile support
st.set_page_config(page_title="Chat App", layout="wide")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown("<h1 style='text-align: center;'>📱 Simple Chat</h1>", unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate bot response (You can replace this with AI logic)
    bot_response = f"🤖: You said '{user_input}'"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Refresh the page to update chat
    st.experimental_rerun()
