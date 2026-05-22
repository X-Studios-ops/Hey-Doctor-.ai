import streamlit as st
import google.genai as genai

# ==============================================================================
# 1. PAGE CONFIGURATION & PREMIUM DARK GREEN THEME
# ==============================================================================
st.set_page_config(page_title="Heydoctor.ai | Premium AI Concierge", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp {
        background: linear-gradient(135deg, #0B1511 0%, #040806 100%);
        color: #E2E8F0;
    }
    
    /* Header Custom Styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* Premium Badge */
    .premium-badge {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 25px;
    }
    
    /* Chat Container Tweaks */
    .stChatMessage {
        background-color: rgba(20, 35, 30, 0.4) !important;
        border: 1px solid rgba(16, 185, 129, 0.15) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }
    
    /* Make Input box look sleek */
    div[data-testid="stChatInput"] {
        border-radius: 10px !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: #10B981 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top UI Branding
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge">✨ Multi-Engine Enterprise Mode: Active</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY ROTATOR LOGIC (ANTI-EXHAUST SYSTEM)
# ==============================================================================
# Streamlit Secrets se saari keys uthana safely
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

# Agar koi key na mile toh default fallback lagana
if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# ==============================================================================
# 3. CORE AI ENGINE INITIALIZATION WITH MEMORY LOCK
# ==============================================================================
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, "
    "and wellness advisor. Provide highly accurate, professional, and empathetic medical insights. "
    "Always maintain your specialist persona and end with a friendly disclaimer that you are an AI."
)

def initialize_chat_session():
    """Client aur Chat Session ko state mein save rakhne ka function taaki crash na ho"""
    if not KEYS_POOL:
        st.error("🚨 API Key missing! Please configure Streamlit Secrets.")
        return False
    
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    active_key = KEYS_POOL[idx]
    
    try:
        # Har baar naya client nahi banega agar pehle se state mein hai
        if "ai_client" not in st.session_state:
            st.session_state.ai_client = genai.Client(api_key=active_key)
            
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = st.session_state.ai_client.chats.create(
                model="gemini-2.5-flash",
                config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
            )
        return True
    except Exception as e:
        # Agar current key fail ho jaye, toh automatic agli key par switch karo
        st.session_state.current_key_index += 1
        if "ai_client" in st.session_state: del st.session_state.ai_client
        if "chat_session" not in st.session_state:
            return initialize_chat_session()
        return False

# Setup connection
engine_ready = initialize_chat_session()

# ==============================================================================
# 4. CHAT HISTORY RENDERER (PERSISTENT LOOK)
# ==============================================================================
# Initialize message log for UI rendering
if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

# Pehle se maujood UI messages ko screen par print karna
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 5. LIVE REACTION HANDLER (USER ENTRY)
# ==============================================================================
if user_query := st.chat_input("Enter physical symptoms, medication queries...", key="heydoctor_input_field"):
    # Screen par user ka message dikhana
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    if engine_ready and "chat_session" in st.session_state:
        with st.chat_message("assistant"):
            try:
                # Actual AI prediction request
                response = st.session_state.chat_session.send_message(user_query)
                st.markdown(response.text)
                st.session_state.messages_display.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Agar message bhejte waqt Quota Exhausted (429) ya koi dikkat aaye
                if "429" in str(e) or "EXHAUSTED" in str(e).upper():
                    st.session_state.current_key_index += 1 # Index badhao
                    # Purana system delete karo taaki agle refresh pe fresh start ho
                    if "ai_client" in st.session_state: del st.session_state.ai_client
                    if "chat_session" in st.session_state: del st.session_state.chat_session
                    st.warning("⚠️ Engine route optimized due to high load. Please click enter again to resend message safely!")
                else:
                    st.error(f"Medical Engine Interrupted: {e}")
