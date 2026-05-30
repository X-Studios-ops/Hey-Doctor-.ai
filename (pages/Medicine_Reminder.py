import streamlit as st
import time
import json
import streamlit.components.v1 as components

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Medicine Reminder - Heydoctor.ai",
    page_icon="💊",
    layout="centered"
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
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00F2FE, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-text {
    color: #a0aec0;
    font-size: 15px;
    line-height: 1.6;
}
.stButton button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #00F2FE, #10B981);
    color: black;
    font-weight: bold;
    border: none;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">💊 Medicine Reminder & Tracker</h1>', unsafe_allow_html=True)

# Session State Storage initialization
if "reminders_list" not in st.session_state:
    st.session_state.reminders_list = []

# ==============================================================================
# TIME SELECTION (TYPE + AM/PM)
# ==============================================================================
st.markdown("### ⏰ Set New Reminder")

med_name = st.text_input("Medicine Name", placeholder="e.g., Paracetamol 650mg")

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    hr_in = st.number_input("Hour (1-12)", min_value=1, max_value=12, value=8, step=1)
with col2:
    min_in = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, step=1)
with col3:
    period = st.selectbox("AM / PM", ["AM", "PM"])

# Formatting time string
formatted_minutes = f"{min_in:02d}"
display_time = f"{hr_in}:{formatted_minutes} {period}"

# 24-hour conversion for JS tracking
hr_24 = hr_in
if period == "PM" and hr_in != 12:
    hr_24 += 12
elif period == "AM" and hr_in == 12:
    hr_24 = 0
time_24_str = f"{hr_24:02d}:{formatted_minutes}:00"

if st.button("Set Reminder Alert"):
    if med_name.strip():
        st.session_state.reminders_list.append({
            "name": med_name.strip(),
            "display": display_time,
            "match_time": time_24_str[0:5]
        })
        st.success(f"✅ Reminder saved for **{med_name}** at **{display_time}**!")
    else:
        st.error("🚨 Please enter a valid Medicine Name.")

# ==============================================================================
# DISPLAY ACTIVE REMINDERS
# ==============================================================================
if st.session_state.reminders_list:
    st.markdown("### 📋 Active Tracking Schedule")
    for r in st.session_state.reminders_list:
        st.info(f"⏰ **{r['display']}** — Take medication: **{r['name']}**")

st.markdown("---")
st.markdown("## 🧠 Why Medicine Timing Matters?")
st.markdown(
    '<p class="info-text">Maintaining a consistent schedule ensures optimal concentration of medicine in your body.<br><br>'
    '<b>⚠️ Risks of Missing Schedule:</b><br>'
    '• Drop in drug efficacy.<br>'
    '• Biological resistance.<br>'
    '• Disruption of systemic physiological balance.</p>',
    unsafe_allow_html=True
)

# ==============================================================================
# BACKGROUND LIVE WORKER (100% CRASH-FREE JAVASCRIPT INJECTION)
# ==============================================================================
js_data = json.dumps(st.session_state.reminders_list)

# Plain text template jisme koi formatting clash nahi hoga
html_template = """
<script>
    if (Notification.permission !== "granted" && Notification.permission !== "denied") {
        Notification.requestPermission();
    }

    const activeList = INSERT_JSON_HERE;
    
    function monitorSystemClock() {
        const sysDate = new Date();
        const currentHHMM = sysDate.toTimeString().split(' ')[0].substring(0,5);
        
        activeList.forEach(item => {
            if (item.match_time === currentHHMM && !window[item.name + item.match_time]) {
                window[item.name + item.match_time] = true;
                
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, audioCtx.currentTime);
                osc.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 1.5);

                alert("🚨 HEYDOCTOR.AI REMINDER:\\n\\nTime to take your medicine: " + item.name);
                
                if (Notification.permission === "granted") {
                    new Notification("💊 Medication Time!", {
                        body: "Please take your medicine: " + item.name,
                        icon: "https://cdn-icons-png.flaticon.com/512/822/822143.png"
                    });
                }
            }
        });
    }
    setInterval(monitorSystemClock, 5000);
</script>
"""

# Replace method se safely data inject kar diya
final_html_code = html_template.replace("INSERT_JSON_HERE", js_data)
components.html(final_html_code, height=0, width=0)
