import streamlit as st
import time
import streamlit.components.v1 as components

# Page Configurations
st.set_page_config(
    page_title="Medicine Reminder - Heydoctor.ai",
    page_icon="💊",
    layout="centered"
)

# Custom Styling (Aapke dark health theme se match karne ke liye)
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

# Title & Description
st.markdown('<h1 class="main-title">💊 Medicine Reminder & Tracker</h1>', unsafe_allow_html=True)

# Session State Storage initialization
if "reminders_list" not in st.session_state:
    st.session_state.reminders_list = []

# ==============================================================================
# 🎯 ADVANCED TIME SELECTION (TYPE + AM/PM DROPDOWN)
# ==============================================================================
st.markdown("### ⏰ Set New Reminder")

# Medicine Name Input
med_name = st.text_input("Medicine Name", placeholder="e.g., Paracetamol 650mg")

# Time configuration rows
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    # Hours input text box (Typable)
    hr_in = st.number_input("Hour (1-12)", min_value=1, max_value=12, value=8, step=1)

with col2:
    # Minutes input text box (Typable)
    min_in = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, step=1)

with col3:
    # AM/PM Selector Dropdown
    period = st.selectbox("AM / PM", ["AM", "PM"])

# Formatting time string for processing
formatted_minutes = f"{min_in:02d}"
display_time = f"{hr_in}:{formatted_minutes} {period}"

# Conversion to 24-hour format logic background tracking ke liye
hr_24 = hr_in
if period == "PM" and hr_in != 12:
    hr_24 += 12
elif period == "AM" and hr_in == 12:
    hr_24 = 0
time_24_str = f"{hr_24:02d}:{formatted_minutes}:00"

# Save Button trigger
if st.button("Set Reminder Alert"):
    if med_name.strip():
        st.session_state.reminders_list.append({
            "name": med_name,
            "display": display_time,
            "match_time": time_24_str[0:5] # HH:MM target
        })
        st.success(f"✅ Reminder successfully saved for **{med_name}** at **{display_time}**!")
    else:
        st.error("🚨 Please enter a valid Medicine Name first.")

# ==============================================================================
# DISPLAY ACTIVE REMINDERS
# ==============================================================================
if st.session_state.reminders_list:
    st.markdown("### 📋 Active Tracking Schedule")
    for idx, r in enumerate(st.session_state.reminders_list):
        st.info(f"⏰ **{r['display']}** — Take medication: **{r['name']}**")

# ==============================================================================
# 📖 EDUCATIONAL CONTENT (WHAT IS MEDICINE TIMING?)
# ==============================================================================
st.markdown("---")
st.markdown("## 🧠 Why Medicine Timing Matters?")
st.markdown(
    '<p class="info-text">'
    "Maintaining a consistent schedule for your prescription intake is essential for managing your health "
    "effectively. When you take your medication at the exact same time every day, it ensures a stable and "
    "optimal concentration of the active therapeutic compound within your bloodstream.<br><br>"
    "<b>⚠️ Critical Risks of Missing Schedule:</b><br>"
    "• Sudden drop in drug efficacy level.<br>"
    "• Biological resistance build-up against active formulations.<br>"
    "• Disruption of systemic physiological balance."
    '</p>',
    unsafe_allow_html=True
)

# ==============================================================================
# BACKGROUND LIVE WORKER (JAVASCRIPT RUNTIME ALERTS)
# ==============================================================================
js_reminders = str(st.session_state.reminders_list)

components.html(f"""
<script>
    if (Notification.permission !== "granted" && Notification.permission !== "denied") {{
        Notification.requestPermission();
    }}

    const activeList = {js_reminders};
    
    function monitorSystemClock() {{
        const sysDate = new Date();
        const currentHHMM = sysDate.toTimeString().split(' ')[0].substring(0,5); // Gets HH:MM
        
        activeList.forEach(item => {{
            if (item.match_time === currentHHMM && !window[item.name + item.match_time]) {{
                window[item.name + item.match_time] = true; // Block loop duplication
                
                // Audio signal trigger
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, audioCtx.currentTime);
                osc.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 1.5); // Beep for 1.5 seconds

                // Browser Popup Display
                alert("🚨 HEYDOCTOR.AI REMINDER:\\n\\nTime to take your medicine: " + item.name);
                
                // Operating System Push Alert
                if (Notification.permission === "granted") {{
                    new Notification("💊 Medication Time!", {{
                        body: "Please take your medicine: " + item.name,
                        icon: "https://cdn-icons-png.flaticon.com/512/822/822143.png"
                    }});
                }}
            }}
        }});
    }}
    setInterval(monitorSystemClock, 5000); // Poll clock every 5 seconds
</script>
""", height=0, width=0)

