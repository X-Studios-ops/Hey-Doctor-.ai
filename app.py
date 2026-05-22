import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. ADVANCED STYLED CONFIGURATION (CONCEPT RE-ALIGNMENT)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Bio-Scanner",
    page_icon="🩺",
    layout="centered"
)

# Advanced Glowing Cyber CSS to match the layout blueprint closely
st.markdown("""
    <style>
    /* Premium Dark Mainframe Background */
    .stApp {
        background: radial-gradient(circle at top, #0C1E17 0%, #030605 100%);
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
    }
    
    /* Neon Glow Title Styling */
    .main-title {
        font-size: 3.6rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #059669 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 15px;
        margin-bottom: 2px;
        letter-spacing: 3px;
        filter: drop-shadow(0px 0px 20px rgba(16, 185, 129, 0.5));
    }
    
    /* Status Badge Container */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 35px;
    }
    .premium-badge {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 6px 20px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        display: inline-block;
        letter-spacing: 1px;
        box-shadow: 0px 0px 12px rgba(16, 185, 129, 0.25);
    }
    
    /* Structured Interface Headers */
    .section-header {
        color: #34D399;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        padding-bottom: 4px;
    }

    /* Bio-Scanner Box Customization */
    div[data-testid="stFileUploader"] {
        border: 1px dashed #10B981 !important;
        background-color: rgba(6, 20, 15, 0.4) !important;
        border-radius: 6px !important;
        padding: 25px !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.05);
    }

    /* Custom Input Wrappers for Dropdowns and Numeric Inputs */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(4, 10, 8, 0.9) !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
        border-radius: 4px !important;
    }
    
    /* Terminal Output Panel */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        padding: 15px;
        background: rgba(6, 15, 12, 0.5);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 4px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Brand Elements
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY MANAGMENT & ROUTING
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
# 3. BACKEND SESSION INITIALIZATION
# ==============================================================================
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge. "
    "Analyze context strings provided alongside patient data parameters. "
    "Provide clinical insight. Conclude with an administrative AI disclosure."
)

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "chat_session" not in st.session_state:
    if not KEYS_POOL:
        st.error("🚨 API Key missing! Check Streamlit Secrets configuration.")
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
        st.error(f"Engine pipeline offline: {e}")
        st.stop()

# ==============================================================================
# 4. DATA MATRIX PRESENTATION (LAYOUT GRID)
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR DIAGNOSTIC SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload"
)

st.markdown("<br>", unsafe_allow_html=True)

# Parameters Input Matrix
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

st.markdown("<br><hr style='border-color: rgba(16, 185, 129, 0.15);'>", unsafe_allow_html=True)

# Persistent Historical Log Renderer
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 5. CORE TRANSACTION PIPELINE (TRANSMISSION HANDLER)
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload data logs..."):
    
    # Structure comprehensive system string payload
    full_meta_prompt = (
        f"[METRIC COMPILATION]\n"
        f"▪ GENDER CONFIGURATION: {gender}\n"
        f"▪ METRIC AGE: {age}\n"
        f"▪ BLOOD CLASSIFICATION: {blood_type}\n"
        f"▪ STATEMENT LOG: {user_query}"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div style="color: #10B981; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4;">
                ⚡ ACTION::PARSING QUANTUM BIOMARKERS...<br>
                🧬 METRICS MERGED WITH CORE CONCIERGE VECTOR...
            </div>
        """, unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        
        try:
            response = st.session_state.chat_session.send_message(full_meta_prompt)
            status_placeholder.empty()
            
            # --- TERMINAL TYPEWRITER RENDERING ---
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
                st.warning("⚠️ Stream Route Reset. Re-enter query payload to authorize transmission.")
            else:
                st.error(f"Inference Failure: {e}")
