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
/* Sidebar toggle button ke saath text chipka do */
section[data-testid="stSidebarCollapseButton"] button::after {
    content: " | 💊 Medicine Info";
    font-size: 14px;
    font-weight: 800;
    color: #10B981;
    margin-left: 10px;
    background: rgba(16, 185, 129, 0.1);
    padding: 2px 10px;
    border-radius: 20px;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

/* Sidebar khulne par icon aur text saaf dikhe */
button[data-testid="sidebar-toggle"] {
    display: flex;
    align-items: center;
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
1. Your creator/developer/founder is Pratyush Ranjan Roul. If anyone asks "Who created you?", "Who is your developer?", or "Who made you?", you must proudly answer that you were engineered and created by Pratyush (Founder of Heydoctor.ai Ecosystem).
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

st.warning("""
🚧 **Medical Image Analysis - Coming Soon**

Our advanced AI diagnostic vision system is currently being upgraded.

Features coming soon:
- Skin Condition Analysis
- Prescription Reading
- Medical Report Interpretation
- Eye & Dental Screening

Stay tuned for the next update.
""")

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

# Everything below this line must be indented properly
if st.button("🔍 Run Reality Check"):
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

# ==============================================================================
# MEDICINE INFO TOOL - SIDEBAR INTEGRATION
# ==============================================================================

with st.sidebar:
    st.markdown("---")
    st.markdown("### 💊 Medicine Info Search")
    
    # Text input for medicine name
    med_query = st.text_input("Enter Medicine Name:", placeholder="e.g. Paracetamol, Ibuprofen")
    
    # Button to trigger search
    if st.button("Search Information", key="med_search_btn"):
        if med_query:
            with st.spinner("Heydoctor.ai is querying neural database..."):
                try:
                    # Current API Key rotation logic
                    api_key = get_next_api()
                    client = genai.Client(api_key=api_key)
                    
                    # Prompt defined for structured output
                    med_prompt = f"""
                    You are Heydoctor.ai medical assistant. Provide a structured,
                    concise medical profile for: '{med_query}'.
                    
                    Format your response exactly as:
                    **1. PRIMARY USES:**
                    - [Use 1]
                    - [Use 2]
                    
                    **2. COMMON SIDE EFFECTS:**
                    - [Side Effect 1]
                    - [Side Effect 2]
                    
                    **3. KEY PRECAUTIONS:**
                    - [Precaution 1]
                    
                    **4. DOCTOR'S WARNING:**
                    [Keep this bold and critical]
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=med_prompt
                    )
                    
                    # Show results in a beautiful box
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # Disclaimer
                    st.markdown("""
                    <div style='font-size:10px; color:#666; margin-top:20px; text-align:center; padding:10px; border: 1px solid #333; border-radius:5px;'>
                    <strong>CRITICAL DISCLAIMER:</strong> This is an AI-generated health insight. It is NOT medical advice. Always verify with a licensed doctor.
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("AI service could not process this request. Please check your API keys.")
        else:
            st.warning("Please enter a medicine name first.")
#==============================================================================
st.markdown("""
## 🚀 Coming Soon

Medicine Reminder feature is under development and will be available soon.
""")

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

    # 🔥 Key health tracking (important)
    key_fail_count = {i: 0 for i in range(len(KEYS_POOL))}

    def get_best_key():
        # least failed key choose karo
        best_index = min(key_fail_count, key=key_fail_count.get)
        return best_index

    for attempt in range(len(KEYS_POOL)):

        key_index = get_best_key()
        api_key = KEYS_POOL[key_index]

        try:
            client = genai.Client(api_key=api_key)

            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=dynamic_system_instruction,
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

        except Exception as e:

            error_text = str(e)
            key_fail_count[key_index] += 1

            # 🔴 mark bad key
            st.warning(f"⚠️ Key {key_index+1} failed")

            # 🔥 Smart delay system
            if "503" in error_text:
                time.sleep(2)

            elif "429" in error_text:
                time.sleep(6)

            else:
                time.sleep(1)

            continue

    # ❌ Final fallback system
    if not success:
        try:
            st.warning("🔁 Switching to fallback model...")

            client = genai.Client(api_key=KEYS_POOL[0])

            response = client.models.generate_content(
                model="gemini-1.5-flash",  # fallback lighter model
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=dynamic_system_instruction
                )
            )

            full_response = response.text
            response_placeholder.markdown(full_response)
            success = True

        except Exception as e:
            response_placeholder.error("🚨 All systems failed. Try again later.")
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
    if len(st.session_state.chat_history) > 12:
        st.session_state.chat_history = (
            st.session_state.chat_history[-12:]
        )
