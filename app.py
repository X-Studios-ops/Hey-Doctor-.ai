import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. ADVANCED HIGH-END CYBERPUNK MAIN FRAME CONFIGURATION (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Multi-Engine Bio-Scanner",
    page_icon="🩺",
    layout="centered"
)

# Deep Cyber Styling: Multi-Color Gradient, Neon Glows, Monospace Terminal Font
st.markdown("""
    <style>
    /* Full Dark Cyborg Mainframe Background */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #040907 0%, #010202 100%) !important;
        color: #E2E8F0 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Ultimate Metallic Gradient Title (image_17.png blueprint style) */
    .main-title {
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #10B981 0%, #34D399 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 25px;
        letter-spacing: 2.5px;
        filter: drop-shadow(0px 0px 25px rgba(16, 185, 129, 0.6));
    }
    
    /* High-Status Badge (Active Mode) */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 35px;
    }
    .premium-badge {
        background: rgba(16, 185, 129, 0.05);
        border: 2px solid rgba(16, 185, 129, 0.5);
        color: #34D399;
        padding: 5px 18px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0px 0px 15px rgba(16, 185, 129, 0.25);
    }
    
    /* Interface Section Headings (image_17.png) */
    .section-header {
        color: #34D399;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* Heavy Duty Image Uploader Box */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(16, 185, 129, 0.4) !important;
        background-color: rgba(6, 18, 14, 0.4) !important;
        border-radius: 6px !important;
        padding: 25px !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.05);
    }
    
    /* Sleek Multi-Color Selector Matrix */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(5, 15, 12, 0.95) !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
        border-radius: 4px !important;
        box-shadow: inset 0 0 10px rgba(16, 185, 129, 0.05);
    }
    
    /* Hacker-Style Chat Response Terminal */
    .hacker-response-container {
        color: #E2E8F0;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        padding: 15px;
        background: rgba(8, 20, 16, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 4px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Multi-Color Neon Branding
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. MULTI-API KEY MANAGMENT & CONCIERGE SETUP
# ==============================================================================
# Get all active keys safely from Streamlit Secrets
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

# Old single key fallback
if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# ------------------------------------------------------------------------------
# Core AI Persona Initializer (System Instruction Lock)
# ------------------------------------------------------------------------------
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge. Provide advanced medical insights. "
    "Maintain specialist persona. Conclude with an administrative AI disclosure."
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
        st.error(f"Engine connection failure: {e}")
        st.stop()

# ==============================================================================
# 3. ADVANCED BIO-SCANNER INTERFACE LAYOUT (as requested)
# ==============================================================================
# Header with extra space
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)

# Large file uploader section
uploaded_image = st.file_uploader(
    "DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", 
    type=["jpg", "jpeg", "png"],
    key="bio_scanner_upload"
)

st.markdown("<br>", unsafe_allow_html=True)

# 3-Column Patient Bio Metrics Grid (Gender, Age, Blood Type side-by-side)
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

st.markdown("<br><hr style='border-color: rgba(16, 185, 129, 0.1);'>", unsafe_allow_html=True)

# Screen par persistent historical log dikhana
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 4. INFERENCE TRANSMISSION & TRANSACTION LOG (ANTI-EXHAUST SYSTEM)
# ==============================================================================
if user_query := st.chat_input("Enter specific physical symptoms or upload photo queries..."):
    
    # Structure comprehensive system string payload (persists Age, Gender, Blood Type)
    full_meta_prompt = (
        f"[METRIC COMPILATION TRANSMISSION]\n"
        f"▪ GENDER CONFIGURATION: {gender}\n"
        f"▪ METRIC AGE: {age}\n"
        f"▪ BLOOD TYPE CLASSIFICATION: {blood_type}\n"
        f"▪ STATEMENT LOG: {user_query}"
    )
    
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        # Custom Terminal-Style Medical Loading Text
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div style="color: #10B981; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.5;">
                ⚡ ACTION::PARSING QUANTUM BIOMARKERS...<br>
                🧬 DATA INJECTED INTO CORE CONCIERGE ENGINE...
            </div>
        """, unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        
        try:
            # Send message to Gemini with all the persistent metadata
            response = st.session_state.chat_session.send_message(full_meta_prompt)
            status_placeholder.empty() # Remove loader
            
            # --- PROFESSIONAL TYPEWRITER ANIMATION (HACKER TERMINAL LOOK) ---
            full_response = response.text
            typed_response = ""
            for char in full_response:
                typed_response += char
                html_output = f'<div class="hacker-response-container">{typed_response}</div>'
                response_placeholder.markdown(html_output, unsafe_allow_html=True)
                # Faster speed (0.005) because Gemini responses are long
                time.sleep(0.005) 
            
            st.session_state.messages_display.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            status_placeholder.empty()
            # If current key fails due to Quota Exhaustion (429)
            if "429" in str(e) or "EXHAUSTED" in str(e).upper():
                st.session_state.current_key_index += 1 # Index badhao
                # Clear session state so next interaction reloads with fresh key
                if "chat_session" in st.session_state: del st.session_state.chat_session
                st.warning("⚠️ Mainframe route optimized due to high load. Click enter again to re-send data securely!")
            else:
                st.error(f"Medical Inference Pipeline Failure: {e}")
