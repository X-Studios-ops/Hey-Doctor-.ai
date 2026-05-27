# ==============================================================================
# PROPRIETARY ARCHITECTURE: HEYDOCTOR.AI ULTRA STABLE ENTERPRISE CORE
# DEVELOPED & OPTIMIZED BY: PRATYUSH (FOUNDER OF BEAST AI / X STUDIOS)
# RUNTIME INFRASTRUCTURE: SMART API ROTATION + HARD-RESET RUNTIME COOLDOWN
# ==============================================================================

import streamlit as st
import google.genai as genai          # <-- ACTIVE AND SET
from google.genai import types  
from PIL import Image
import time
import streamlit.components.v1 as components

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# GOOGLE SEARCH CONSOLE HANDSHAKE
st.markdown("""
<head>
<meta name="google-site-verification" content="lfm3sejmWeeXFmm02FkosXVTAjiBRidxSnWI8CpuOIs"/>
</head>
""", unsafe_allow_html=True)

# ==============================================================================
# CYBERPUNK MATRIX NEON THEME
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
    filter: drop-shadow(0px 0px 20px rgba(0, 242, 254, 0.3));
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
    letter-spacing: 1px;
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
div[data-testid="stChatMessage"] {
    background: rgba(5, 14, 11, 0.85) !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    border-radius: 6px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🔥 ULTRA-FAST LAZY LOAD ADSTERRA CORE (3 SECONDS DELAY ENGINE)
# ==============================================================================
st.markdown("""
    <div style="border: 1px dashed #10B981; background-color: rgba(16, 185, 129, 0.05); padding: 12px; text-align: center; border-radius: 4px; margin-bottom: 15px; margin-top: 5px;">
        <span style="color: #10B981; font-size: 10px; display: block; letter-spacing: 2px; margin-bottom: 6px; font-weight: bold;">📢 SPONSORED ENCRYPTED ADVERT</span>
    </div>
""", unsafe_allow_html=True)

# JavaScript injection jo ad ko 3 second baad inject karegi taaki site superfast khule
components.html("""
    <div id="adsterra-lazy-node" style="display: flex; justify-content: center; align-items: center; width: 100%; min-height: 90px;">
        <span style="color: rgba(241,245,249,0.3); font-size: 11px; font-family: monospace;">INITIALIZING SECURE AD CLUSTER...</span>
    </div>
    
    <script type="text/javascript">
        setTimeout(function() {
            var container = document.getElementById('adsterra-lazy-node');
            container.innerHTML = ''; // Clear loading text
            
            window.atOptions = {
                'key' : '4c180b2176e3a1a287de9e6b76879287',
                'format' : 'iframe',
                'height' : 90,
                'width' : 728,
                'params' : {}
            };
            
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = 'https://www.highperformanceformat.com/4c180b2176e3a1a287de9e6b76879287/invoke.js';
            container.appendChild(script);
        }, 3000); // 3 Seconds precise lazy load delay
    </script>
""", height=110)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE MAIN CORE
# ------------------------------------------------------------------------------
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="premium-badge-container">
<div class="premium-badge">⚡ ENTERPRISE MULTI-CLUSTER ENGINE ACTIVE</div>
</div>
""", unsafe_allow_html=True)

# --- PRODUCT HUNT BADGE ---
badge_code = """
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 25px;">
    <a href="https://www.producthunt.com/products/hey-doctor-ai?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-hey-doctor-ai" target="_blank" rel="noopener noreferrer">
        <img alt="Hey Doctor.ai - Free AI Medical Assistant &amp; Symptom Checker built in Python | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1156270&amp;theme=dark&amp;t=1779795209915" />
    </a>
</div>
"""
components.html(badge_code, height=70)

st.markdown("""
<div class="bio-scan-container">
<div class="scanner-text">
STATUS::ONLINE<br>
SMART_ROUTER::LOAD_BALANCED_ACTIVE<br>
FAILOVER_ENGINE::AUTOMATIC_HARD_RESET_ENABLED<br>
OPTIMIZATION::BY_PRATYUSH_X_STUDIOS
</div>
<div class="bio-scan-line"></div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SECURE ALLOCATION POOL REGISTRY
# ==============================================================================
KEYS_POOL = []
secret_keys = ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C", "GEMINI_API_KEY_D", "GEMINI_API_KEY_E", "GEMINI_API_KEY"]

for key_name in secret_keys:
    if key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL:
    st.error("🚨 CRITICAL METRIC: NO API KEYS DECLARED IN ENVIRONMENT CONFIG.")
    st.stop()

# SESSION STATE MEMORY MANAGEMENT
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "messages_display" not in st.session_state: st.session_state.messages_display = []
if "api_health" not in st.session_state: st.session_state.api_health = {}

for key in KEYS_POOL:
    if key not in st.session_state.api_health:
        st.session_state.api_health[key] = {"fails": 0, "cooldown_until": 0.0}

with st.sidebar:
    st.markdown("### 🛠️ CORE ADMINISTRATIVE NODE")
    if st.button("🔄 FORCE RESET API POOL COOLDOWNS"):
        st.session_state.api_health = {}
        for key in KEYS_POOL: st.session_state.api_health[key] = {"fails": 0, "cooldown_until": 0.0}
        st.success("✅ ALL CLUSTER NODES FLUSHED & HEALTH RESTORED!")

def get_best_available_key():
    current_time = time.time()
    available_keys = [key for key in KEYS_POOL if current_time >= st.session_state.api_health[key]["cooldown_until"]]
    return min(available_keys, key=lambda k: st.session_state.api_health[k]["fails"]) if available_keys else KEYS_POOL[0]

def mark_key_failed(key):
    st.session_state.api_health[key]["fails"] += 1
    st.session_state.api_health[key]["cooldown_until"] = time.time() + 10.0 

def reset_key_health(key):
    if key in st.session_state.api_health: st.session_state.api_health[key]["fails"] = 0

GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge and expert wellness companion. "
    "IDENTITY OVERRIDE STATEMENT: You were fully developed, coded, and created from scratch by Pratyush, "
    "the brilliant tech founder behind Beast AI and X Studios. "
    "If anyone asks about your creator, developer, owner, or who made you, proudly announce with amazing emojis "
    "that you are a custom healthcare system built entirely by Pratyush (Founder of Beast AI / X Studios). "
    "CRITICAL RULE: Never say 'Hello again', 'Hi again', 'Welcome back', or repeat greetings in your replies. "
    "Jump straight into giving the medical analysis or answering the query instantly. "
    "1. Always use lots of relevant medical, health, and warning emojis (e.g., 🩺, 🧪, 💡, ⚠️, 🥗, 💊). "
    "2. Format beautifully using bold headings and clean bullet points. No dense walls of text. "
    "3. Conclude with a bold, friendly safety disclaimer stating you are an advanced AI concierge."
)

