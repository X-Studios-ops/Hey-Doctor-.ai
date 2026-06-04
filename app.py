# ==============================================================================
# HEYDOCTOR.AI - ULTRA STABLE FINAL PRODUCTION CORE
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
    font-family: 'Poppins', sans-serif;
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

.glass-box {
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(0,255,200,0.15);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
}

.section-title {
    color: #10B981;
    font-size: 1.2rem;
    font-weight: bold;
}

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.05);
}

.stButton button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg,#00F2FE,#10B981);
    color: black;
    font-weight: bold;
    border: none;
}
/* 👇 BAS YAHAN SABSE NEECHE YEH NAYA CODE PASTE KAR DO */

section[data-testid="stSidebarCollapseButton"] button::after {
    content: " Shortcut";
    font-size: 14px;
    font-weight: bold;
    color: #10B981;
    position: relative;
    left: 5px;
    top: -2px;
    white-space: nowrap;
}

section[data-testid="stSidebarCollapseButton"] button:hover::after {
    color: #00F2FE;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# ONLY SIDEBAR ARROW TEXT & PAGE RENAMING SHORTCUT CODE
# ==============================================================================
st.markdown("""
<style>
/* 1. SIDEBAR ARROW KE SATH SHORTCUT TEXT */
button[data-testid="sidebar-toggle"]::after {
    content: " 📲 More Tools / Menu";
    font-size: 13px;
    font-weight: 800;
    color: #10B981;
    white-space: nowrap;
    position: absolute;
    left: 40px;
    top: 10px;
    background: rgba(16, 185, 129, 0.1);
    padding: 2px 10px;
    border-radius: 20px;
    border: 1px solid rgba(16, 185, 129, 0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; transform: scale(1.02); }
    100% { opacity: 0.7; }
}

/* Multi-page CSS Selector (Super Strong Match) */
a[href*="app"] span { display: none !important; }
a[href*="app"]::before { content: "🧠 Main AI" !important; font-weight: bold; color: white; }

a[href*="BMI"] span { display: none !important; }
a[href*="BMI"]::before { content: "⚖️ BMI Calculator" !important; font-weight: bold; color: white; }

/* Naya Strong Selector: Medicine ya Timer kuch bhi mile toh replace karega */
a[href*="med"] span, a[href*="Med"] span, a[href*="timer"] span { display: none !important; }
a[href*="med"]::before, a[href*="Med"]::before, a[href*="timer"]::before { content: "⏰ Medicine Timer" !important; font-weight: bold; color: white; }
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
# PRODUCT HUNT BADGE
# ==============================================================================
components.html("""
<div style="display:flex;justify-content:center;margin-bottom:15px;">

<a href="https://www.producthunt.com/products/hey-doctor-ai"
target="_blank">

<img
src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1156270&theme=dark"
width="250"
/>

</a>

</div>
""", height=80)
# ==============================================================================
# API KEYS POOL FETCHING
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
        # Secret value cleanly extract kar rhe hain
        val = st.secrets[key_name]
        if val and str(val).strip():
            KEYS_POOL.append(str(val).strip())

if not KEYS_POOL:
    st.error("🚨 Configuration Error: No API Keys found in Streamlit Secrets Dashboard. Please add them in App Settings.")
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
    st.session_state.api_index = (st.session_state.api_index + 1) % len(KEYS_POOL)
    return key
# ==============================================================================
# SYSTEM PROMPT (STRICT IDENTITY FORCE)
# ==============================================================================
SYSTEM_PROMPT = """
You are Heydoctor.ai, an advanced autonomous medical and health companion system.

CRITICAL IDENTITY RULES:
1. Your creator/developer/founder is Pratyush. If anyone asks "Who created you?", "Who is your developer?", or "Who made you?", you must proudly answer that you were engineered and created by Pratyush (Founder of Heydoctor.ai Ecosystem).
2. DO NOT mention Google, OpenAI, or any other company as your creator. You are an independent neural architecture built by Pratyush.
3. Maintain this persona strictly throughout the conversation.

MEDICAL RULES:
- Give professional medical guidance with a precision-driven wellness approach.
- Always use emojis, clear headings, and bullet points to keep the response beautiful and readable.
"""


# ==============================================================================
# IMAGE UPLOAD
# ==============================================================================
st.markdown("## 🧬 Diagnostic Stream")

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
# FIRST ADSTERRA AD
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

<script type="text/javascript"
src="//www.highperformanceformat.com/4c180b2176e3a1a287de9e6b76879287/invoke.js">
</script>

</div>
""", height=100)

# ⭐ AI Reality Check

st.markdown("---")
st.markdown("## ⭐ AI Reality Check")
st.caption("Get a brutally honest review of your lifestyle 😅")

sleep_hours = st.slider("😴 Sleep Hours Per Day", 0, 12, 7)
water_glasses = st.slider("💧 Glasses of Water Per Day", 0, 15, 8)
exercise_days = st.slider("🏃 Exercise Days Per Week", 0, 7, 3)
screen_hours = st.slider("📱 Screen Time (Hours/Day)", 0, 15, 5)
junk_food = st.slider("🍔 Junk Food Meals Per Week", 0, 20, 3)

if st.button("🔍 Run Reality Check"):

```
score = 100

if sleep_hours < 7:
    score -= (7 - sleep_hours) * 5

if water_glasses < 8:
    score -= (8 - water_glasses) * 2

if exercise_days < 3:
    score -= (3 - exercise_days) * 5

if screen_hours > 6:
    score -= (screen_hours - 6) * 3

if junk_food > 4:
    score -= (junk_food - 4) * 2

score = max(0, min(100, score))

st.success(f"🎯 Reality Score: {score}/100")

if score >= 85:
    st.info("🟢 Your lifestyle is actually impressive. Keep it up!")
elif score >= 70:
    st.info("🟡 Not bad, but your body has a few complaints.")
elif score >= 50:
    st.warning("🟠 Your body is working overtime to compensate for your habits. 😭")
elif score >= 30:
    st.warning("🔴 Reality Check: Your lifestyle choices are winning against your health.")
else:
    st.error("💀 Emergency Reality Check: Your body deserves an apology.")
```


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

    st.success(f"✅ Your BMI = {bmi:.2f}")

    if bmi < 18.5:
        st.warning("⚠️ Underweight")

    elif bmi < 25:
        st.success("💚 Normal Weight")

    elif bmi < 30:
        st.warning("⚠️ Overweight")

    else:
        st.error("🚨 Obese")
#==============================================================================
st.markdown("""
## 🚀 Coming Soon

Medicine Reminder feature is under development and will be available soon.
""")
# ==============================================================================
# SECOND ADSTERRA AD
# ==============================================================================
st.markdown("---")

components.html("""
<div style="display:flex;justify-content:center;">

<script type="text/javascript">
atOptions = {
    'key' : '4c180b2176e3a1a287de9e6b76879287',
    'format' : 'iframe',
    'height' : 50,
    'width' : 320,
    'params' : {}
};
</script>

<script type="text/javascript"
src="//www.highperformanceformat.com/4c180b2176e3a1a287de9e6b76879287/invoke.js">
</script>

</div>
""", height=60)

# ==============================================================================
# 1. PURANE MESSAGES DIKHANA (Yeh page rerun hone par history wapas layega)
# ==============================================================================
for message in st.session_state.chat_history:
    # Gemini API 'model' role use karta hai, par Streamlit UI 'assistant' mangta hai
    display_role = "assistant" if message["role"] == "model" else message["role"]
    
    with st.chat_message(display_role):
        st.markdown(message["text"])

# ==============================================================================
# 2. USER SE NAYA INPUT LENA
# ==============================================================================
user_query = st.chat_input("What are your symptoms?")
# ==============================================================================
# AI ENGINE
# ==============================================================================
if user_query:

    # 1. User ka message UI pe dikhao
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. PATIENT DETAILS KO SYSTEM PROMPT MEIN DAAL DIYA (Har message me nahi jayega)
    dynamic_system_instruction = SYSTEM_PROMPT + f"""
    \nCURRENT PATIENT PROFILE:
    - Gender: {gender}
    - Age: {age}
    - Blood Type: {blood_type}
    
    (Note: Do not greet the patient repeatedly in every response. Just answer their current query directly and naturally.)
    """

    contents = []

    # History nikal rahe hain
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

    # Ab meta_prompt ki jagah seedha user_query bhej rahe hain
    current_parts = [
        types.Part.from_text(text=user_query)
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
                client = genai.Client(api_key=api_key)

                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=dynamic_system_instruction, # Yahan naya instruction pass kiya
                        temperature=0.5
                    )
                )

                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                success = True
                break

            except Exception:
                continue

        if not success:
            st.error("🚨 All API Keys Failed")

    # History mein ab sirf user ka exact message save hoga (bina kisi meta tag ke)
    st.session_state.chat_history.append({
        "role": "user",
        "text": user_query 
    })

    st.session_state.chat_history.append({
        "role": "model",
        "text": full_response
    })

  # ==============================================================================
    # 🛑 SAFE HISTORY LIMIT (PREVENTS CRASH & TOKEN OVERLOAD)
    # ==============================================================================
    # Sirf last 30 messages save rakhega
    if len(st.session_state.chat_history) > 30:
        st.session_state.chat_history = (
            st.session_state.chat_history[-30:]
        )
