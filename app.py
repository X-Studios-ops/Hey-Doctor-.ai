import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE SETUP, MULTICOLOR NEON INJECTOR & GOOGLE VERIFICATION
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered"
)

# 🔑 GOOGLE SEARCH CONSOLE VERIFICATION TAG
st.markdown("""
    <head>
        <meta name="google-site-verification" content="lfm3sejmWeeXFmm02FkosXVTAjiBRidxSnWI8CpuOIs" />
    </head>
""", unsafe_allow_html=True)

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
            QUOTA::GEMINI_5X_CLUSTER
        </div>
        <div class="bio-scan-line"></div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SECURE 5-API CLUSTER ROUTING & WATERTIGHT RUNTIME
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C", "GEMINI_API_KEY_D", "GEMINI_API_KEY_E"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# 🌟 5-ENGINE IDENTITY SETUP: CREATOR TAG SECURELY BINDED
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge and expert wellness companion. "
    "IDENTITY OVERRIDE STATEMENT: You were fully developed, coded, and created by Beast AI (also known as X Studios). "
    "If anyone asks about your creator, developer, owner, or who made you, proudly announce with stellar emojis "
    "that you are a custom proprietary healthcare engine built from scratch by Beast AI / X Studios. "
    "CRITICAL RULE: Never say 'Hello again', 'Hi again', 'Welcome back', or repeat greetings in your replies. "
    "Jump straight into giving the medical analysis or answering the query instantly. "
    "1. Always use lots of relevant medical, health, and warning emojis (e.g., 🩺, 🧪, 💡, ⚠️, 🥗, 💊). "
    "2. Format beautifully using bold headings and clean bullet points. No dense walls of text. "
    "3. Conclude with a bold, friendly safety disclaimer stating you are an advanced AI concierge."
)

def init_secure_engine():
    """Initializes client and chat simultaneously inside state cache to guarantee immunity from closed pipes"""
    if not KEYS_POOL:
        st.error("🚨 API Key configuration missing in Streamlit Secrets.")
        st.stop()
        
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    try:
        active_key = KEYS_POOL[idx]
        new_client = genai.Client(api_key=active_key)
        new_chat = new_client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
        )
        st.session_state.secure_client = new_client
        st.session_state.secure_chat = new_chat
        return new_chat
    except Exception as e:
        st.session_state.current_key_index += 1
        idx = st.session_state.current_key_index % len(KEYS_POOL)
        active_key = KEYS_POOL[idx]
        new_client = genai.Client(api_key=active_key)
        new_chat = new_client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
        )
        st.session_state.secure_client = new_client
        st.session_state.secure_chat = new_chat
        return new_chat

# Verify engine integrity on run
if "secure_chat" not in st.session_state or not st.session_state.secure_chat:
    init_secure_engine()

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
    gender = st.selectbox("Gender Select", ["Male", "Female", "AB", "Custom"], key="patient_gender_selector", label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-header">ENTER AGE</div>', unsafe_allow_html=True)
    age = st.number_input("Age Input", min_value=1, max_value=120, value=18, step=1, key="patient_age_input", label_visibility="collapsed")

with col3:
    st.markdown('<div class="section-header">BLOOD TYPE</div>', unsafe_allow_html=True)
    blood_type = st.selectbox("Blood Select", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key="patient_blood_selector", label_visibility="collapsed")

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
                🧬 METRICS INJECTED SECURELY INTO 5-KEY ENGINE CLUSTER...
            </div>
        """, unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        
        try:
            if "secure_chat" not in st.session_state or st.session_state.secure_chat is None:
                current_chat = init_secure_engine()
            else:
                current_chat = st.session_state.secure_chat
                
            response = current_chat.send_message(full_meta_prompt)
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
            st.session_state.current_key_index += 1
            st.session_state.secure_chat = None
            st.session_state.secure_client = None
            
            try:
                backup_chat = init_secure_engine()
                response = backup_chat.send_message(full_meta_prompt)
                full_response = response.text
                typed_response = ""
                for char in full_response:
                    typed_response += char
                    response_placeholder.markdown(f'<div class="hacker-response-container">{typed_response}</div>', unsafe_allow_html=True)
                    time.sleep(0.005)
                st.session_state.messages_display.append({"role": "assistant", "content": full_response})
            except Exception as cluster_err:
                st.error(f"Inference cluster overload: {cluster_err}. Please refresh and send once more!")
