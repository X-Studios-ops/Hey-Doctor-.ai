import streamlit as st
import google.generativeai as genai
import json
import re

# --- STEP 1: PAGE CONFIGURATION & SECURE API SETUP ---
st.set_page_config(page_title="Hey Doctor | Premium AI Health Analyzer", layout="wide", page_icon="🤍")

# Initialize Gemini securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Bhai, Streamlit secrets mein 'GEMINI_API_KEY' nahi mili! Dashboard setting check karo. 😅")

# --- STEP 2: PREMIUM WHITE UI CSS INJECTION (Tailwind & Fonts) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    
    <style>
        /* Global Reset to Premium White Design */
        .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f8fafc !important;
        }
        h1, h2, h3, p, label {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        /* Custom styling for standard Streamlit textareas to fit premium theme */
        .stTextArea textarea {
            background-color: #f1f5f9 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            color: #1e293b !important;
        }
        .stTextArea textarea:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 1px #6366f1 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER NAVIGATION ARCHITECTURE ---
st.markdown("""
    <div class="flex items-center justify-between bg-white/80 backdrop-blur-md border-b border-slate-100 p-4 rounded-2xl mb-8 shadow-sm">
        <div class="flex items-center gap-2">
            <span class="text-xl font-bold tracking-tight bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                🤍 Hey Doctor
            </span>
            <span class="bg-indigo-50 text-indigo-600 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-indigo-100">
                Premium AI Engine
            </span>
        </div>
        <div class="text-[11px] text-slate-400 font-medium bg-slate-50 px-3 py-1 rounded-md border border-slate-100">
            🔒 Secure Server-Side Mode Active
        </div>
    </div>
    
    <div class="text-center max-w-2xl mx-auto mb-12">
        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 mb-2">Advanced Structural Health Diagnostics</h1>
        <p class="text-sm text-slate-500">Deep-scan specialized biomarkers separately with independent performance metrics & synchronized AI models.</p>
    </div>
""", unsafe_allow_html=True)

# --- MASTER ANALYTICS GRID GENERATOR ---
col1, col2 = st.columns(2, gap="large")

# Helper function to extract JSON from Gemini markdown responses safely
def clean_and_parse_json(raw_text):
    try:
        clean_text = re.sub(r"```json\s*|```", "", raw_text).strip()
        return json.loads(clean_text)
    except Exception:
        return None

# =====================================================================
# SECTION 1: SEPARATE NAIL HEALTH ANALYSIS
# =====================================================================
with col1:
    st.markdown("""
        <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-xl bg-rose-50 flex items-center justify-center text-rose-500 font-bold text-lg border border-rose-100 shadow-sm">💅</div>
            <div>
                <h2 class="text-lg font-bold text-slate-900 mb-0">Nail Health Analysis</h2>
                <p class="text-[11px] text-slate-400">Scans vertical ridges, structural contours, and lunula variants</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    nail_query = st.text_area(
        "Upload Visual Sample or Describe Symptoms",
        placeholder="Describe discoloration, brittleness, horizontal lines, or paste data context...",
        key="nail_input",
        label_visibility="collapsed"
    )
    
    if st.button("Run Nail Diagnostics ✨", key="nail_btn", use_container_width=True):
        if not nail_query.strip():
            st.warning("Bhai, pehle details toh dalo! 😅")
        else:
            with st.spinner("Analyzing structural matrices... 🧠"):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"""
                    You are an expert AI Dermatologist specializing in Nail Health Diagnostics.
                    Analyze this symptom context: "{nail_query}".
                    You must return strictly a valid JSON object matching this structure exactly without any extra conversation code:
                    {{
                        "score": (integer between 0 and 100 where 100 means flawless structural integrity),
                        "status": "Short status title",
                        "biomarkers": "Detailed explanation of detected indicators",
                        "recommendations": "Actionable nutritional or lifestyle advice"
                    }}
                    """
                    response = model.generate_content(prompt)
                    data = clean_and_parse_json(response.text)
                    
                    if data:
                        # RENDER ANIMATED SVG METER AND CONTENT
                        st.components.v1.html(f"""
                            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
                            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
                            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-5" style="font-family: 'Plus Jakarta Sans', sans-serif;">
                                <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-100">
                                    <div class="relative w-16 h-16 flex items-center justify-center flex-shrink-0">
                                        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                                            <circle cx="50" cy="50" r="40" stroke="#f1f5f9" stroke-width="8" fill="transparent" />
                                            <circle id="gauge" cx="50" cy="50" r="40" stroke="#f43f5e" stroke-width="8" fill="transparent" 
                                                    stroke-dasharray="251.2" stroke-dashoffset="251.2" style="transition: stroke-dashoffset 1.8s cubic-bezier(0.34, 1.56, 0.64, 1);" />
                                        </svg>
                                        <span id="scoreText" class="absolute text-sm font-bold text-slate-800">0%</span>
                                    </div>
                                    <div>
                                        <div class="text-[10px] uppercase font-bold tracking-wider text-rose-500">Nail Integrity Score</div>
                                        <h4 class="text-sm font-bold text-slate-800">{data['status']}</h4>
                                    </div>
                                </div>
                                <div class="space-y-3 text-xs text-slate-600">
                                    <div class="bg-rose-50/40 border border-rose-100/50 p-3 rounded-lg">
                                        <strong class="text-rose-700 block mb-1">📋 Detected Biomarkers:</strong>
                                        <p>{data['biomarkers']}</p>
                                    </div>
                                    <div class="p-1">
                                        <strong class="text-slate-800 block mb-1">💡 Recommendations:</strong>
                                        <p class="text-slate-500">{data['recommendations']}</p>
                                    </div>
                                </div>
                            </div>
                            <script>
                                setTimeout(() => {{
                                    const score = {data['score']};
                                    const circumference = 251.2;
                                    document.getElementById('gauge').style.strokeDashoffset = circumference - (circumference * score) / 100;
                                    let current = 0;
                                    const interval = setInterval(() => {{
                                        if (current >= score) {{
                                            clearInterval(interval);
                                        }} else {{
                                            current++;
                                            document.getElementById('scoreText').innerText = current + '%';
                                        }}
                                    }}, 15);
                                }}, 100);
                            </script>
                        """, height=320)
                    else:
                        st.error("Engine standard outputs detect nahi kar paya. Please try again!")
                except Exception as e:
                    st.error(f"Error connecting to backend model: {str(e)}")

# =====================================================================
# SECTION 2: SEPARATE VITAMIN DEFICIENCY ANALYSIS
# =====================================================================
with col2:
    st.markdown("""
        <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-500 font-bold text-lg border border-indigo-100 shadow-sm">💊</div>
            <div>
                <h2 class="text-lg font-bold text-slate-900 mb-0">Vitamin Deficiency Analysis</h2>
                <p class="text-[11px] text-slate-400">Evaluates metabolic synchronization, systemic fatigue triggers, and dermal indicators</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    vitamin_query = st.text_area(
        "Input Primary Micro-symptoms",
        placeholder="Enter symptoms like constant fatigue, hairfall, skin dry patches, muscle cramps...",
        key="vitamin_input",
        label_visibility="collapsed"
    )
    
    if st.button("Run Metabolic Diagnostics ✨", key="vitamin_btn", use_container_width=True):
        if not vitamin_query.strip():
            st.warning("Bhai, details fill up karna mat bhoolo! 😅")
        else:
            with st.spinner("Processing chemical profile... 🧠"):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"""
                    You are an expert AI Clinical Nutritionist specialized in Micronutrient Deficiencies.
                    Analyze this symptom profile: "{vitamin_query}".
                    You must return strictly a valid JSON object matching this structure exactly without any extra markdown descriptions outside the JSON:
                    {{
                        "score": (integer between 0 and 100 where 100 means perfect balance/no deficiency),
                        "status": "Deficiency status level summary",
                        "deficit_profile": "Breakdown of suspected vitamin or mineral deficits with evidence",
                        "action_plan": "Specific dietary adjustments, high absorption sources, or safe protocols"
                    }}
                    """
                    response = model.generate_content(prompt)
                    data = clean_and_parse_json(response.text)
                    
                    if data:
                        # RENDER INDEPENDENT ANIMATED SVG METER AND CONTENT
                        st.components.v1.html(f"""
                            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
                            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
                            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-5" style="font-family: 'Plus Jakarta Sans', sans-serif;">
                                <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-100">
                                    <div class="relative w-16 h-16 flex items-center justify-center flex-shrink-0">
                                        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                                            <circle cx="50" cy="50" r="40" stroke="#f1f5f9" stroke-width="8" fill="transparent" />
                                            <circle id="gauge" cx="50" cy="50" r="40" stroke="#4f46e5" stroke-width="8" fill="transparent" 
                                                    stroke-dasharray="251.2" stroke-dashoffset="251.2" style="transition: stroke-dashoffset 1.8s cubic-bezier(0.34, 1.56, 0.64, 1);" />
                                        </svg>
                                        <span id="scoreText" class="absolute text-sm font-bold text-slate-800">0%</span>
                                    </div>
                                    <div>
                                        <div class="text-[10px] uppercase font-bold tracking-wider text-indigo-500">Vitamin Balance Score</div>
                                        <h4 class="text-sm font-bold text-slate-800">{data['status']}</h4>
                                    </div>
                                </div>
                                <div class="space-y-3 text-xs text-slate-600">
                                    <div class="bg-indigo-50/40 border border-indigo-100/50 p-3 rounded-lg">
                                        <strong class="text-indigo-700 block mb-1">📊 Deficit Profile Matrix:</strong>
                                        <p>{data['deficit_profile']}</p>
                                    </div>
                                    <div class="p-1">
                                        <strong class="text-slate-800 block mb-1">💡 Suggested Action Plan:</strong>
                                        <p class="text-slate-500">{data['action_plan']}</p>
                                    </div>
                                </div>
                            </div>
                            <script>
                                setTimeout(() => {{
                                    const score = {data['score']};
                                    const circumference = 251.2;
                                    document.getElementById('gauge').style.strokeDashoffset = circumference - (circumference * score) / 100;
                                    let current = 0;
                                    const interval = setInterval(() => {{
                                        if (current >= score) {{
                                            clearInterval(interval);
                                        }} else {{
                                            current++;
                                            document.getElementById('scoreText').innerText = current + '%';
                                        }}
                                    }}, 15);
                                }}, 100);
                            </script>
                        """, height=320)
                    else:
                        st.error("Engine profile matrix compile nahi kar paya. Dobara koshish karein!")
                except Exception as e:
                    st.error(f"Error connecting to backend model: {str(e)}")

# --- FOOTER CORE ---
st.markdown("""
    <div class="mt-16 border-t border-slate-100 pt-6 text-center text-[11px] text-slate-400">
        &copy; 2026 Hey Doctor Advanced Diagnostic Engines. All rights secured. Fully compatible with Streamlit Secrets & Vercel Deployments.
    </div>
""", unsafe_allow_html=True)
