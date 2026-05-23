# ==============================================================================
# HEYDOCTOR.AI FINAL STABLE VERSION
# FULLY FIXED • NO Pydantic Errors • SMART API ROTATION
# DEVELOPED BY PRATYUSH (X STUDIOS)
# ==============================================================================

import streamlit as st
import google.generativeai as genai
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
# STYLE
# ==============================================================================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {

    background: radial-gradient(circle at center, #061510 0%, #010403 100%);
    color: white;
    font-family: 'Courier New', monospace;
}

.main-title {

    font-size: 3rem;
    font-weight: 900;
    text-align: center;

    background: linear-gradient(
        90deg,
        #00F2FE,
        #4FACFE,
        #10B981
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-top: 20px;
}

.section-header {

    color: #10B981;

    font-size: 12px;

    font-weight: bold;

    letter-spacing: 2px;

    border-left: 3px solid #00F2FE;

    padding-left: 10px;

    margin-bottom: 10px;
}

.response-box {

    padding: 18px;

    background: rgba(5,14,11,0.85);

    border: 1px solid rgba(0,242,254,0.6);

    border-radius: 6px;

    margin-top: 10px;

    line-height: 1.7;
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

# ==============================================================================
# SESSION STATES
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_index" not in st.session_state:
    st.session_state.api_index = 0

# ==============================================================================
# API KEYS
# ==============================================================================
API_KEYS = []

key_names = [
    "GEMINI_API_KEY_A",
    "GEMINI_API_KEY_B",
    "GEMINI_API_KEY_C",
    "GEMINI_API_KEY_D",
    "GEMINI_API_KEY_E",
    "GEMINI_API_KEY"
]

for key in key_names:

    if key in st.secrets:

        value = st.secrets[key]

        if value:
            API_KEYS.append(value)

if len(API_KEYS) == 0:

    st.error("🚨 No API Keys Found")

    st.stop()

# ==============================================================================
# SMART KEY GETTER
# ==============================================================================
def get_next_api_key():

    index = st.session_state.api_index

    key = API_KEYS[index % len(API_KEYS)]

    st.session_state.api_index += 1

    return key

# ==============================================================================
# IMAGE UPLOAD
# ==============================================================================
st.markdown(
    '<div class="section-header">🧬 IMAGE SCANNER</div>',
    unsafe_allow_html=True
)

uploaded_image = st.file_uploader(
    "Upload medical image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="✅ Image Uploaded",
        use_container_width=True
    )

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

    blood = st.selectbox(
        "Blood",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

# ==============================================================================
# SHOW OLD CHATS
# ==============================================================================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ==============================================================================
# CHAT INPUT
# ==============================================================================
if prompt := st.chat_input("Describe symptoms here..."):

    # USER MESSAGE
    with st.chat_message("user"):

        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # ==========================================================================
    # CREATE MEDICAL PROMPT
    # ==========================================================================
    final_prompt = f"""

You are Heydoctor.ai.

Patient Information:

Gender: {gender}
Age: {age}
Blood Type: {blood}

Symptoms:

{prompt}

Instructions:

- Give short helpful answer
- Use medical emojis
- Use headings
- Be safe and professional

"""

    # ==========================================================================
    # AI RESPONSE
    # ==========================================================================
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        success = False

        attempts = 0

        max_attempts = len(API_KEYS)

        while not success and attempts < max_attempts:

            try:

                active_key = get_next_api_key()

                # ==============================================================
                # CONFIGURE GEMINI
                # ==============================================================
                genai.configure(
                    api_key=active_key
                )

                model = genai.GenerativeModel(
                    "gemini-1.5-flash"
                )

                # ==============================================================
                # IMAGE SUPPORT
                # ==============================================================
                if uploaded_image:

                    uploaded_image.seek(0)

                    image = Image.open(uploaded_image)

                    response = model.generate_content([
                        final_prompt,
                        image
                    ])

                else:

                    response = model.generate_content(
                        final_prompt
                    )

                full_response = response.text

                response_placeholder.markdown(
                    f"""
<div class="response-box">

{full_response}

</div>
""",
                    unsafe_allow_html=True
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

                success = True

            except Exception as e:

                attempts += 1

                time.sleep(1)

                if attempts >= max_attempts:

                    st.error(f"""

🚨 All AI servers are busy.

Please wait 15 seconds.

Error:
{str(e)}

""")
