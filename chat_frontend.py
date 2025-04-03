import streamlit as st

# Set page config for better mobile display
st.set_page_config(page_title="Chat App", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown("<h1 style='text-align: center;'>Simple Chat</h1>", unsafe_allow_html=True)

# Display chat messages without labels (like ChatGPT)
for msg in st.session_state.messages:
    st.markdown(f"<div style='padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #f1f1f1;'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type a message...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate bot response (Replace this with real AI response if needed)
    bot_response = f"You said '{user_input}'"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display the new messages without forcing a rerun
    st.rerun()
