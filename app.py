import streamlit as st
import google.genai as genai
import time

# ==============================================================================
# 1. PAGE SETUP & MULTICOLOR NEON INJECTOR
# ==============================================================================
st.set_page_config(
    page_title="Heydoctor.ai | Advanced Medical Core",
    page_icon="🩺",
    layout="centered"
)

# Heavy-duty custom CSS override to enforce neon multi-color highlights and animations
st.markdown("""
    <style>
    /* Full Application Metallic Canvas */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #061510 0%, #010403 100%) !important;
        color: #F1F5F9 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Multicolor Title (Cyan to Green Gradient) */
    .main-title {
        font-size: 3.6rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 40%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 15px;
        margin-bottom: 2px;
        letter-spacing: 2px;
        filter: drop-shadow(0px 0px 20px rgba(0, 242, 254, 0.4));
    }
    
    /* Advanced Glowing Shield Badge */
    .premium-badge-container {
        text-align: center;
        margin-bottom: 30px;
    }
    .premium-badge {
        background: rgba(0, 242, 254, 0.05);
        border: 1px dashed #00F2FE;
        color: #00F2FE;
        padding: 6px 18px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 0px 15px rgba(0, 242, 254, 0.2);
    }

    /* 🦾 ADVANCED BIO-SCANNER ANIMATION */
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    .bio-scan-container {
        position: relative;
        width: 100%;
        height: 120px;
        background: rgba(4, 15, 12, 0.7);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.1);
    }
    .bio-scan-line {
        position: absolute;
        width: 100%;
        height: 2px;
        background: #00F2FE;
        opacity: 0.8;
        box-shadow: 0 0 10px #00F2FE;
        animation: scan 1.5s linear infinite;
    }
    .scanner-text {
        position: absolute;
        top: 10px;
        left: 10px;
        color: #00F2FE;
        font-size: 10px;
        opacity: 0.6;
    }
    
    /* Structured Section Group Label */
    .section-header {
        color: #10B981;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
        text-transform: uppercase;
        border-left: 3px solid #00F2FE;
        padding-left: 8px;
    }

    /* Photo Scan Drop-Zone Custom Overrides */
    div[data-testid="stFileUploader"] {
        border: 1px solid #00F2FE !important;
        background-color: rgba(4, 15, 12, 0.7) !important;
        border-radius: 4px !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.1) !important;
    }

    /* Input Matrix Component Custom Borders */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(2, 6, 5, 0.95) !important;
        border: 1px solid #10B981 !important;
        border-radius: 4px !important;
    }
    
    /* Output Terminal Panels */
    .hacker-response-container {
        color: #F8FAFC;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        padding: 15px;
        background: rgba(5, 14, 11, 0.8);
        border: 1px solid #00F2FE;
        border-radius: 4px;
        margin-bottom: 12px;
        box-shadow: inset 0 0 15px rgba(0, 242, 254, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Top Brand Presentation
st.markdown('<h1 class="main-title">🩺 heydoctor.ai</h1>', unsafe_allow_html=True)
st.markdown('<div class="premium-badge-container"><div class="premium-badge">⚡ MULTI-ENGINE ENTERPRISE MODE: ACTIVE</div></div>', unsafe_allow_html=True)

# 🦾 Animation Block
st.markdown("""
    <div class="bio-scan-container">
        <div class="scanner-text">
            STATUS::LIVE<br>
            BIO_SCAN::ACTIVE<br>
            QUOTA::GEMINI_STABLE_FRAME
        </div>
        <div class="bio-scan-line"></div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SECURE API CLUSTER ROUTING & SELF-HEALING SYSTEM
# ==============================================================================
KEYS_POOL = []
for key_name in ["GEMINI_API_KEY_A", "GEMINI_API_KEY_B", "GEMINI_API_KEY_C"]:
    if hasattr(st, "secrets") and key_name in st.secrets and st.secrets[key_name]:
        KEYS_POOL.append(st.secrets[key_name])

if not KEYS_POOL and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    KEYS_POOL.append(st.secrets["GEMINI_API_KEY"])

if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# 🌟 Strict No Greeting / Emojis Setup
GOD_MODE_SYSTEM_INSTRUCTION = (
    "You are Heydoctor.ai, an elite-tier AI health concierge and expert wellness companion. "
    "CRITICAL RULE: Never say 'Hello again', 'Hi again', 'Welcome back', or repeat greetings in your replies. "
    "Do not acknowledge that this is a repeated conversation. Jump straight into giving the medical analysis. "
    "1. Always use lots
