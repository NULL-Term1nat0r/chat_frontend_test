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

# Add custom CSS and JavaScript to handle scroll and button positioning
st.markdown("""
    <style>
        /* Position the button on the top left */
        #open-sidebar-btn {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 10;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            border: none;
        }

        /* Hide the button when scrolling */
        #open-sidebar-btn.hidden {
            display: none;
        }

        .chat-container {
            margin-top: 50px; /* Make room for the button */
        }
    </style>
    <script>
        // Hide the button when scrolling
        const btn = document.getElementById("open-sidebar-btn");
        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {  // Hide after 50px scroll
                btn.classList.add("hidden");
            } else {
                btn.classList.remove("hidden");
            }
        });
    </script>
""", unsafe_allow_html=True)

# Button to open the sidebar for previous conversations
st.markdown('<button id="open-sidebar-btn">View Previous Conversations</button>', unsafe_allow_html=True)

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
