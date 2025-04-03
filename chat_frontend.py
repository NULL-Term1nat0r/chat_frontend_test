import streamlit as st

# Set page config for better mobile display
st.set_page_config(page_title="Chat App", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize previous conversations (you can replace this with a persistent storage mechanism)
if "conversations" not in st.session_state:
    st.session_state.conversations = []

# Title
st.markdown("<h1 style='text-align: center;'>Simple Chat</h1>", unsafe_allow_html=True)

# Button to open the sidebar for previous conversations
if st.button('View Previous Conversations'):
    # Expand the sidebar (it will automatically appear on mobile when using Streamlit's sidebar)
    with st.sidebar:
        st.header("Previous Conversations")
        # Display previous conversations with clickable links
        for i, conversation in enumerate(st.session_state.conversations):
            if st.button(f"Conversation {i+1}"):
                # Display the selected conversation
                st.session_state.messages = conversation
                st.experimental_rerun()

# Display chat messages with different alignments for user and bot
for msg in st.session_state.messages:
    if msg["role"] == "user":
        # Align user messages to the right
        st.markdown(f"<div style='display: flex; justify-content: flex-end; padding: 10px; margin-bottom: 10px;'>"
                    f"<div style='background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 70%; color: black;'>{msg['content']}</div>"
                    "</div>", unsafe_allow_html=True)
    else:
        # Align assistant messages to the left
        st.markdown(f"<div style='display: flex; justify-content: flex-start; padding: 10px; margin-bottom: 10px;'>"
                    f"<div style='background-color: #E4E6EB; padding: 10px; border-radius: 10px; max-width: 70%; color: black;'>{msg['content']}</div>"
                    "</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type a message...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate bot response (Replace this with real AI response if needed)
    bot_response = f"You said '{user_input}'"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Save the current conversation to history
    st.session_state.conversations.append(st.session_state.messages.copy())

    # Display the new messages without forcing a rerun
    st.rerun()
