import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. ULTIMATE NEON PREMIUM INJECTOR (THEME & GLOW)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Bio-Scanner",
    page_icon="🩺",
    layout="centered"
)

# Hardcore CSS Override to force custom layout structure
st.markdown("""
    <style>
    /* Force background and cyberpunk font */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #06130E 0%, #020504 100%) !important;
        color: #E2E8F0 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Premium Title Design */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        filter: drop-shadow(0px 0px 15px rgba(16, 185, 129, 0.5));
    }
    
    .premium-badge-container { text-align: center; margin-bottom: 30px; }
    .premium-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* Sci-Fi Container Custom Headers */
    .section-header {
        color: #34D399;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        text-transform: uppercase;
        text-shadow: 0 0 8px rgba(52, 211, 153, 0.4);
    }

    /* Force Border Glow on Image Uploader */
    div[data-testid="stFileUploader"] {
        border: 2px solid #10B981 !important;
        background-color: rgba(6, 22, 16, 0.6) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15) !important;
    }

    /* Custom Styling for the Multi-Columns Selectors */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(4, 11, 8, 0.95) !important;
        border: 1px solid #10B981 !important;
        border-radius: 6px !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
    }
    
    /* Custom Output Terminal Box */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        padding: 15px;
        background: rgba(5, 16, 12, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.1);
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY MANAGMENT
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# ==============================================================================
# 3. CHAT INITIALIZATION & MEMORY SETUP
# ==============================================================================
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge. "
    "Provide advanced clinical insights based on patient data metrics."
    "Always conclude with an AI administrative safety disclaimer."
)

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "chat_session" not in st.session_state:
    if not KEYS_POOL:
        st.error("🚨 API Key missing! Check Streamlit Secrets.")
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
        st.error(f"Mainframe pipeline offline: {e}")
        st.stop()

# ==============================================================================
# 4. DIGITAL BIO-METRIC STRUCTURED INPUTS
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload"
)

st.markdown("<br>", unsafe_allow_html=True)

# Parameters Input Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-header">SELECT GENDER</div>', unsafe_allow_html=True)
    gender = st.selectbox("", ["Male", "Female", "AB", "Custom"], label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-header">ENTER AGE</div>', unsafe_allow_html=True)
    age = st.number_input("", min_value=1, max_value=120, value=18, step=1, label_visibility="collapsed")

with col3:
    st.markdown('<div class="section-header">BLOOD TYPE</div>', unsafe_allow_html=True)
    blood_type = st.selectbox("", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], label_visibility="collapsed")

st.markdown("<br><hr style='border-color: rgba(16, 185, 129, 0.2);'>", unsafe_allow_html=True)

# History Renderer
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 5. CORE INFERENCE HANDLER
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload photo queries..."):
    
    full_meta_prompt = (
        f"[PATIENT REPORT LOG]\n"
        f"▪ GENDER: {gender}\n"
        f"▪ AGE: {age}\n"
        f"▪ BLOOD TYPE: {blood_type}\n"
        f"▪ QUERY: {user_query}"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div style="color: #10B981; font-family: 'Courier New', monospace; font-size: 12px;">
                ⚡ COMPILING PATIENT BIOMARKERS...<br>
                🧬 DATA INJECTED INTO CORE CONCIERGE ENGINE...
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
            if "429" in str(e) or "EXHAUSTED" in str(e).upper():
                st.session_state.current_key_index += 1
                if "chat_session" in st.session_state: del st.session_state.chat_session
                st.warning("⚠️ High load route switch. Please hit enter again to authorize data packet!")
            else:
                st.error(f"Transmission Interrupted: {e}")