# ==============================================================================
# PHYSICAL PHOTO BIO-SCANNER AREA
# ==============================================================================
st.markdown('<div class="section-header">🧬 PHYSICAL PHOTO BIO-SCANNER</div>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("DROP PHYSICAL SYMPTOM PHOTO HERE FOR BIO-SCAN", type=["jpg", "jpeg", "png"], key="medical_bio_uploader_field")

if uploaded_image is not None:
    try:
        preview = Image.open(uploaded_image)
        st.image(preview, caption="✅ BIOMETRIC ARTIFACT CAPTURED", use_container_width=True)
    except Exception as e:
        st.error(f"Scanner Interdiction Fault: {e}")

col1, col2, col3 = st.columns(3)
with col1: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with col2: age = st.number_input("Age", min_value=1, max_value=120, value=18)
with col3: blood_type = st.selectbox("Blood", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

st.markdown("<br><hr style='border-color: rgba(0, 242, 254, 0.15);'>", unsafe_allow_html=True)

# RENDER HISTORICAL CHAT
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# PIPELINE STREAM ENGINE EXECUTION
# ==============================================================================
if user_query := st.chat_input("Describe symptoms or data metrics here..."):
    meta_header = f"""[PATIENT ARTIFACT REGISTERED]\nGender: {gender} | Age: {age} | Blood Type: {blood_type}\n\nCURRENT QUERY MATRIX:\n{user_query}"""

    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages_display.append({"role": "user", "content": user_query})

    uploaded_img_data = None
    if uploaded_image is not None:
        try: uploaded_img_data = Image.open(uploaded_image)
        except Exception: uploaded_img_data = None

    current_prompt_payload = []
    for past_turn in st.session_state.chat_history:
        clean_role = "user" if past_turn["role"] == "user" else "model"
        current_prompt_payload.append(types.Content(role=clean_role, parts=[types.Part.from_text(text=past_turn["text"])]))
    
    current_turn_parts = [types.Part.from_text(text=meta_header)]
    if uploaded_img_data is not None: current_turn_parts.append(types.Part.from_image(uploaded_img_data))
    current_prompt_payload.append(types.Content(role="user", parts=current_turn_parts))

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        status_placeholder = st.empty()
        stream_success = False
        attempts = 0
        max_attempts = len(KEYS_POOL)

        while not stream_success and attempts < max_attempts:
            active_key = get_best_available_key()
            try:
                status_placeholder.markdown("""<div style="color:#00F2FE; font-size:12px; font-family:'Courier New',monospace;">⚡ CONNECTING SMART ENGINE ROUTER CORE...<br>🧠 STREAMING ANALYTICAL DICT SEGMENTS SECURELY...</div>""", unsafe_allow_html=True)
                client = genai.Client(api_key=active_key)
                config_schema = types.GenerateContentConfig(system_instruction=GOD_MODE_SYSTEM_INSTRUCTION, temperature=0.5)
                response_stream = client.models.generate_content_stream(model="gemini-2.5-flash", contents=current_prompt_payload, config=config_schema)

                status_placeholder.empty()
                full_response = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▒")

                response_placeholder.markdown(full_response)
                st.session_state.messages_display.append({"role": "assistant", "content": full_response})
                st.session_state.chat_history.append({"role": "user", "text": meta_header})
                st.session_state.chat_history.append({"role": "model", "text": full_response})

                if len(st.session_state.chat_history) > 6: st.session_state.chat_history = st.session_state.chat_history[-6:]
                reset_key_health(active_key)
                stream_success = True

            except Exception as e:
                mark_key_failed(active_key)
                attempts += 1
                status_placeholder.markdown(f"""<div style="color:#FF4B4B; font-size:11px; font-family:'Courier New',monospace;">⚠️ NODE SWITCH DETECTED: {str(e)[:60]}...</div>""", unsafe_allow_html=True)
                time.sleep(0.5)

        if not stream_success:
            status_placeholder.empty()
            st.error("🚨 INSTANCE COOLDOWN TRIGGERED: Click 'FORCE RESET API POOL COOLDOWNS' in the left sidebar to clear memory leaks.")

    if uploaded_img_data is not None: uploaded_img_data.close()
