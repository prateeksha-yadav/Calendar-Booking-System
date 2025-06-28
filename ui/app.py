import streamlit as st
import requests
import uuid
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Booking Assistant",
    page_icon="✨",
    layout="wide", # Use wide layout for sidebar
    initial_sidebar_state="expanded",
)

# --- Sidebar with Embedded Calendar ---
with st.sidebar:
    st.header("🗓️ Your Calendar")
    st.markdown(
        "Appointments you book with the assistant will appear here. "
    )
    user_email = "prateekshayadav01102004@gmail.com"
    calendar_url = f"https://calendar.google.com/calendar/embed?src={user_email.replace('@', '%40')}&ctz=UTC"
    st.components.v1.iframe(calendar_url, width=None, height=600, scrolling=True)
    
    if st.button("Start New Booking"):
        # Clear chat history and create a new session ID for a fresh start
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()


# --- Custom CSS for Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Hide the sidebar expand/collapse button */
    button[kind="header"] {
        display: none;
    }
    
    /* General Body Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117; /* GitHub Dark background */
        color: #c9d1d9;
    }
    
    /* Main container for chat */
    .main .block-container {
        padding: 2rem;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 0.75rem;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 1px solid #30363d;
        width: 90%;
        max-width: 800px;
    }

    /* Assistant message */
    .st-emotion-cache-1c7y2kd {
        background-color: #161b22;
    }
    
    /* User message */
    .st-emotion-cache-4oy321 {
        background: linear-gradient(135deg, #238636, #2ea043);
    }
    
    /* Avatar icons */
    .st-emotion-cache-1f1d6gn {
        border: 2px solid #238636;
        box-shadow: 0 0 12px rgba(46, 160, 67, 0.5);
    }

    /* User Input Area */
    .stTextInput>div>div>input {
        background-color: #0d1117;
        color: #c9d1d9;
        border-radius: 0.5rem;
        border: 1px solid #30363d;
        padding: 0.8rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid #2ea043;
        box-shadow: 0 0 8px rgba(46, 160, 67, 0.4);
    }

    /* Page Title */
    h1 {
        font-weight: 700;
        color: #c9d1d9;
        text-align: center;
    }
    
    /* Subheader */
    .stMarkdown p {
        text-align: center;
        color: #8b949e;
    }

</style>
""", unsafe_allow_html=True)


# --- Main Chat Interface ---
st.title("📅 AI Booking Assistant 🤖")
st.markdown("I can help you find and book appointments. Try asking: 'Do you have any availability tomorrow?'")

# --- Session State Initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# --- User Input & Agent Interaction ---
if prompt := st.chat_input("What would you like to do?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/chat")
                response = requests.post(
                    backend_url, 
                    json={"message": prompt, "session_id": st.session_state.session_id}
                )
                response.raise_for_status()
                full_response = response.json().get("response", "I'm sorry, I encountered an issue.")
            except requests.exceptions.RequestException as e:
                full_response = f"Error: Could not connect to the backend. Is it running? {e}"
        
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Rerun to update the calendar if a booking was made
    if "Success!" in full_response:
        st.rerun() 