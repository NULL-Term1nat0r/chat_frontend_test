import streamlit as st
from datetime import datetime
import json

# Set page configuration
st.set_page_config(
    page_title="Chat App",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    /* Main chat container */
    .main .block-container {
        padding-bottom: 5rem;
    }
    
    /* Input container at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        z-index: 100;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        width: 300px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        max-width: 80%;
    }
    
    .user-message .stChatMessage {
        margin-left: auto;
        margin-right: 0;
    }
    
    .bot-message .stChatMessage {
        margin-right: auto;
        margin-left: 0;
        background-color: #e6f7ff;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .sidebar .sidebar-content {
            width: 100%;
        }
    }
    
    /* History item styling */
    .history-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .history-item:hover {
        background-color: #f0f0f0;
    }
    
    .history-item.active {
        background-color: #e0f7fa;
    }
    
    /* Menu button styling */
    .menu-button {
        position: absolute;
        top: 1rem;
        left: 1rem;
        z-index: 101;
        background: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []
    
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = []
    
if 'sidebar_open' not in st.session_state:
    st.session_state['sidebar_open'] = False
    
if 'new_chat_id' not in st.session_state:
    st.session_state['new_chat_id'] = 0

# Function to save chat history
def save_chat_history():
    if st.session_state['current_chat']:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        chat_title = f"Chat {len(st.session_state['history']) + 1} - {timestamp}"
        st.session_state['history'].insert(0, {
            'id': st.session_state['new_chat_id'],
            'title': chat_title,
            'messages': st.session_state['current_chat'].copy()
        })
        st.session_state['new_chat_id'] += 1
        st.session_state['current_chat'] = []

# Function to load a chat from history
def load_chat(chat_id):
    for chat in st.session_state['history']:
        if chat['id'] == chat_id:
            st.session_state['current_chat'] = chat['messages'].copy()
            break

# Function to start a new chat
def new_chat():
    save_chat_history()
    st.session_state['current_chat'] = []

# Toggle sidebar
def toggle_sidebar():
    st.session_state['sidebar_open'] = not st.session_state['sidebar_open']

# Main app layout
def main():
    # Menu button to toggle sidebar
    st.markdown("""
    <button class="menu-button" onclick="parent.document.querySelector('.sidebar .sidebar-content').style.display = 'block';">
        ☰
    </button>
    """, unsafe_allow_html=True)
    
    # Sidebar with chat history
    with st.sidebar:
        st.title("Chat History")
        
        # Button to start new chat
        if st.button("➕ New Chat", use_container_width=True):
            new_chat()
            st.session_state['sidebar_open'] = False
            st.rerun()
        
        # Display chat history
        st.write("---")
        for chat in st.session_state['history']:
            is_active = any(msg['id'] == chat['id'] for msg in st.session_state['current_chat']) if st.session_state['current_chat'] else False
            item_class = "history-item active" if is_active else "history-item"
            st.markdown(f"""
            <div class="{item_class}" onclick="loadChat({chat['id']})">
                {chat['title']}
            </div>
            """, unsafe_allow_html=True)
    
    # Hide sidebar initially if not open
    if not st.session_state['sidebar_open']:
        st.markdown("""
        <style>
            .sidebar .sidebar-content {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Main chat area
    st.title("Chat")
    
    # Display current chat messages
    for msg in st.session_state['current_chat']:
        if msg['is_user']:
            with st.container():
                st.markdown('<div class="user-message">', unsafe_allow_html=True)
                st.chat_message("user").write(msg['content'])
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown('<div class="bot-message">', unsafe_allow_html=True)
                st.chat_message("assistant").write(msg['content'])
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area at bottom
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        user_input = st.chat_input("Type your message here...", key="input")
        
        if user_input:
            # Add user message to current chat
            user_msg_id = len(st.session_state['current_chat'])
            st.session_state['current_chat'].append({
                'id': user_msg_id,
                'content': user_input,
                'is_user': True,
                'timestamp': datetime.now().isoformat()
            })
            
            # Simulate bot response
            bot_response = f"I received your message: '{user_input}'"
            st.session_state['current_chat'].append({
                'id': user_msg_id + 1,
                'content': bot_response,
                'is_user': False,
                'timestamp': datetime.now().isoformat()
            })
            
            # Rerun to update the display
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript to handle chat loading
    st.markdown("""
    <script>
        function loadChat(chatId) {
            const data = {chat_id: chatId};
            fetch('/_stcore/handle_loaded_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                }
            });
        }
        
        // Close sidebar when clicking outside
        document.addEventListener('click', function(event) {
            const sidebar = parent.document.querySelector('.sidebar .sidebar-content');
            const menuButton = parent.document.querySelector('.menu-button');
            
            if (sidebar.style.display === 'block' && 
                !sidebar.contains(event.target) && 
                !menuButton.contains(event.target)) {
                sidebar.style.display = 'none';
            }
        });
    </script>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
