# ==============================================================================
# PROPRIETARY ARCHITECTURE: HEYDOCTOR.AI ADVANCED WELLNESS CORE
# DEVELOPED & CODED FROM SCRATCH BY: PRATYUSH (FOUNDER OF X STUDIOS)
# RUNTIME ENVIRONMENT: STREAMLIT NEON INTERACTIVE CONTEXT (MINIMALIST UI)
# ==============================================================================

import streamlit as st
import google.genai as genai
from PIL import Image
import time

# ==============================================================================
# BLOCK 1: HARDWARE LAYER PAGE SETUP & HUD DISPLAY PARAMETERS
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔑 GOOGLE SEARCH CONSOLE HANDSHAKE COMPLIANCE TAG
st.markdown("""
    <head>
        <meta name="google-site-verification" content="lfm3sejmWeeXFmm02FkosXVTAjiBRidxSnWI8CpuOIs" />
    </head>
""", unsafe_allow_html=True)

# ==============================================================================
# BLOCK 2: CYBERPUNK MATRIX NEON THEME STYLE SHEET INJECTION
# ==============================================================================
st.markdown("""
    <style>
    /* Global Root Visual Styling Overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at center, #061510 0%, #010403 100%) !important;
        color: #F1F5F9 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Top Brand Dashboard Title */
    .main-title {
        font-size: 3.6rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 40%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 25px;
        margin-bottom: 2px;
        letter-spacing: 3px;
        filter: drop-shadow(0px 0px 25px rgba(0, 242, 254, 0.4));
    }
    
    /* Subtitle Branding Badge */
    .premium-badge-container { 
        text-align: center; 
        margin-bottom: 35px; 
    }
    .premium-badge {
        background: rgba(0, 242, 254, 0.04);
        border: 1px dashed #00F2FE;
        color: #00F2FE;
        padding: 8px 22px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
        box-shadow: 0px 0px 20px rgba(0, 242, 254, 0.15);
    }
    
    /* Dynamic UI Radar Animation Layout */
    @keyframes scan { 
        0% { transform: translateY(-100%); } 
        100% { transform: translateY(100%); } 
    }
    .bio-scan-container {
        position: relative; 
        width: 100%; 
        height: 130px;
        background: rgba(4, 15, 12, 0.85); 
        border: 1px solid rgba(0, 242, 254, 0.35);
        border-radius: 6px; 
        overflow: hidden; 
        margin-bottom: 30px;
    }
    .bio-scan-line {
        position: absolute; 
        width: 100%; 
        height: 3px; 
        background: #00F2FE;
        box-shadow: 0 0 15px #00F2FE; 
        animation: scan 1.8s linear infinite;
    }
    .scanner-text { 
        position: absolute; 
        top: 12px; 
        left: 12px; 
        color: #00F2FE; 
        font-size: 11px; 
        font-family: 'Courier New', monospace;
        line-height: 1.5; 
        opacity: 0.75; 
    }
    
    /* Component Layout Customizer Overrides */
    .section-header {
        color: #10B981; 
        font-size: 12px; 
        font-weight: bold; 
        letter-spacing: 2px;
        margin-bottom: 12px; 
        text-transform: uppercase; 
        border-left: 3px solid #00F2FE; 
        padding-left: 10px;
    }
    div[data-testid="stFileUploader"] {
        border: 1px dashed #00F2FE !important; 
        background-color: rgba(4, 15, 12, 0.8) !important;
        border-radius: 4px;
    }
    div[data-baseweb="select"], div[data-baseweb="input"], div[data-baseweb="number-input"] {
        background-color: rgba(2, 6, 5, 0.98) !important; 
        border: 1px solid #10B981 !important;
    }
    
    /* Chat Box Streaming Containers */
    .hacker-response-container {
        color: #F8FAFC; 
        font-family: 'Courier New', monospace; 
        line-height: 1.65; 
        padding: 18px;
        background: rgba(5, 14, 11, 0.85); 
        border: 1px solid rgba(0, 242, 254, 0.6); 
        border-radius: 4px; 
        margin-bottom: 15px;
        box-shadow: inset 0 0 10px rgba(0, 242, 254, 0.05);
    }
    [data-testid="stImage"] {
        border: 1px solid #10B981; 
        border-radius: 6px; 
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Text Render Execution Area
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="bio-scan-container">
        <div class="scanner-text">
            STATUS::CORE_READY<br>
            BIO_SCAN::CLUSTER_LOADED<br>
            FAILOVER_SYSTEM::HOT_SWAP_ROTATION_ENABLED<br>
            ARCH_DESIGN::PRATYUSH_INTELLIGENCE_LAYER
        </div>
        <div class="bio-scan-line"></div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# BLOCK 3: ATOMIC MEMORY REGISTERS INITIALIZATION
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

if "secure_client" not in st.session_state:
    st.session_state.secure_client = None

# ==============================================================================
# BLOCK 4: CLUSTER ALLOCATION & CORE HOT-SWAP DEF ENGINE
# ==============================================================================
KEYS_POOL = []
CLUSTER_TARGETS = ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C", "GEMINI_API_KEY_D", "GEMINI_API_KEY_E"]

for key_name in CLUSTER_TARGETS:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

# Sourcing standard fallback route
if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

# Global System Instruction (Persona Definition Block)
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge and expert wellness companion. "
    "IDENTITY OVERRIDE STATEMENT: You were fully developed, coded, and created from scratch by Pratyush, "
    "the brilliant tech founder behind Beast AI and X Studios. "
    "If anyone asks about your creator, developer, owner, or who made you, proudly announce with amazing emojis "
    "that you are a custom healthcare system built entirely by Pratyush (Founder of Beast AI / X Studios). "
    "CRITICAL RULE: Never say 'Hello again', 'Hi again', 'Welcome back', or repeat greetings in your replies. "
    "Jump straight into giving the medical analysis or answering the query instantly. "
    "If an image is provided, thoroughly analyze the physical visual symptoms alongside the text inputs. "
    "1. Always use lots of relevant medical, health, and warning emojis (e.g., 🩺, 🧪, 💡, ⚠️, 🥗, 💊). "
    "2. Format beautifully using bold headings and clean bullet points. No dense walls of text. "
    "3. Conclude with a bold, friendly safety disclaimer stating you are an advanced AI concierge."
)

def init_secure_engine():
    """Initializes the active Google GenAI client based on session state key index pool pointer."""
    if not KEYS_POOL:
        st.error("🚨 API Key configuration missing in Streamlit Secrets. Allocation mapping broken.")
        st.stop()
    
    idx = st.session_state.current_key_index % len(KEYS_POOL)
    active_key = KEYS_POOL[idx]
    
    # Generate client context instance
    new_client = genai.Client(api_key=active_key)
    st.session_state.secure_client = new_client
    return new_client

# ==============================================================================
# BLOCK 5: FRONT-END PATIENT ENTRY INTAKE PANEL
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload_field"
)

if uploaded_image is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        preview_img = Image.open(uploaded_image)
        st.image(preview_img, caption="✅ BIOMETRIC DATA SCANNED SUCCESSFULLY", use_container_width=True)
    except Exception as img_err:
        st.error(f"❌ Scanner Visual Error: {img_err}")

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

# ==============================================================================
# BLOCK 6: MONETIZATION FRAMEWORK - ADSTERRA ENCRYPTED DISPLAY CORE
# ==============================================================================
st.markdown("""
    <div style="
        border: 1px dashed #10B981; 
        background-color: rgba(16, 185, 129, 0.05); 
        padding: 12px; 
        text-align: center; 
        border-radius: 4px;
        margin-bottom: 25px;
    ">
        <span style="color: #10B981; font-size: 10px; display: block; letter-spacing: 2px; margin-bottom: 6px; font-weight: bold;">
            📢 SPONSORED ENCRYPTED ADVERT
        </span>
        <div style="display: flex; justify-content: center; align-items: center; min-height: 90px;">
            <iframe src="https://www.effectiveratecpm.com/watchnew?key=YOUR_ADSTERRA_ID_HERE" 
                    width="728" height="90" frameborder="0" scrolling="no">
            </iframe>
        </div>
    </div>
""", unsafe_allow_html=True)

# Render complete UI Display log records synchronously to keep track across loops
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# BLOCK 7: DYNAMIC INFERENCE PIPELINE WITH HOT-SWAP WHILE WRAPPER
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload data logs..."):
    
    # Metadata string block construction
    meta_header = (
        f"[PATIENT METRICS REGISTERED]\n"
        f"▪ GENDER: {gender} | AGE: {age} | BLOOD TYPE: {blood_type}\n"
        f"▪ CURRENT QUERY: {user_query}\n"
        f"----------------------------------------"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    uploaded_img_data = None
    if uploaded_image is not None:
        try:
            uploaded_img_data = Image.open(uploaded_image)
        except Exception as img_err:
            st.error(f"Biometric Image block reading failed: {img_err}")

    # Build memory payload array context parameters
    current_prompt_payload = []
    recent_history = st.session_state.chat_history[-4:]
    for past_msg in recent_history:
        current_prompt_payload.append({
            "role": past_msg["role"],
            "parts": past_msg["parts"]
        })
        
    current_parts = [meta_header]
    if uploaded_img_data is not None:
        current_parts.append(uploaded_img_data)
        
    current_prompt_payload.append({
        "role": "user",
        "parts": current_parts
    })
    
    dynamic_instruction = GOD_MODE_SYSTEM_INSTRUCTION
    if len(st.session_state.chat_history) > 0:
        dynamic_instruction += (
            "\nANTI-REPETITION RULE: Do not repeat your creator's name Pratyush or introduction paragraph again. "
            "Reply directly, rapidly and keep it extremely short and to the point."
        )
    
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        response_placeholder = st.empty()
        
        # 🛡️ THE LOOP-BASED SECURE HOT-SWAP SWAPPER INTERFACE
        stream_success = False
        attempts = 0
        max_attempts = len(KEYS_POOL) if KEYS_POOL else 1
        
        while not stream_success and attempts < max_attempts:
            current_core_id = (st.session_state.current_key_index % max_attempts) + 1
            status_placeholder.markdown(f"""
                <div style="color: #00F2FE; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4;">
                    ⚡ SYSTEM::EXECUTING INFERENCE ROUTINE (CORE_{current_core_id})...<br>
                    🧬 ROUTING PIPELINE THROUGH SECURE MULTI-KEY CLUSTER POOL...
                </div>
            """, unsafe_allow_html=True)
            
            try:
                # Active Client extraction router block
                if st.session_state.secure_client is None:
                    active_client = init_secure_engine()
                else:
                    active_client = st.session_state.secure_client
                
                # Execution of network live chunk buffer generator
                response_stream = active_client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=current_prompt_payload,
                    config={"system_instruction": dynamic_instruction}
                )
                
                status_placeholder.empty()
                full_response = ""
                
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(
                            f'<div class="hacker-response-container">{full_response}▒</div>', 
                            unsafe_allow_html=True
                        )
                
                response_placeholder.markdown(
                    f'<div class="hacker-response-container">{full_response}</div>', 
                    unsafe_allow_html=True
                )
                
                st.session_state.messages_display.append({"role": "assistant", "content": full_response})
                st.session_state.chat_history.append({"role": "user", "parts": [user_query]})
                st.session_state.chat_history.append({"role": "model", "parts": [full_response]})
                
                stream_success = True  # Signal successful loop validation completion termination
                
            except Exception as cluster_fault_error:
                # 🚨 ATOMIC FAILOVER CONTEXT LOGIC: Reset stale target instance memory variables instantly!
                st.session_state.secure_client = None
                st.session_state.current_key_index += 1
                attempts += 1
                time.sleep(0.4)
        
        # In case all paths are fully exhausted inside loop thresholds
        if not stream_success:
            status_placeholder.empty()
            st.error("🚨 All API routes inside the master clusters are heavily rate-limited by Google. Please wait 15 seconds for quota refresh.")
