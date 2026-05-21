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

# Secrets se key uthana (GitHub par koi key nahi hai)
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = None

# ==============================================================================
# # SYSTEM INSTRUCTION CONFIGURATION
# ==============================================================================
GOD_MODE_SYSTEM_INSTRUCTION = """
You are Heydoctor.ai, an elite-tier, enterprise-grade AI health concierge, lifestyle companion, and wellness advisor. 
"""

# ---- 4. CHAT INITIALIZATION WITH MEMORY ----
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = None

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = client.chats.create(
                model="gemini-2.5-flash",
                config={"system_instruction": GOD_MODE_SYSTEM_INSTRUCTION}
            )
            
    except Exception as e:
        st.error(f"Engine Initialization Error: {e}")
