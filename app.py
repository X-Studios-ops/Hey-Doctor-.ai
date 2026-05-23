# ==============================================================================
# PROPRIETARY ARCHITECTURE: HEYDOCTOR.AI ADVANCED WELLNESS CORE
# DEVELOPED & OPTIMIZED BY: PRATYUSH (X STUDIOS)
# FULLY OPTIMIZED SMART API ROTATION + MEMORY + SECURITY PATCH
# ==============================================================================

import streamlit as st
import google.genai as genai
from PIL import Image
import time
import random

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# GOOGLE SEARCH CONSOLE VERIFICATION
# ==============================================================================
st.markdown("""
<head>
<meta name="google-site-verification" content="lfm3sejmWeeXFmm02FkosXVTAjiBRidxSnWI8CpuOIs" />
</head>
""", unsafe_allow_html=True)

# ==============================================================================
# CYBERPUNK UI STYLE
# ==============================================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: radial-gradient(circle at center, #061510 0%, #010403 100%) !important;
    color: #F1F5F9 !important;
    font-family: 'Courier New', monospace !important;
}
.main-title {
    font-size: 3.4rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 40%, #10B981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 20px;
    letter-spacing: 3px;
}
.premium-badge-container {
    text-align: center;
    margin-bottom: 25px;
}
.premium-badge {
    background: rgba(0, 242, 254, 0.04);
    border: 1px dashed #00F2FE;
    color: #00F2FE;
    padding: 8px 22px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}
