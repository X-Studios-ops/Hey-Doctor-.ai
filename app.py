import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE CONFIGURATION & CYBERPUNK MEDICAL THEME (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Bio-Scanner",
    page_icon="🩺",
    layout="centered"
)

# Custom High-End Cyberpunk Glowing CSS
st.markdown("""
    <style>
    /* Full Dark Cyberpunk Background */
    .stApp {
        background: linear-gradient(135deg, #050E0B 0%, #020403 100%);
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
    }
    
    /* Main Title Metallic Glow */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #059669 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: 2px;
        letter-spacing: 2px;
        filter: drop-shadow(0px 0px 15px rgba(16, 185, 129, 0.6));
    }
    
    /* Premium Sub-Badge */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 25px;
    }
    .premium-badge {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 5px 18px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0px 0px 10px rgba(16, 185, 129, 0.3);
    }
    
    /* Section Headings */
    .section-header {
        color: #34D399;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* File Uploader Cyber Styling */
    div[data-testid="stFileUploader"] {
        border: 2px dashed rgba(16, 185, 129, 0.4) !important;
        background-color: rgba(6, 18, 14, 0.6) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.1);
    }
    div[data-testid="stFileUploader"] label {
        color: #34D399 !important;
        font-weight: bold !important;
    }

    /* Cyber Inputs Look */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(6, 18, 14, 0.8) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Chat Response Container */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
        line-height: 1.7;
        padding: 15px;
        background: rgba(10, 25, 20, 0.3);
        border-left: 3px solid #10B981;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Branding
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY ROTATOR LOGIC
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
# 3. CHAT INITIALIZATION & CORE PERSONA
# ==============================================================================
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge. "
    "Analyze symptoms along with provided patient metrics (Age, Gender, Blood Type). "
    "Provide highly accurate, professional medical insights. End with an AI disclaimer."
)

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

# ==============================================================================
# 4. NEW ADVANCED METERICS GRAPHICS (BIO-SCANNER INPUTS)
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

# File Uploader Section for Medical Images
uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload"
)

st.markdown("<br>", unsafe_allow_html=True)

# 3-Column Patient Bio Metrics Grid (Gender, Age, Blood Type)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-header">SELECT GENDER</div>', unsafe_allow_html=True)
    gender = st.selectbox("", ["Male", "Female", "AB", "Custom", "Other"], label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-header">ENTER AGE</div>', unsafe_allow_html=True)
    age = st.number_input("", min_value=1, max_value=120, value=18, step=1, label_visibility="collapsed")

with col3:
    st.markdown('<div class="section-header">BLOOD TYPE</div>', unsafe_allow_html=True)
    blood_type = st.selectbox("", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], label_visibility="collapsed")

st.markdown("<br><hr style='border-color: rgba(16, 185, 129, 0.2);'>", unsafe_allow_html=True)

# Old Chat History Renderer
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 5. STREAMLINED ACTION HANDLER (PRO INFERENCE ENGINE)
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload photo queries..."):
    
    # Context pack banana taaki AI patient ka Age/Gender/Blood group yaad rakhe
    full_meta_prompt = (
        f"[PATIENT DATA COMPILING]\n"
        f"▪ GENDER: {gender}\n"
        f"▪ AGE: {age}\n"
        f"▪ BLOOD TYPE: {blood_type}\n"
        f"▪ CHIEF COMPLAINT: {user_query}"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        # Custom Terminal-Style Medical Loading Text
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div style="color: #10B981; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.5;">
                ⚡ SYSTEM::INITIALIZING BIO-SCAN ENGINE...<br>
                🧬 ANALYZING BIOMARKERS AND PATIENT METRICS...<br>
                📥 PATIENT DATA PACKET INJECTED SUCCESSFULLY.
            </div>
        """, unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        
        try:
            # Send message to Gemini with all the metadata embedded
            response = st.session_state.chat_session.send_message(full_meta_prompt)
            status_placeholder.empty() # Remove loader text
            
            # --- PROFESSIONAL TYPEWRITER ANIMATION ---
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
                st.warning("⚠️ High Load Switch triggered. Press Enter to re-send data securely!")
            else:
                st.error(f"Inference Interrupted: {e}")
