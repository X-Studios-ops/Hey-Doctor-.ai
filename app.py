import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE CONFIGURATION & PREMIUM BLACK MAGIC THEME (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Concierge",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for the full Premium Design, Hacker Typing, and Medical Scanner
st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp {
        background: linear-gradient(135deg, #0B1511 0%, #040806 100%);
        color: #E2E8F0;
    }
    
    /* Header Custom Styling (As seen in image_3.png) */
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: 5px;
        text-shadow: 0px 4px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Premium Badge (Active Status) */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 30px;
    }
    .premium-badge {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0px 4px 15px rgba(16, 185, 129, 0.2);
        letter-spacing: 0.5px;
    }
    
    /* Input field styling (Responsive, Sleek) */
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(20, 35, 30, 0.5) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        color: #E2E8F0 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* 🦾 MEDICAL SCANNER LOADING ANIMATION (Premium Feature) */
    @keyframes scan-animation {
        0% { transform: translateY(-100%) translateX(-100%); opacity: 0; }
        20% { opacity: 0.8; }
        100% { transform: translateY(100%) translateX(100%); opacity: 0; }
    }
    .medical-scanner {
        position: relative;
        width: 100%;
        height: 200px;
        background: rgba(16, 185, 129, 0.03);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .medical-scanner::after {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 200%; height: 200%;
        background: linear-gradient(135deg, rgba(16,185,129,0) 0%, rgba(16,185,129,0.3) 50%, rgba(16,185,129,0) 100%);
        animation: scan-animation 2s linear infinite;
    }
    .scanner-text {
        position: absolute;
        bottom: 10px; left: 15px;
        color: #10B981;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Hacker Styling for AI Response Container */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace; /* Classic hacker look */
        line-height: 1.6;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Top UI Branding and Badge (image_3.png compliant)
# ------------------------------------------------------------------------------
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">✨ Multi-Engine Enterprise Mode: Active</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY ROTATOR LOGIC (ANTI-EXHAUST SYSTEM)
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

# Fallback case (if only old key exists)
if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# ==============================================================================
# 3. CHAT INITIALIZATION & UI MESSAGES
# ==============================================================================
# System instructions to lock AI persona (God Mode)
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, "
    "and wellness advisor. Provide highly accurate, professional, and empathetic medical insights. "
    "Always maintain your specialist persona and end with a friendly disclaimer that you are an AI."
)

# Initialize messages display and chat session in state
if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "chat_session" not in st.session_state:
    if not KEYS_POOL:
        st.error("🚨 API Key missing! Please configure Streamlit Secrets (A, B, C).")
        st.stop()
        
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    try:
        active_key = KEYS_POOL[idx]
        ai_client = genai.Client(api_key=active_key)
        st.session_state.chat_session = ai_client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
        )
    except Exception as e:
        st.error(f"Engine connection failed: {e}")
        st.stop()

# ------------------------------------------------------------------------------
# Chat History Renderer (Normal for old messages)
# ------------------------------------------------------------------------------
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        # Use normal display for history to avoid slow rendering
        st.markdown(msg["content"])

# ==============================================================================
# 4. LIVE INPUT HANDLER (Premium UI + Hacker Typewriter)
# ==============================================================================
if user_query := st.chat_input("Enter physical symptoms, medication queries...", key="heydoctor_chat_input"):
    
    # 1. Show user message instantly
    with st.chat_message("user"):
        st.markdown(user_query)
    # Persist message
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    # 2. Start AI Response Flow
    with st.chat_message("assistant"):
        # 🦾 MEDICAL SCANNER LOADING (UI Element)
        scanner_placeholder = st.empty()
        scanner_placeholder.markdown("""
            <div class="medical-scanner">
                <div class="scanner-text">
                    SYSTEM::INITIALIZING...<br>
                    SCANNING BIOMARKERS...<br>
                    QUERYING MEDICAL DATABASE...
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Hacker-style response container (Empty initially)
        response_placeholder = st.empty()
        
        try:
            # 🔄 AI Prediction Request (This is the long process)
            response = st.session_state.chat_session.send_message(user_query)
            # Medical scan over, hide the animation
            scanner_placeholder.empty()
            
            # --- 🦾 HACKER-STYLE TYPEWRITER EFFECT ---
            full_response = response.text
            typed_response = ""
            # Loop through characters and print them one by one to a custom div
            for char in full_response:
                typed_response += char
                # Build the custom HTML structure for the 'hacker look'
                html_output = f'<div class="hacker-response-container">{typed_response}</div>'
                response_placeholder.markdown(html_output, unsafe_allow_html=True)
                # Controls the speed (small delay makes it look like live typing)
                time.sleep(0.007) 
            # --- 🦾 END TYPEWRITER ---
            
            # Persist message for normal rendering on reload
            st.session_state.messages_display.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            scanner_placeholder.empty() # In case of crash, hide loader
            # Handle Quota / Connection errors
            if "429" in str(e) or "EXHAUSTED" in str(e).upper():
                st.session_state.current_key_index += 1 # Switch key
                del st.session_state.chat_session # Clean session to reload fresh key
                st.warning("⚠️ Engine optimized due to high load. Click Enter again to resend safely!")
            else:
                st.error(f"Medical Engine Interrupted: {e}")import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE CONFIGURATION & PREMIUM BLACK MAGIC THEME (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Concierge",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for the full Premium Design, Hacker Typing, and Medical Scanner
st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp {
        background: linear-gradient(135deg, #0B1511 0%, #040806 100%);
        color: #E2E8F0;
    }
    
    /* Header Custom Styling (As seen in image_3.png) */
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: 5px;
        text-shadow: 0px 4px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Premium Badge (Active Status) */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 30px;
    }
    .premium-badge {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0px 4px 15px rgba(16, 185, 129, 0.2);
        letter-spacing: 0.5px;
    }
    
    /* Input field styling (Responsive, Sleek) */
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(20, 35, 30, 0.5) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        color: #E2E8F0 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* 🦾 MEDICAL SCANNER LOADING ANIMATION (Premium Feature) */
    @keyframes scan-animation {
        0% { transform: translateY(-100%) translateX(-100%); opacity: 0; }
        20% { opacity: 0.8; }
        100% { transform: translateY(100%) translateX(100%); opacity: 0; }
    }
    .medical-scanner {
        position: relative;
        width: 100%;
        height: 200px;
        background: rgba(16, 185, 129, 0.03);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .medical-scanner::after {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 200%; height: 200%;
        background: linear-gradient(135deg, rgba(16,185,129,0) 0%, rgba(16,185,129,0.3) 50%, rgba(16,185,129,0) 100%);
        animation: scan-animation 2s linear infinite;
    }
    .scanner-text {
        position: absolute;
        bottom: 10px; left: 15px;
        color: #10B981;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Hacker Styling for AI Response Container */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace; /* Classic hacker look */
        line-height: 1.6;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Top UI Branding and Badge (image_3.png compliant)
# ------------------------------------------------------------------------------
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">✨ Multi-Engine Enterprise Mode: Active</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY ROTATOR LOGIC (ANTI-EXHAUST SYSTEM)
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

# Fallback case (if only old key exists)
if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# ==============================================================================
# 3. CHAT INITIALIZATION & UI MESSAGES
# ==============================================================================
# System instructions to lock AI persona (God Mode)
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, "
    "and wellness advisor. Provide highly accurate, professional, and empathetic medical insights. "
    "Always maintain your specialist persona and end with a friendly disclaimer that you are an AI."
)

# Initialize messages display and chat session in state
if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "chat_session" not in st.session_state:
    if not KEYS_POOL:
        st.error("🚨 API Key missing! Please configure Streamlit Secrets (A, B, C).")
        st.stop()
        
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    try:
        active_key = KEYS_POOL[idx]
        ai_client = genai.Client(api_key=active_key)
        st.session_state.chat_session = ai_client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
        )
    except Exception as e:
        st.error(f"Engine connection failed: {e}")
        st.stop()

# ------------------------------------------------------------------------------
# Chat History Renderer (Normal for old messages)
# ------------------------------------------------------------------------------
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        # Use normal display for history to avoid slow rendering
        st.markdown(msg["content"])

# ==============================================================================
# 4. LIVE INPUT HANDLER (Premium UI + Hacker Typewriter)
# ==============================================================================
if user_query := st.chat_input("Enter physical symptoms, medication queries...", key="heydoctor_chat_input"):
    
    # 1. Show user message instantly
    with st.chat_message("user"):
        st.markdown(user_query)
    # Persist message
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    # 2. Start AI Response Flow
    with st.chat_message("assistant"):
        # 🦾 MEDICAL SCANNER LOADING (UI Element)
        scanner_placeholder = st.empty()
        scanner_placeholder.markdown("""
            <div class="medical-scanner">
                <div class="scanner-text">
                    SYSTEM::INITIALIZING...<br>
                    SCANNING BIOMARKERS...<br>
                    QUERYING MEDICAL DATABASE...
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Hacker-style response container (Empty initially)
        response_placeholder = st.empty()
        
        try:
            # 🔄 AI Prediction Request (This is the long process)
            response = st.session_state.chat_session.send_message(user_query)
            # Medical scan over, hide the animation
            scanner_placeholder.empty()
            
            # --- 🦾 HACKER-STYLE TYPEWRITER EFFECT ---
            full_response = response.text
            typed_response = ""
            # Loop through characters and print them one by one to a custom div
            for char in full_response:
                typed_response += char
                # Build the custom HTML structure for the 'hacker look'
                html_output = f'<div class="hacker-response-container">{typed_response}</div>'
                response_placeholder.markdown(html_output, unsafe_allow_html=True)
                # Controls the speed (small delay makes it look like live typing)
                time.sleep(0.007) 
            # --- 🦾 END TYPEWRITER ---
            
            # Persist message for normal rendering on reload
            st.session_state.messages_display.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            scanner_placeholder.empty() # In case of crash, hide loader
            # Handle Quota / Connection errors
            if "429" in str(e) or "EXHAUSTED" in str(e).upper():
                st.session_state.current_key_index += 1 # Switch key
                del st.session_state.chat_session # Clean session to reload fresh key
                st.warning("⚠️ Engine optimized due to high load. Click Enter again to resend safely!")
            else:
                st.error(f"Medical Engine Interrupted: {e}")
