# ==============================================================================
# HEYDOCTOR.AI - ULTRA STABLE FINAL CORE
# ==============================================================================

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import time
import streamlit.components.v1 as components

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
# CUSTOM CSS
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
    background: linear-gradient(90deg,#00F2FE,#10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
}

.section-box {
    background: rgba(5,15,10,0.85);
    border: 1px solid rgba(0,255,200,0.2);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

div[data-testid="stChatMessage"] {
    background: rgba(0,0,0,0.25);
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# TITLE
# ==============================================================================
st.markdown(
    '<h1 class="main-title">🩺 Heydoctor.ai</h1>',
    unsafe_allow_html=True
)

# ==============================================================================
# API POOL
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
    if key_name in st.secrets:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL:
    st.error("No API Keys Found")
    st.stop()

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_index" not in st.session_state:
    st.session_state.api_index = 0

# ==============================================================================
# API ROTATION
# ==============================================================================
def get_next_api():
    key = KEYS_POOL[st.session_state.api_index]
    st.session_state.api_index = (
        st.session_state.api_index + 1
    ) % len(KEYS_POOL)
    return key

# ==============================================================================
# SYSTEM PROMPT
# ==============================================================================
SYSTEM_PROMPT = """
You are Heydoctor.ai.

Give advanced medical guidance in beautiful formatting.

Use emojis.

Use bullet points.

Do not say hello repeatedly.
"""

# ==============================================================================
# IMAGE UPLOAD
# ==============================================================================
st.markdown("## 🧬 Symptom Scanner")

uploaded_image = st.file_uploader(
    "Upload Medical Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, use_container_width=True)

# ==============================================================================
# USER DETAILS
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
        ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    )

# ==============================================================================
# BMI CALCULATOR
# ==============================================================================
st.markdown("---")
st.markdown("## ⚖️ BMI Calculator")

height = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=170.0
)

weight = st.number_input(
    "Weight (kg)",
    min_value=10.0,
    max_value=300.0,
    value=70.0
)

if st.button("Calculate BMI"):

    bmi = weight / ((height / 100) ** 2)

    st.success(f"✅ BMI = {bmi:.2f}")

    if bmi < 18.5:
        st.warning("⚠️ Underweight")

    elif bmi < 25:
        st.success("💚 Normal")

    elif bmi < 30:
        st.warning("⚠️ Overweight")

    else:
        st.error("🚨 Obese")

# ==============================================================================
# MEDICINE REMINDER
# ==============================================================================
st.markdown("---")
st.markdown("## 💊 Medicine Reminder")

medicine_name = st.text_input("Medicine Name")

reminder_time = st.time_input("Reminder Time")

if st.button("Save Reminder"):
    st.success(
        f"✅ Reminder Saved: {medicine_name} at {reminder_time}"
    )

# ==============================================================================
# ADSTERRA
# ==============================================================================
st.markdown("---")

components.html("""
<div style="display:flex;justify-content:center;">
<script type="text/javascript">
atOptions = {
    'key' : '4c180b2176e3a1a287de9e6b76879287',
    'format' : 'iframe',
    'height' : 90,
    'width' : 320,
    'params' : {}
};
</script>
<script type="text/javascript" src="//www.highperformanceformat.com/4c180b2176e3a1a287de9e6b76879287/invoke.js"></script>
</div>
""", height=100)

# ==============================================================================
# CHAT INPUT
# ==============================================================================
user_query = st.chat_input(
    "Describe symptoms here..."
)

# ==============================================================================
# AI ENGINE
# ==============================================================================
if user_query:

    with st.chat_message("user"):
        st.markdown(user_query)

    meta_prompt = f"""
Gender: {gender}
Age: {age}
Blood Type: {blood_type}

User Symptoms:
{user_query}
"""

    contents = []

    for item in st.session_state.chat_history:
        contents.append(
            types.Content(
                role=item["role"],
                parts=[
                    types.Part.from_text(
                        text=item["text"]
                    )
                ]
            )
        )

    current_parts = [
        types.Part.from_text(text=meta_prompt)
    ]

    if uploaded_image:
        image_data = Image.open(uploaded_image)
        current_parts.append(
            types.Part.from_image(image_data)
        )

    contents.append(
        types.Content(
            role="user",
            parts=current_parts
        )
    )

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        success = False

        for _ in range(len(KEYS_POOL)):

            try:

                api_key = get_next_api()

                client = genai.Client(
                    api_key=api_key
                )

                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.5
                    )
                )

                for chunk in response_stream:

                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(
                            full_response + "▌"
                        )

                response_placeholder.markdown(
                    full_response
                )

                success = True
                break

            except Exception as e:
                continue

        if not success:
            st.error("🚨 All API Keys Failed")

    st.session_state.chat_history.append({
        "role": "user",
        "text": meta_prompt
    })

    st.session_state.chat_history.append({
        "role": "model",
        "text": full_response
    })

    if len(st.session_state.chat_history) > 6:
        st.session_state.chat_history = (
            st.session_state.chat_history[-6:]
)    
