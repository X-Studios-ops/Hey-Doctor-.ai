import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import datetime

# ============================================================================
# 1. ENTERPRISE LEVEL UI CONFIGURATION & THEME
# ============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Multimodal AI Health Concierge",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Stylesheet (Dark Teal & Clean Clinical Aesthetics)
st.markdown("""
    <style>
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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "wallet_tokens" not in st.session_state:
    st.session_state.wallet_tokens = 9  # Free Tier limit

if "premium_licensed" not in st.session_state:
    st.session_state.premium_licensed = True

# ============================================================================
# 3. CORE AI ENGINE & SECURITY GATEWAY (GEMINI 2.5 FLASH)
# ============================================================================
# CRITICAL: Replace with your working Google AI Studio API Key
GEMINI_API_KEY = "AIzaSyA_Eg-EhCaUrQF5e4c0f3M-Nge7ssNeQmE" 
client = genai.Client(api_key=GEMINI_API_KEY)

GOD_MODE_SYSTEM_INSTRUCTION = """
You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, and wellness advisor. You were engineered by your Master Developer Pratyush .

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
    # Injection of structural metadata to personalize diagnostics
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
            temperature=0.35, # Grounded, balanced, highly secure output
            max_output_tokens=1500
        )
    )
    return execution_response.text

# ============================================================================
# 4. SIDEBAR: MASTER CREATOR PROFILE & GRAPHICAL USER INTERFACE
# ============================================================================

# --- Section A: The Immortal Developer Branding ---
st.sidebar.markdown("""
    <div class="creator-premium-card">
        <span class="dev-badge">Chief Architect & Founder</span>
        <h2 style='margin:8px 0 2px 0; font-size:28px; font-weight:800; letter-spacing:-0.5px;'>Your Name</h2>
        <p style='margin:0; font-size:14px; opacity:0.85; font-family: monospace;'>Founder, Heydoctor.ai Ecosystem</p>
    </div>
""", unsafe_allow_html=True)

# Add your real social coordinates here
st.sidebar.markdown("""
🌐 **Developer Hub & Portfolio:**
- [✨ GitHub Profile](https://github.com/)
- [💼 LinkedIn Network](https://linkedin.com/)
""")
st.sidebar.markdown("---")

# --- Section B: Commercial Tokenization Logic ---
st.sidebar.subheader("💎 License & Token Gateway")
if st.session_state.premium_licensed:
    st.sidebar.success("👑 Premium Pro Status: Active Unlimited")
else:
    st.sidebar.warning(f"⏳ Free Access Tokens: {st.session_state.wallet_tokens} Remainder")
    if st.session_state.wallet_tokens <= 0:
        st.sidebar.markdown("""
            <div class="monetization-box">
                <p style='color:#7f6000; margin:0; font-weight:bold;'>⛔ Consultation Limit Reached!</p>
                <p style='font-size:13px; margin:6px 0; color:#555;'>Unlock infinite multimodal queries, deep medical document decoding, and prioritized lightning-fast engine computations.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("Upgrade to Premium Pro (₹99)"):
            st.session_state.premium_licensed = True
            st.session_state.wallet_tokens = 999999
            st.rerun()

st.sidebar.markdown("---")

# --- Section C: Contextual Smart Demographic Profile ---
st.sidebar.subheader("👤 Patient Demographics")
meta_age = st.sidebar.number_input("Patient Age", min_value=1, max_value=125, value=24)
meta_gender = st.sidebar.selectbox("Biological Gender", ["Male", "Female", "Other"])
meta_blood = st.sidebar.selectbox("Blood Group Matrix", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
current_metadata = {"age": meta_age, "gender": meta_gender, "blood": meta_blood}

st.sidebar.markdown("---")

# --- Section D: Ultra-Camera & Hardware Diagnostics Input ---
st.sidebar.subheader("📸 Hardware Scanner Suite")
capture_channel = st.sidebar.radio("Symptom Input Type:", ("Text-Only Stream", "Live Device Camera", "Local File Storage System"))

hardware_media_buffer = None
if capture_channel == "Live Device Camera":
    # Asks browser permission natively for camera 📸
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

# Clinical Redline Crisis Banner
st.markdown("""
    <div class="crisis-alert-banner">
        🚨 <b>CRITICAL DISPATCH PROTOCOL:</b> If you are facing life-threatening medical events (e.g., crushing chest pressure, sudden unyielding dyspnea, acute neurological weakness, or extreme traumatic hemorrhaging), abort digital screening immediately. Dial <b>102</b> or <b>112</b> instantly for paramedics. Heydoctor.ai is a non-clinical wellness companion system.
    </div>
""", unsafe_allow_html=True)
st.write("")

# Render Full Conversation Pipeline Natively
for chat_node in st.session_state.chat_history:
    with st.chat_message(chat_node["role"]):
        st.markdown(chat_node["content"])

# Main Input Stream Execution
# --- Chat Blocker Code by Pratyush ---
if not st.session_state.premium_licensed and len(st.session_state.chat_history) >= 9:
    st.error("🚨 Free Chat Limit Reached (Max 9 Chats)! Please upgrade to Premium Pro.")
    st.markdown("### 👑 Upgrade to Premium Pro")
    if st.button("Unlock Unlimited Chats (₹99)"):
        st.session_state.premium_licensed = True
        st.rerun()
    user_prompt = None
else:
    user_prompt = st.chat_input("Enter physical symptoms, medication queries...")

if user_prompt:
# Financial Verification Guardrail
    if not st.session_state.premium_licensed and st.session_state.wallet_tokens <= 0:
        st.error("🚨 Consultation streaming suspended. Free-tier token exhaustion detected. Please upgrade via the License Gateway in the sidebar.")
    else:
        # Commit User Command to State
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
                                
            # Compute AI Diagnostic
            with st.chat_message("assistant"):
                with st.spinner("⚡ Initializing Neural Diagnostic Stream..."):
                    try:
                        # Request execution from Gemini API Gateway
                        computed_insight = compute_health_insights(user_prompt, hardware_media_buffer, current_metadata)
                        st.markdown(computed_insight)
                        
                        # Log Assistant Node to History
                        st.session_state.chat_history.append({"role": "assistant", "content": computed_insight})
                        
                        # Deduct Commercial Token Allocation
                        if not st.session_state.premium_licensed:
                            st.session_state.wallet_tokens -= 1
                            st.rerun() # Refresh tokens dashboard
                            
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
