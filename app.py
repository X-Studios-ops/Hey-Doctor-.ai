import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE SETUP & MULTICOLOR NEON INJECTOR
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered"
)

# Heavy-duty custom CSS override to enforce neon multi-color highlights and animations
st.markdown("""
    <style>
    /* Full Application Metallic Canvas */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #061510 0%, #010403 100%) !important;
        color: #F1F5F9 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Multicolor Title (Cyan to Green Gradient) */
    .main-title {
        font-size: 3.6rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 40%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 15px;
        margin-bottom: 2px;
        letter-spacing: 2px;
        filter: drop-shadow(0px 0px 20px rgba(0, 242, 254, 0.4));
    }
    
    /* Advanced Glowing Shield Badge */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 30px;
    }
    .premium-badge {
        background: rgba(0, 242, 254, 0.05);
        border: 1px dashed #00F2FE;
        color: #00F2FE;
        padding: 6px 18px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 0px 15px rgba(0, 242, 254, 0.2);
    }

    /* 🦾 ADVANCED BIO-SCANNER ANIMATION */
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    .bio-scan-container {
        position: relative;
        width: 100%;
        height: 120px;
        background: rgba(4, 15, 12, 0.7);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.1);
    }
    .bio-scan-line {
        position: absolute;
        width: 100%;
        height: 2px;
        background: #00F2FE;
        opacity: 0.8;
        box-shadow: 0 0 10px #00F2FE;
        animation: scan 1.5s linear infinite;
    }
    .scanner-text {
        position: absolute;
        top: 10px;
        left: 10px;
        color: #00F2FE;
        font-size: 10px;
        opacity: 0.6;
    }
    
    /* Structured Section Group Label */
    .section-header {
        color: #10B981;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
        text-transform: uppercase;
        border-left: 3px solid #00F2FE;
        padding-left: 8px;
    }

    /* Photo Scan Drop-Zone Custom Overrides */
    div[data-testid="stFileUploader"] {
        border: 1px solid #00F2FE !important;
        background-color: rgba(4, 15, 12, 0.7) !important;
        border-radius: 4px !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.1) !important;
    }

    /* Input Matrix Component Custom Borders */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(2, 6, 5, 0.95) !important;
        border: 1px solid #10B981 !important;
        border-radius: 4px !important;
    }
    
    /* Output Terminal Panels */
    .hacker-response-container {
        color: #F8FAFC;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        padding: 15px;
        background: rgba(5, 14, 11, 0.8);
        border: 1px solid #00F2FE;
        border-radius: 4px;
        margin-bottom: 12px;
        box-shadow: inset 0 0 15px rgba(0, 242, 254, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Top Brand Presentation
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# 🦾 Animation Block
st.markdown("""
    <div class="bio-scan-container">
        <div class="scanner-text">
            STATUS::LIVE<br>
            BIO_SCAN::ACTIVE<br>
            QUOTA::GEMINI_STABLE_FRAME
        </div>
        <div class="bio-scan-line"></div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SECURE API CLUSTER ROUTING & SELF-HEALING SYSTEM
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# 🌟 HIGH-POWER STYLISH EMOJI PERSONA
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge, premium wellness advisor, and lifestyle expert. "
    "Your response style must be visually outstanding, engaging, and easy to read. "
    "1. Always use lots of context-specific medical, health, and warning emojis (e.g., 🩺, 🧪, 💡, ⚠️, 🥗, 🏋️, 💊, 📉, 🔴). "
    "2. Format your response beautifully using bold headings, concise bullet points, and neat spacing. Never write dense walls of text. "
    "3. Keep your tone highly professional yet modern, encouraging, and clear. "
    "4. Always analyze provided patient parameters (Age, Gender, Blood Type) dynamically. "
    "5. Conclude every message with a bold, friendly safety disclaimer stating you are an advanced AI concierge."
)

def create_fresh_session():
    """Client reset system using the high-availability model"""
    if not KEYS_POOL:
        st.error("🚨 API Key configuration missing in Streamlit Secrets.")
        st.stop()
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    try:
        active_key = KEYS_POOL[idx]
        st.session_state.ai_client = genai.Client(api_key=active_key)
        st.session_state.chat_session = st.session_state.ai_client.chats.create(
            model="gemini-1.5-flash",  # Changed to the most stable high-availability model
            config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
        )
        return True
    except Exception as e:
        st.error(f"Failed to boot engine: {e}")
        return False

# Session management patch
if "chat_session" not in st.session_state or "ai_client" not in st.session_state:
    create_fresh_session()

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

# ==============================================================================
# 3. PATIENT ENTRY PORTAL LAYOUT
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload_field"
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-header">SELECT GENDER</div>', unsafe_allow_html=True)
    gender = st.selectbox("Patient Gender Configuration", ["Male", "Female", "AB", "Custom"], key="patient_gender_selector", label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-header">ENTER AGE</div>', unsafe_allow_html=True)
    age = st.number_input("Patient Age Input", min_value=1, max_value=120, value=18, step=1, key="patient_age_input", label_visibility="collapsed")

with col3:
    st.markdown('<div class="section-header">BLOOD TYPE</div>', unsafe_allow_html=True)
    blood_type = st.selectbox("Patient Blood Type Dropdown", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key="patient_blood_selector", label_visibility="collapsed")

st.markdown("<br><hr style='border-color: rgba(0, 242, 254, 0.15);'>", unsafe_allow_html=True)

# Persistent Historical Rendering Panel
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 4. CORE INFERENCE PIPELINE
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload data logs..."):
    
    full_meta_prompt = (
        f"[CORE REGISTRY REPORT]\n"
        f"▪ GENDER CLASSIFICATION: {gender}\n"
        f"▪ METRIC AGE: {age}\n"
        f"▪ BLOOD TYPE: {blood_type}\n"
        f"▪ QUERY LOG: {user_query}"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div style="color: #00F2FE; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4;">
                ⚡ SYSTEM::PARSING LOGICAL VECTORS...<br>
                🧬 METRICS INJECTED SECURELY INTO CONCIERGE ENGINE...
            </div>
        """, unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        
        try:
            response = st.session_state.chat_session.send_message(full_meta_prompt)
            status_placeholder.empty()
            
            full_response = response.text
            typed_response = ""
            for char in full_response:
                typed_response += char
                response_placeholder.markdown(f'<div class="hacker-response-container">{typed_response}</div>', unsafe_allow_html=True)
                time.sleep(0.005) 
            
            st.session_state.messages_display.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            status_placeholder.empty()
            # Handle rate-limit, closed clients, or 503 server overloads gracefully
            if "429" in str(e) or "EXHAUSTED" in str(e).upper() or "CLOSED" in str(e).upper() or "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                st.session_state.current_key_index += 1
                if "chat_session" in st.session_state: del st.session_state.chat_session
                if "ai_client" in st.session_state: del st.session_state.ai_client
                create_fresh_session()
                st.warning("⚠️ High load pipeline reset. Press Enter once more to authorize data packets securely!")
            else:
                st.error(f"Inference failure: {e}")
