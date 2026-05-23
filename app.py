# ==============================================================================
# HEYDOCTOR.AI ULTRA STABLE ENTERPRISE CORE
# DEVELOPED & OPTIMIZED BY: PRATYUSH (X STUDIOS)
# FULL SMART API ROTATION + FAILOVER + CACHE + MEMORY PATCH
# ==============================================================================

import streamlit as st
import google.genai as genai
from PIL import Image
import time

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# GOOGLE VERIFICATION
# ==============================================================================
st.markdown("""
<head>
<meta name="google-site-verification"
content="lfm3sejmWeeXFmm02FkosXVTAjiBRidxSnWI8CpuOIs"/>
</head>
""", unsafe_allow_html=True)

# ==============================================================================
# CYBERPUNK UI
# ==============================================================================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #061510 0%, #010403 100%);
    color: #F1F5F9;
    font-family: 'Courier New', monospace;
}

.main-title {
    font-size: 3.2rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(
        90deg,
        #00F2FE 0%,
        #4FACFE 40%,
        #10B981 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-top: 20px;
    margin-bottom: 10px;
}

.section-header {
    color: #10B981;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 10px;
    border-left: 3px solid #00F2FE;
    padding-left: 10px;
}

.hacker-response-container {

    color: #F8FAFC;
    line-height: 1.7;

    padding: 18px;

    background: rgba(5, 14, 11, 0.85);

    border: 1px solid rgba(0, 242, 254, 0.6);

    border-radius: 6px;

    margin-bottom: 15px;
}

.bio-scan-container {

    position: relative;

    width: 100%;
    height: 120px;

    background: rgba(4, 15, 12, 0.85);

    border: 1px solid rgba(0, 242, 254, 0.35);

    border-radius: 6px;

    overflow: hidden;

    margin-bottom: 30px;
}

@keyframes scan {

    0% {
        transform: translateY(-100%);
    }

    100% {
        transform: translateY(100%);
    }
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

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# HEADER
# ==============================================================================
st.markdown(
    '<h1 class="main-title">🩺 heydoctor.ai</h1>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="bio-scan-container">

<div class="scanner-text">

STATUS::ONLINE<br>
SMART_ROUTER::ACTIVE<br>
FAILOVER_ENGINE::READY<br>
AI_CLUSTER::CONNECTED

</div>

<div class="bio-scan-line"></div>

</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

if "api_health" not in st.session_state:
    st.session_state.api_health = {}

if "client_cache" not in st.session_state:
    st.session_state.client_cache = {}

# ==============================================================================
# LOAD API KEYS
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

        KEYS_POOL.append(
            st.secrets[key_name]
        )

if not KEYS_POOL:

    st.error("🚨 NO GEMINI API KEYS FOUND")
    st.stop()

# ==============================================================================
# API HEALTH REGISTRY
# ==============================================================================
for key in KEYS_POOL:

    if key not in st.session_state.api_health:

        st.session_state.api_health[key] = {

            "fails": 0,

            "cooldown_until": 0
        }

# ==============================================================================
# BEST KEY SELECTOR
# ==============================================================================
def get_best_available_key():

    current_time = time.time()

    available_keys = []

    for key in KEYS_POOL:

        data = st.session_state.api_health[key]

        if current_time >= data["cooldown_until"]:

            available_keys.append(key)

    if not available_keys:

        return None

    best_key = min(

        available_keys,

        key=lambda k:
        st.session_state.api_health[k]["fails"]
    )

    return best_key

# ==============================================================================
# FAIL HANDLER
# ==============================================================================
def mark_key_failed(key):

    data = st.session_state.api_health[key]

    data["fails"] += 1

    cooldown = min(

        30,

        3 * data["fails"]
    )

    data["cooldown_until"] = (

        time.time() + cooldown
    )

# ==============================================================================
# RESET HEALTH
# ==============================================================================
def reset_key_health(key):

    st.session_state.api_health[key]["fails"] = 0

# ==============================================================================
# SYSTEM PROMPT
# ==============================================================================
SYSTEM_PROMPT = """

You are Heydoctor.ai,
an advanced AI wellness assistant.

RULES:

1. Be short and helpful.

2. Use medical emojis.

3. Use headings and bullet points.

4. Never repeat greetings.

5. Analyze uploaded images.

6. Give safe wellness guidance only.

"""

# ==============================================================================
# IMAGE UPLOADER
# ==============================================================================
st.markdown(
    '<div class="section-header">🧬 BIO-SCAN IMAGE</div>',
    unsafe_allow_html=True
)

uploaded_image = st.file_uploader(

    "Upload symptom image",

    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:

    try:

        preview = Image.open(uploaded_image)

        st.image(
            preview,
            caption="✅ Image Uploaded",
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Image Error: {e}")

# ==============================================================================
# USER DATA
# ==============================================================================
col1, col2, col3 = st.columns(3)

with col1:

    gender = st.selectbox(

        "Gender",

        ["Male", "Female", "Other"]
    )

with col2:

    age = st.number_input(

        "Age",

        min_value=1,

        max_value=120,

        value=18
    )

with col3:

    blood_type = st.selectbox(

        "Blood",

        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

# ==============================================================================
# DISPLAY HISTORY
# ==============================================================================
for msg in st.session_state.messages_display:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ==============================================================================
# CHAT INPUT
# ==============================================================================
if user_query := st.chat_input(

    "Describe symptoms here..."
):

    meta_header = f"""

PATIENT DATA

Gender: {gender}

Age: {age}

Blood Type: {blood_type}

SYMPTOMS:

{user_query}

"""

    with st.chat_message("user"):

        st.markdown(user_query)

    st.session_state.messages_display.append({

        "role": "user",

        "content": user_query
    })

    # ==========================================================================
    # LOAD IMAGE
    # ==========================================================================
    uploaded_img_data = None

    if uploaded_image is not None:

        try:

            uploaded_img_data = Image.open(
                uploaded_image
            )

        except Exception:

            uploaded_img_data = None

    # ==========================================================================
    # HISTORY
    # ==========================================================================
    current_prompt_payload = []

    recent_history = st.session_state.chat_history[-6:]

    for item in recent_history:

        current_prompt_payload.append({

            "role": item["role"],

            "parts": item["parts"]
        })

    current_parts = [meta_header]

    if uploaded_img_data is not None:

        current_parts.append(
            uploaded_img_data
        )

    current_prompt_payload.append({

        "role": "user",

        "parts": current_parts
    })

    # ==========================================================================
    # AI RESPONSE
    # ==========================================================================
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        status_placeholder = st.empty()

        stream_success = False

        attempts = 0

        max_attempts = len(KEYS_POOL)

        while (

            not stream_success

            and

            attempts < max_attempts
        ):

            active_key = get_best_available_key()

            if active_key is None:

                st.error("""

🚨 ALL AI SERVERS ARE COOLING DOWN

Please wait 15-30 seconds.

""")

                break

            try:

                status_placeholder.markdown("""

<div style="color:#00F2FE;">

⚡ CONNECTING AI CLUSTER...<br>

🧠 PROCESSING MEDICAL ANALYSIS...

</div>

""", unsafe_allow_html=True)

                # ==============================================================
                # CLIENT CACHE
                # ==============================================================
                if (

                    active_key

                    not in

                    st.session_state.client_cache
                ):

                    st.session_state.client_cache[
                        active_key
                    ] = genai.Client(

                        api_key=active_key
                    )

                client = st.session_state.client_cache[
                    active_key
                ]

                # ==============================================================
                # GEMINI REQUEST
                # ==============================================================
                response_stream = client.models.generate_content_stream(

                    model="gemini-1.5-flash",

                    contents=current_prompt_payload,

                    config={

                        "system_instruction": SYSTEM_PROMPT,

                        "temperature": 0.7
                    }
                )

                full_response = ""

                for chunk in response_stream:

                    if chunk.text:

                        full_response += chunk.text

                        response_placeholder.markdown(f"""

<div class="hacker-response-container">

{full_response}▒

</div>

""", unsafe_allow_html=True)

                response_placeholder.markdown(f"""

<div class="hacker-response-container">

{full_response}

</div>

""", unsafe_allow_html=True)

                status_placeholder.empty()

                # ==============================================================
                # SAVE HISTORY
                # ==============================================================
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

                # ==============================================================
                # LIMIT MEMORY
                # ==============================================================
                MAX_HISTORY = 10

                if (

                    len(st.session_state.chat_history)

                    > MAX_HISTORY
                ):

                    st.session_state.chat_history = (

                        st.session_state.chat_history[
                            -MAX_HISTORY:
                        ]
                    )

                reset_key_health(active_key)

                stream_success = True

            except Exception as e:

                error_text = str(e).lower()

                mark_key_failed(active_key)

                attempts += 1

                status_placeholder.markdown(f"""

<div style="color:#FF4B4B;">

⚠️ FAILOVER ACTIVATED<br>

🔄 SWITCHING AI CORE...<br><br>

{str(e)}

</div>

""", unsafe_allow_html=True)

                time.sleep(1)

        # ==========================================================================
        # FINAL FAILSAFE
        # ==========================================================================
        if not stream_success:

            status_placeholder.empty()

            st.error("""

🚨 ENTERPRISE CHANNELS EXHAUSTED

Please wait 15 seconds
for hot-key cooldown refresh.

""")

    # ==========================================================================
    # IMAGE MEMORY CLEANUP
    # ==========================================================================
    if uploaded_img_data is not None:

        uploaded_img_data.close()