.bio-scan-container {
    position: relative;
    width: 100%;
    height: 120px;
    background: rgba(4, 15, 12, 0.85);
    border: 1px solid rgba(0, 242, 254, 0.35);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 25px;
}
@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
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
    line-height: 1.5;
}
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
.hacker-response-container {
    color: #F8FAFC;
    line-height: 1.7;
    padding: 18px;
    background: rgba(5, 14, 11, 0.85);
    border: 1px solid rgba(0, 242, 254, 0.6);
    border-radius: 4px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# HEADER
# ==============================================================================
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="premium-badge-container">
<div class="premium-badge">
⚡ ENTERPRISE AI HEALTH SYSTEM ACTIVE
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bio-scan-container">
<div class="scanner-text">
STATUS::CORE_READY<br>
BIO_SCAN::ONLINE<br>
API_CLUSTER::ACTIVE<br>
SMART_ROUTER::ENABLED<br>
OPTIMIZATION::BY_PRATYUSH_X_STUDIOS
</div>
<div class="bio-scan-line"></div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION MEMORY
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "api_health" not in st.session_state:
    st.session_state.api_health = {}

# ==============================================================================
# API KEYS POOL MAPPING
# ==============================================================================
KEYS_POOL = []
secret_keys = [
    "GEMINI_API_KEY_A",
    "GEMINI_API_KEY_B",
    "GEMINI_API_KEY_C",
    "GEMINI_API_KEY_D",
    "GEMINI_API_KEY_E",
    "GEMINI_API_KEY"
]

for key_name in secret_keys:
    if key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL:
    st.error("🚨 NO API KEYS FOUND IN STREAMLIT SECRETS")
    st.stop()

# ==============================================================================
# API HEALTH REGISTRY
# ==============================================================================
for key in KEYS_POOL:
    if key not in st.session_state.api_health:
        st.session_state.api_health[key] = {
            "fails": 0,
            "cooldown_until": 0.0
        }

# ==============================================================================
# SMART KEY ROUTER
# ==============================================================================
def get_best_available_key():
    current_time = time.time()
    available_keys = []

    for key in KEYS_POOL:
        key_data = st.session_state.api_health[key]
        if current_time >= key_data["cooldown_until"]:
            available_keys.append(key)

    if not available_keys:
        return None

    return random.choice(available_keys)

# ==============================================================================
# FAILURE HANDLER
# ==============================================================================
def mark_key_failed(key):
    data = st.session_state.api_health[key]
    data["fails"] += 1
    cooldown = min(120, 5 * data["fails"])
    data["cooldown_until"] = time.time() + cooldown

# ==============================================================================
# RESET HEALTH
# ==============================================================================
def reset_key_health(key):
    st.session_state.api_health[key]["fails"] = 0

# ==============================================================================
# SYSTEM PROMPT (GOD MODE DESIGNER PARAMS)
# ==============================================================================
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

# ==============================================================================
# IMAGE UPLOAD
# ==============================================================================
st.markdown('<div class="section-header">🧬 BIO-SCAN IMAGE UPLOAD</div>', unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "UPLOAD SYMPTOM IMAGE",
    type=["jpg", "jpeg", "png"],
    key="medical_bio_uploader_field"
)

if uploaded_image is not None:
    try:
        preview = Image.open(uploaded_image)
        st.image(
            preview,
            caption="✅ BIOMETRIC ARTIFACT ANALYZED SUCCESSFULLY",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Image Visualizer Error: {e}")

# ==============================================================================
# USER METADATA
# ==============================================================================
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    age = st.number_input("Age", min_value=1, max_value=120, value=18)

with col3:
    blood_type = st.selectbox("Blood", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

st.markdown("<br><hr style='border-color: rgba(0, 242, 254, 0.15);'>", unsafe_allow_html=True)

# ==============================================================================
# DISPLAY HISTORY SYNCHRONOUSLY
# ==============================================================================
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# USER INPUT & INFERENCE PIPELINE
# ==============================================================================
if user_query := st.chat_input("Describe symptoms here..."):

    meta_header = f"""[PATIENT DATA COMPLIANCE]
Gender: {gender} | Age: {age} | Blood Type: {blood_type}

USER SPECIFIC SYMPTOMS:
{user_query}
"""

    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages_display.append({
        "role": "user",
        "content": user_query
    })

    # Safely duplicate data buffer image context
    uploaded_img_data = None
    if uploaded_image is not None:
        try:
            uploaded_img_data = Image.open(uploaded_image)
        except Exception:
            uploaded_img_data = None

    # Payload Array Builder Block
    current_prompt_payload = []
    recent_history = st.session_state.chat_history[-4:]  # Sliced for tokens control

    for item in recent_history:
        current_prompt_payload.append({
            "role": item["role"],
            "parts": item["parts"]
        })

    current_parts = [meta_header]
    if uploaded_img_data is not None:
        current_parts.append(uploaded_img_data)

    current_prompt_payload.append({
        "role": "user",
        "parts": current_parts
    })

    # AI Execution Node
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        status_placeholder = st.empty()

        stream_success = False
        attempts = 0
        max_attempts = len(KEYS_POOL)

        while not stream_success and attempts < max_attempts:
            active_key = get_best_available_key()

            if active_key is None:
                status_placeholder.empty()
                st.error("🚨 ALL AI SERVERS IN THE CLUSTER ARE COOLING DOWN. Please wait 15 seconds.")
                break

            try:
                status_placeholder.markdown(f"""
                <div style="color:#00F2FE; font-size:12px; font-family:'Courier New',monospace;">
                    ⚡ CONNECTING INTEGRATED CLUSTER ENGINE...<br>
                    🧠 BALANCING WORKLOAD PATIENTS LOGS VIA TARGET BACKEND...
                </div>
                """, unsafe_allow_html=True)

                client = genai.Client(api_key=active_key)
                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=current_prompt_payload,
                    config={
                        "system_instruction": GOD_MODE_SYSTEM_INSTRUCTION,
                        "temperature": 0.5
                    }
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

                st.session_state.messages_display.append({
                    "role": "assistant",
                    "content": full_response
                })

                st.session_state.chat_history.append({
                    "role": "user",
                    "parts": [user_query]
                })

                st.session_state.chat_history.append({
                    "role": "model",
                    "parts": [full_response]
                })

                # Strict boundary truncation registers
                if len(st.session_state.chat_history) > 10:
                    st.session_state.chat_history = st.session_state.chat_history[-10:]

                reset_key_health(active_key)
                stream_success = True

            except Exception as cluster_error:
                mark_key_failed(active_key)
                attempts += 1
                status_placeholder.markdown(f"""
                <div style="color:#FF4B4B; font-size:11px;">
                    ⚠️ ROUTE ERROR ON CORE ACTIVE NODE<br>
                    🔄 FAILOVER INITIATING MULTI-SWAP OVERRIDE DIRECTIVE...
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

        if not stream_success:
            status_placeholder.empty()
            st.error("🚨 INTERPRISE CHANNELS EXHAUSTED: Please wait 15 seconds for hot-keys automatic cooldown refresh.")

    # Memory cleanup buffer handles
    if uploaded_img_data is not None:
        uploaded_img_data.close()
