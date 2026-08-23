import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Healthcare AI Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and dark glassmorphism theme
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #091e3a 50%, #1e293b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Container */
    .header-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1deg solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .header-title {
        background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    /* Disclaimer Card */
    .disclaimer-card {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 20px;
        color: #fbbf24;
        font-size: 0.9rem;
    }

    /* Chat Messages */
    .stChatMessage[data-testimonial="user"] {
        background: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
    }

    .stChatMessage[data-testimonial="assistant"] {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(52, 211, 153, 0.2) !important;
        border-radius: 12px !important;
    }

    /* Quick Prompt Pills */
    div.stButton > button {
        background: rgba(30, 41, 59, 0.8);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        transition: all 0.3s ease;
        width: 100%;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #0284c7 0%, #059669 100%);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# System instruction definition
SYSTEM_INSTRUCTION = """
You are HealthcareAI, an empathetic, highly knowledgeable healthcare information assistant.

Guidelines:
1. Provide accurate, structured, and easy-to-read medical & wellness information.
2. ALWAYS include a brief safety disclaimer emphasizing that your responses are for educational/informational purposes only and not medical advice.
3. If severe symptoms are described (e.g. intense chest pain, breathing difficulty, severe bleeding, stroke symptoms), advise calling emergency services (911/112) IMMEDIATELY.
4. Use markdown lists, headings, and bold text for readability.
"""

def init_gemini(api_key):
    """Configures the Gemini API client and model."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={"temperature": 0.7, "max_output_tokens": 8192},
        system_instruction=SYSTEM_INSTRUCTION
    )

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/hospital.png", width=70)
    st.title("Settings & Help")

    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get your key from Google AI Studio (aistudio.google.com)"
    )

    st.markdown("---")
    st.subheader("🚨 Emergency Numbers")
    st.markdown("""
    - **US / Canada**: `911`
    - **Europe / UK**: `112` / `999`
    - **India**: `102` / `108`
    - **Poison Control**: `1-800-222-1222`
    """)

    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

# Main Header
st.markdown("""
<div class="header-box">
    <h1 class="header-title">🩺 Healthcare AI Assistant</h1>
    <p style="color: #94a3b8; margin-top: 6px;">Your 24/7 AI guide for medical info, wellness tips, and symptom guidance.</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer Notice
st.markdown("""
<div class="disclaimer-card">
    ⚠️ <strong>Medical Disclaimer:</strong> This chatbot provides general educational information only. It is NOT a substitute for professional medical advice, diagnosis, or emergency treatment.
</div>
""", unsafe_allow_html=True)

# Check API Key availability
if not api_key_input:
    st.warning("👈 Please enter your **Gemini API Key** in the sidebar to start chatting.")
    st.stop()

# Initialize Chat Model Session
try:
    model = init_gemini(api_key_input)
    if "chat" not in st.session_state or st.session_state.chat is None:
        st.session_state.chat = model.start_chat(history=[])
    if "messages" not in st.session_state:
        st.session_state.messages = []
except Exception as e:
    st.error(f"Failed to initialize Gemini API: {e}")
    st.stop()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick Prompt Suggestions
st.markdown("##### 💡 Quick Questions:")
col1, col2, col3, col4 = st.columns(4)

prompt_input = None
if col1.button("🍎 Healthy Diet Tips"):
    prompt_input = "What are key components of a balanced, heart-healthy diet?"
if col2.button("😴 Tips for Better Sleep"):
    prompt_input = "What are scientific tips to improve sleep hygiene and fall asleep faster?"
if col3.button("🩺 Cold vs Flu Symptoms"):
    prompt_input = "How can I tell the difference between a common cold and the flu?"
if col4.button("💊 Medication Storage"):
    prompt_input = "What are general safety rules for storing household medications properly?"

# Chat Input Box
user_prompt = st.chat_input("Ask a health or wellness question...")
if user_prompt:
    prompt_input = user_prompt

if prompt_input:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    # Generate Bot Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt_input)
                bot_response = response.text
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as err:
                st.error(f"An error occurred: {err}")
