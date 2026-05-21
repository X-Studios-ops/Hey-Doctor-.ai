import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import datetime

# ============================================================================
# 1. ENTERPRISE LEVEL UI CONFIGURATION & THEME (CLEAN & MINIMAL)
# ============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Multimodal AI Health Concierge",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS - Streamlit ke default headers, footers aur menus ko completely hide karne ke liye
st.markdown("""
    <style>
    /* Streamlit ke faltu elements ko hide karne ke liye */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Global Background aur Professional Colors */
    .stApp { background-color: #f4f7f6; }
    .main-header {
        color: #004d40;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 42px;
        margin-bottom: 5px;
    }
    .creator-premium-card {
        background: linear-gradient(135deg, #004d40 0%, #00796b 100%);
        color: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 77, 64, 0.15);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .monetization-box {
        background-color: #fffde7;
        border: 1px solid #fbc02d;
        padding: 15px;
        border-radius: 12px;
        margin-top: 15px;
    }
    .crisis-alert-banner {
        background-color: #ffebee;
        border-left: 6px solid #d32f2f;
        padding: 18px;
        border-radius: 10px;
        color: #c62828;
        font-family: sans-serif;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .dev-badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. STATE MANAGEMENT & COMMERCIAL GATEWAYS
# ============================================================================
today_date = str(datetime.date.today())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "last_chat_date" not in st.session_state or st.session_state.last_chat_date != today_date:
    st.session_state.last_chat_date = today_date
    st.session_state.user_daily_tokens = 9  # Har naye din 9 fresh tokens

if "premium_licensed" not in st.session_state:
    st.session_state.premium_licensed = True

# ==============================================================================
# # 3. CORE AI ENGINE & SECURITY GATEWAY (GEMINI 2.5 FLASH)
# ==============================================================================

# Secrets se key uthana
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = None

# ---- 4. CHAT INITIALIZATION WITH MEMORY ----
if GEMINI_API_KEY:
    try:
        # Client aur Model setup
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Agar chat session pehle se nahi bana hai toh naya banao
        if "chat_session" not in st.session_state:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=GOD_MODE_SYSTEM_INSTRUCTION
            )
            st.session_state.chat_session = model.start_chat(history=[])
            
    except Exception as e:
        st.error(f"Engine Initialization Error: {e}")
else:
    st.error("API Key nahi mili! Please Streamlit Secrets check karein.")

# ---- 5. SCREEN PAR PURANI CHAT HISTORY DIKHANA ----
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

# ---- 6. USER KA NEW INPUT HANDLE KARNA ----
if user_query := st.chat_input("Enter physical symptoms, medication queries..."):
    # User ka message screen par dikhao
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # AI se response lo (Poori history automatic piche se jayegi)
    if "chat_session" in st.session_state:
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(user_query)
                st.markdown(response.text)
            except Exception as e:
                # Agar ab koi error aayega toh asli wajah dikhegi, ganda static error nahi!
                st.error(f"Data Stream Interrupted: {e}")

# Agar Secrets mein key mil gayi hai toh client shuru hoga
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    st.error("API Key nahi mili! Please Streamlit Secrets check karein.")
GOD_MODE_SYSTEM_INSTRUCTION = """
You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, and wellness advisor. You were engineered by your Master Developer Pratyush.

OPERATIONAL PROTOCOLS:
1. MULTILINGUAL AUTO-ADAPTATION: Analyze the user's language instantly. If they type in Hinglish, reply in empathetic, natural, fluent Hinglish. If they use English, Hindi script, Marathi, Tamil, or Bengali, respond natively in that exact language and script. Matching the user's cultural context is non-negotiable.
2. MEDICAL ACCURACY & CLINICAL SAFETY: You are an advisory AI, not a practicing doctor. For general symptoms, structure your answers flawlessly using these clean headers:
   - **🔍 Symptom Breakdown / लक्षण विश्लेषण**
   - **💡 Potential Friendly Insights / संभावित कारण**
   - **🌱 Actionable Wellness Blueprint & Home Tips / घरेलू उपचार और उपाय**
   - **🩺 Medical Consult Recommendation / डॉक्टर की सलाह कब लें**
3. CRITICAL CRISIS OVERRIDE: If the input contains signs of emergency (e.g., crushing chest pain, extreme dyspnea, heavy arterial bleeding, stroke signs), you must immediately trigger a high-priority emergency warning phrase.
4. IMAGE ANALYSIS: When an image is attached, dynamically evaluate if it's a diagnostic report, pill bottle, or a dermatological issue (rash/burn/cut). Explain the visual data without using scary medical terminal jargon. Always tell them to cross-verify reports with real clinicians.
"""

def compute_health_insights(prompt_text, file_buffer, user_metadata):
    # Demographics data ko system injection ke sath jodna
    structured_payload = [
        f"[SYSTEM DATA - CLINICAL CONTEXT]\n"
        f"Patient Profile -> Age: {user_metadata['age']}, Biological Sex: {user_metadata['gender']}, Blood Phenotype: {user_metadata['blood']}\n"
        f"[USER COMMAND]\n{prompt_text}"
    ]
    
    if file_buffer:
        structured_payload.append(Image.open(file_buffer))
        
    execution_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=structured_payload,
        config=types.GenerateContentConfig(
            system_instruction=GOD_MODE_SYSTEM_INSTRUCTION,
            temperature=0.35, # Secure aur grounded outputs ke liye
            max_output_tokens=1500
        )
    )
    return execution_response.text

# ============================================================================
# 4. SIDEBAR: MASTER CREATOR PROFILE & GRAPHICAL USER INTERFACE
# ============================================================================

# --- Section A: Chief Architect Profile (Pratyush Branding) ---
st.sidebar.markdown("""
    <div class="creator-premium-card">
        <span class="dev-badge">Chief Architect & Founder</span>
        <h2 style='margin:8px 0 2px 0; font-size:28px; font-weight:800; letter-spacing:-0.5px;'>Pratyush</h2>
        <p style='margin:0; font-size:14px; opacity:0.85; font-family: monospace;'>Founder, Heydoctor.ai Ecosystem</p>
    </div>
""", unsafe_allow_html=True)

# Apne links tu yahan badal sakta hai baad mein
st.sidebar.markdown("""
🌐 **Developer Hub & Portfolio:**
- [✨ GitHub Profile](https://github.com/)
- [💼 LinkedIn Network](https://linkedin.com/)
""")
st.sidebar.markdown("---")

# --- Section B: License Status ---
st.sidebar.subheader("💎 License & Token Gateway")
if st.session_state.premium_licensed:
    st.sidebar.success("👑 Premium Pro Status: Active Unlimited")

st.sidebar.markdown("---")

# --- Section C: Patient Demographics Form ---
st.sidebar.subheader("👤 Patient Demographics")
meta_age = st.sidebar.number_input("Patient Age", min_value=1, max_value=125, value=24)
meta_gender = st.sidebar.selectbox("Biological Gender", ["Male", "Female", "Other"])
meta_blood = st.sidebar.selectbox("Blood Group Matrix", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
current_metadata = {"age": meta_age, "gender": meta_gender, "blood": meta_blood}

st.sidebar.markdown("---")

# --- Section D: Multimodal Hardware Scanner Suite (Camera & Files) ---
st.sidebar.subheader("📸 Hardware Scanner Suite")
capture_channel = st.sidebar.radio("Symptom Input Type:", ("Text-Only Stream", "Live Device Camera", "Local File Storage System"))

hardware_media_buffer = None
if capture_channel == "Live Device Camera":
    # Natively asks for browser camera access 📸
    hardware_media_buffer = st.sidebar.camera_input("Position Symptom/Report in Frame")
elif capture_channel == "Local File Storage System":
    hardware_media_buffer = st.sidebar.file_uploader("Upload Medical Image Asset", type=["png", "jpg", "jpeg"])

if hardware_media_buffer:
    st.sidebar.image(hardware_media_buffer, caption="Asset Staged for Diagnostic Stream", use_column_width=True)

# ============================================================================
# 5. CORE INTERFACE & DIAGNOSTIC STREAM RUNTIME
# ============================================================================
st.markdown("<h1 class='main-header'>🩺 Heydoctor.ai</h1>", unsafe_allow_html=True)
st.write(f"**Next-Gen Autonomous Multimodal Health Companion.** Engineered for precision diagnostics assistance.")

# Safety Crisis Banner
st.markdown("""
    <div class="crisis-alert-banner">
        🚨 <b>CRITICAL DISPATCH PROTOCOL:</b> If you are facing life-threatening medical events (e.g., crushing chest pressure, sudden unyielding dyspnea, acute neurological weakness, or extreme traumatic hemorrhaging), abort digital screening immediately. Dial <b>102</b> or <b>112</b> instantly for paramedics. Heydoctor.ai is a non-clinical wellness companion system.
    </div>
""", unsafe_allow_html=True)
st.write("")

# Dynamic Conversation Render Pipeline
for chat_node in st.session_state.chat_history:
    with st.chat_message(chat_node["role"]):
        st.markdown(chat_node["content"])

# Chat box input
user_prompt = st.chat_input("Enter physical symptoms, medication queries...")

if user_prompt:
    # Append user chat to history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
                            
        # Core execution loop
        with st.chat_message("assistant"):
            with st.spinner("⚡ Initializing Neural Diagnostic Stream..."):
                try:
                    # Gemini API hit karna
                    computed_insight = compute_health_insights(user_prompt, hardware_media_buffer, current_metadata)
                    st.markdown(computed_insight)
                    st.session_state.chat_history.append({"role": "assistant", "content": computed_insight})
                        
                except Exception as critical_fault_log:
                    st.error("Data Stream Interrupted: Please verify your Gemini API key activation parameter.")
                    st.sidebar.error(f"System Debug Fault: {critical_fault_log}")

# ============================================================================
# 6. SYSTEM ENTERPRISE FOOTER
# ============================================================================
st.markdown("---")
footer_grid = st.columns([4, 1])
with footer_grid[0]:
    st.markdown(f"© {datetime.datetime.now().year} **Heydoctor.ai** Ecosystem | Advanced Neural Health Advisor Architecture. All Rights Reserved.")
with footer_grid[1]:
    st.markdown(f"<p style='text-align:right; font-family:monospace; color:#777;'><b>Core Version:</b> 3.0.0-PRO</p>", unsafe_allow_html=True)
