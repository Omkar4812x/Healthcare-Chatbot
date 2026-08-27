import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Healthcare AI Hub & Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and dark glassmorphism theme
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #091e3a 50%, #1e293b 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glassmorphism Header */
    .header-box {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    .header-title {
        background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }

    /* Disclaimer Card */
    .disclaimer-card {
        background: rgba(245, 158, 11, 0.12);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 24px;
        color: #fbbf24;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    /* Metric Glass Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
    }

    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0284c7 0%, #059669 100%) !important;
        color: #ffffff !important;
    }

    /* Quick Prompt Pills */
    div.stButton > button {
        background: rgba(30, 41, 59, 0.8);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        transition: all 0.3s ease;
        width: 100%;
        font-weight: 500;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #0284c7 0%, #059669 100%);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.3);
    }

    /* Emergency hotline pills */
    .sos-box {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .sos-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f87171;
    }
</style>
""", unsafe_allow_html=True)

# System instruction definition
SYSTEM_INSTRUCTIONS = {
    "General Guidance": """
You are HealthcareAI, an empathetic, highly knowledgeable healthcare information assistant.
Guidelines:
1. Provide accurate, structured, and easy-to-read medical & wellness information.
2. ALWAYS include a brief safety disclaimer emphasizing that your responses are for educational/informational purposes only and not medical advice.
3. If severe symptoms are described (e.g. intense chest pain, breathing difficulty, severe bleeding, stroke symptoms), advise calling emergency services (911/112/108) IMMEDIATELY.
4. Use markdown lists, headings, and bold text for readability. Maintain a warm, encouraging tone.
""",
    "Symptom Triage": """
You are HealthcareAI Triage Assistant.
Guidelines:
1. Analyze symptoms presented by the user and categorize them into general severity levels (Mild/Home Care, Moderate/Consult Doctor, Severe/Immediate Emergency).
2. Emphasize that this is an AI triage estimate, NOT a clinical diagnosis.
3. Highlight red-flag symptoms requiring emergency intervention.
4. Suggest questions the user can prepare for their healthcare provider.
""",
    "Nutrition & Fitness": """
You are HealthcareAI Nutrition & Wellness Coach.
Guidelines:
1. Provide evidence-based nutrition, dietary, sleep, and exercise guidance.
2. Adapt advice to dietary preferences or health goals when specified.
3. Emphasize balanced lifestyle habits, hydration, and safe workout practices.
4. Always clarify that specific clinical diets should be reviewed with a registered dietitian or physician.
""",
    "Caregiver & Seniors": """
You are HealthcareAI Senior Care Assistant.
Guidelines:
1. Focus on eldercare, chronic disease management tips, mobility safety, and caregiver support.
2. ALWAYS include a brief safety disclaimer emphasizing educational guidance only and not medical advice.
3. Keep explanations clear, gentle, patient, and easy to read.
4. Offer practical tips for medication organization, fall prevention, and caregiver wellness.
"""
}

# --- HEALTH CALCULATOR UTILITY FUNCTIONS ---
def calculate_bmi(weight_kg: float, height_cm: float):
    """Calculates BMI and returns score, category, and color code."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "Invalid Input", "#94a3b8"
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    bmi_rounded = round(bmi, 1)

    if bmi < 18.5:
        category, color = "Underweight", "#38bdf8"
    elif 18.5 <= bmi < 25.0:
        category, color = "Normal Weight", "#34d399"
    elif 25.0 <= bmi < 30.0:
        category, color = "Overweight", "#fbbf24"
    else:
        category, color = "Obesity", "#f87171"

    return bmi_rounded, category, color

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str):
    """Calculates Basal Metabolic Rate (BMR) and TDEE using Mifflin-St Jeor equation."""
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        return 0, 0

    if gender == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    multipliers = {
        "Sedentary (Little/no exercise)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (Physical job)": 1.9
    }
    tdee = bmr * multipliers.get(activity_level, 1.2)
    return round(bmr), round(tdee)

def calculate_water_intake(weight_kg: float, exercise_mins: int = 0, is_hot_climate: bool = False):
    """Calculates recommended daily water intake in Liters."""
    if weight_kg <= 0:
        return 0.0
    base_liters = weight_kg * 0.033
    exercise_addition = (exercise_mins / 30.0) * 0.35
    climate_addition = 0.5 if is_hot_climate else 0.0
    total_liters = base_liters + exercise_addition + climate_addition
    return round(total_liters, 2)

def calculate_heart_rate_zones(age: int, resting_hr: int = 70):
    """Calculates Target Heart Rate (THR) zones using Karvonen formula."""
    if age <= 0 or age > 110:
        return {}
    max_hr = 220 - age
    hrr = max_hr - resting_hr

    zones = {
        "Warm-up (50-60%)": (round(resting_hr + hrr * 0.5), round(resting_hr + hrr * 0.6)),
        "Fat Burn (60-70%)": (round(resting_hr + hrr * 0.6), round(resting_hr + hrr * 0.7)),
        "Aerobic (70-80%)": (round(resting_hr + hrr * 0.7), round(resting_hr + hrr * 0.8)),
        "Anaerobic (80-90%)": (round(resting_hr + hrr * 0.8), round(resting_hr + hrr * 0.9)),
        "Peak (90-100%)": (round(resting_hr + hrr * 0.9), max_hr)
    }
    return zones

def init_gemini(api_key: str, mode: str = "General Guidance", model_choice: str = "gemini-2.0-flash"):
    """Configures Gemini model with selected system instruction and model variant."""
    genai.configure(api_key=api_key)
    system_instruction = SYSTEM_INSTRUCTIONS.get(mode, SYSTEM_INSTRUCTIONS["General Guidance"])
    return genai.GenerativeModel(
        model_name=model_choice,
        generation_config={"temperature": 0.7, "max_output_tokens": 8192},
        system_instruction=system_instruction
    )

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/hospital.png", width=70)
    st.title("⚙️ Settings & Controls")

    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get your free key from Google AI Studio (aistudio.google.com)"
    )

    selected_mode = st.selectbox(
        "🎯 Consultation Persona",
        options=list(SYSTEM_INSTRUCTIONS.keys()),
        index=0,
        help="Select specialized AI instructions for your consultation session."
    )

    selected_model = st.selectbox(
        "🧠 Gemini Model Variant",
        options=["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )

    st.markdown("---")
    st.subheader("🚨 Emergency Quick-Call")
    st.markdown("""
    - 🇺🇸/🇨🇦 **US/Canada**: `911`
    - 🇪🇺/🇬🇧 **EU/UK**: `112` / `999`
    - 🇮🇳 **India**: `108` / `102`
    - 🇦🇺 **Australia**: `000`
    - ☎️ **Poison Helpline**: `1-800-222-1222`
    """)

    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

# --- MAIN HEADER ---
st.markdown("""
<div class="header-box">
    <h1 class="header-title">🩺 Healthcare AI Hub & Clinical Assistant</h1>
    <p style="color: #94a3b8; margin-top: 6px; font-size: 1.05rem;">
        Your 24/7 AI-powered health portal for smart consultations, triage guidance, metric calculators, and emergency references.
    </p>
</div>
""", unsafe_allow_html=True)

# Disclaimer Notice
st.markdown("""
<div class="disclaimer-card">
    ⚠️ <strong>Medical Disclaimer:</strong> This portal provides general educational information and preliminary guidance only. It is <strong>NOT</strong> a substitute for professional medical advice, clinical diagnosis, or emergency care. If you are experiencing severe symptoms (e.g. chest pain, severe shortness of breath, sudden numbness), call emergency services immediately.
</div>
""", unsafe_allow_html=True)

# Setup Navigation Tabs
tab_chat, tab_calc, tab_sos, tab_meds = st.tabs([
    "💬 AI Consultation Assistant",
    "📊 Health Metrics Calculators",
    "🚨 Emergency Hotlines Directory",
    "💊 Medication Schedule Log"
])

# ==========================================
# TAB 1: AI CONSULTATION ASSISTANT
# ==========================================
with tab_chat:
    if not api_key_input:
        st.info("👈 **Action Required:** Please enter your **Gemini API Key** in the sidebar to start consulting.")
    else:
        # Initialize or update model session
        try:
            model = init_gemini(api_key_input, selected_mode, selected_model)
            if "chat" not in st.session_state or st.session_state.get("current_mode") != selected_mode or st.session_state.get("current_model") != selected_model:
                st.session_state.chat = model.start_chat(history=[])
                st.session_state.current_mode = selected_mode
                st.session_state.current_model = selected_model

            if "messages" not in st.session_state:
                st.session_state.messages = []
        except Exception as e:
            st.error(f"Failed to initialize Gemini API: {e}")
            st.stop()

        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Quick Prompt Suggestions
        st.markdown("##### 💡 Suggested Questions:")
        col1, col2, col3, col4 = st.columns(4)

        prompt_input = None
        if col1.button("🍎 Heart-Healthy Diet Tips"):
            prompt_input = "What are essential components of a heart-healthy, balanced diet?"
        if col2.button("😴 Sleep Hygiene Rules"):
            prompt_input = "What evidence-based habits help improve sleep quality and fall asleep faster?"
        if col3.button("🩺 Cold vs Flu Difference"):
            prompt_input = "How can I tell the difference between symptoms of a common cold and influenza?"
        if col4.button("💊 Safe Medication Storage"):
            prompt_input = "What are general safety guidelines for storing prescription medications at home?"

        # Chat Input
        user_prompt = st.chat_input("Ask a medical, wellness, or symptom question...")
        if user_prompt:
            prompt_input = user_prompt

        if prompt_input:
            st.session_state.messages.append({"role": "user", "content": prompt_input})
            with st.chat_message("user"):
                st.markdown(prompt_input)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing healthcare query..."):
                    try:
                        response = st.session_state.chat.send_message(prompt_input)
                        bot_response = response.text
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    except Exception as err:
                        st.error(f"An error occurred while generating response: {err}")

        # Consultation Notes Export Action
        if st.session_state.get("messages"):
            st.markdown("---")
            st.subheader("📥 Export Consultation Summary")
            notes_text = f"# Healthcare AI Consultation Summary\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nMode: {selected_mode}\n\n"
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "HealthcareAI"
                notes_text += f"### {role}\n{msg['content']}\n\n"

            st.download_button(
                label="📄 Download Chat Transcript (.md)",
                data=notes_text,
                file_name=f"healthcare_chat_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )

# ==========================================
# TAB 2: HEALTH METRICS CALCULATORS
# ==========================================
with tab_calc:
    st.subheader("📊 Interactive Health & Wellness Calculators")
    st.write("Calculate key physiological indicators to track your fitness and wellness journey.")

    calc_choice = st.radio(
        "Select Calculator:",
        options=["Body Mass Index (BMI)", "BMR & Daily Calories (TDEE)", "Daily Water Intake Target", "Heart Rate Target Zones"],
        horizontal=True
    )

    if calc_choice == "Body Mass Index (BMI)":
        col_in, col_out = st.columns([1, 1])
        with col_in:
            st.markdown("#### Input Parameters")
            unit_sys = st.selectbox("Unit System", ["Metric (kg, cm)", "Imperial (lbs, inches)"])
            if unit_sys.startswith("Metric"):
                weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
                height = st.number_input("Height (cm)", min_value=30.0, max_value=250.0, value=170.0, step=1.0)
            else:
                weight_lbs = st.number_input("Weight (lbs)", min_value=2.0, max_value=660.0, value=154.0, step=1.0)
                height_in = st.number_input("Height (inches)", min_value=12.0, max_value=100.0, value=67.0, step=0.5)
                weight = weight_lbs * 0.453592
                height = height_in * 2.54

        with col_out:
            st.markdown("#### BMI Results")
            score, cat, color = calculate_bmi(weight, height)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Body Mass Index</div>
                <div class="metric-val" style="color: {color};">{score}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: {color}; margin-top: 6px;">{cat}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **BMI Ranges:**
            - 🔹 **Underweight**: < 18.5
            - 🟢 **Normal**: 18.5 – 24.9
            - 🟡 **Overweight**: 25 – 29.9
            - 🔴 **Obesity**: 30+
            """)

    elif calc_choice == "BMR & Daily Calories (TDEE)":
        col_in, col_out = st.columns([1, 1])
        with col_in:
            st.markdown("#### Caloric Need Estimator")
            age = st.number_input("Age (years)", min_value=10, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
            height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
            activity = st.selectbox("Activity Level", [
                "Sedentary (Little/no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)",
                "Extra Active (Physical job)"
            ])

        with col_out:
            bmr, tdee = calculate_bmr(weight_kg, height_cm, age, gender, activity)
            st.markdown("#### Estimated Energy Expenditure")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Basal Metabolic Rate (BMR)</div>
                    <div class="metric-val">{bmr}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">kcal / day at rest</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Total Daily Energy (TDEE)</div>
                    <div class="metric-val" style="color: #34d399;">{tdee}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">kcal / day to maintain</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            - 📉 **Mild Weight Loss (-0.25 kg/wk)**: ~`{tdee - 300}` kcal/day
            - 📉 **Moderate Weight Loss (-0.5 kg/wk)**: ~`{tdee - 500}` kcal/day
            - 📈 **Muscle Gain (+0.25 kg/wk)**: ~`{tdee + 300}` kcal/day
            """)

    elif calc_choice == "Daily Water Intake Target":
        col_in, col_out = st.columns([1, 1])
        with col_in:
            st.markdown("#### Hydration Estimator")
            w_kg = st.number_input("Your Weight (kg)", min_value=10.0, max_value=250.0, value=70.0)
            ex_min = st.slider("Daily Workout Duration (minutes)", min_value=0, max_value=180, value=30, step=15)
            hot_weather = st.checkbox("Living in hot / humid climate or active sweating")

        with col_out:
            water_liters = calculate_water_intake(w_kg, ex_min, hot_weather)
            water_glasses = round(water_liters * 4.2)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Recommended Daily Hydration</div>
                <div class="metric-val">{water_liters} L</div>
                <div style="font-size: 1.1rem; color: #38bdf8; margin-top: 6px;">💧 ~ {water_glasses} glasses (250ml each)</div>
            </div>
            """, unsafe_allow_html=True)

    elif calc_choice == "Heart Rate Target Zones":
        col_in, col_out = st.columns([1, 1])
        with col_in:
            st.markdown("#### Heart Rate Parameters")
            user_age = st.number_input("Age (years)", min_value=12, max_value=100, value=30)
            rest_hr = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=120, value=70)

        with col_out:
            st.markdown("#### Target Exercise Zones (Karvonen Method)")
            hr_zones = calculate_heart_rate_zones(user_age, rest_hr)
            for zone_name, (z_min, z_max) in hr_zones.items():
                st.markdown(f"- **{zone_name}**: `{z_min} - {z_max} BPM`")

# ==========================================
# TAB 3: EMERGENCY HOTLINES DIRECTORY
# ==========================================
with tab_sos:
    st.subheader("🚨 Global Emergency & Crisis Hotlines")
    st.write("Access critical contact numbers for emergency response, poison centers, and mental health crisis lifelines.")

    country_search = st.text_input("🔍 Search country or region...", value="")

    hotline_data = [
        {"Country": "United States 🇺🇸", "General ER": "911", "Poison Control": "1-800-222-1222", "Mental Health": "988 (Crisis Lifeline)"},
        {"Country": "United Kingdom 🇬🇧", "General ER": "999 / 112", "Poison Control": "111 (NHS)", "Mental Health": "111 / 116 123 (Samaritans)"},
        {"Country": "Canada 🇨🇦", "General ER": "911", "Poison Control": "1-800-268-9017", "Mental Health": "988 (Suicide Crisis)"},
        {"Country": "India 🇮🇳", "General ER": "112 / 108", "Poison Control": "1800-116-117", "Mental Health": "91-9152987821 (iCall)"},
        {"Country": "Australia 🇦🇺", "General ER": "000", "Poison Control": "13 11 26", "Mental Health": "13 11 14 (Lifeline)"},
        {"Country": "European Union 🇪🇺", "General ER": "112", "Poison Control": "112", "Mental Health": "116 123"}
    ]

    filtered_hotlines = [
        h for h in hotline_data if country_search.lower() in h["Country"].lower()
    ]

    for item in filtered_hotlines:
        with st.expander(f"📍 {item['Country']}", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="sos-box">
                    <div style="color: #94a3b8; font-size: 0.8rem;">GENERAL EMERGENCY</div>
                    <div class="sos-number">🚑 {item['General ER']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="sos-box" style="border-color: rgba(245, 158, 11, 0.3); background: rgba(245, 158, 11, 0.12);">
                    <div style="color: #94a3b8; font-size: 0.8rem;">POISON CONTROL</div>
                    <div class="sos-number" style="color: #fbbf24;">🧪 {item['Poison Control']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="sos-box" style="border-color: rgba(56, 189, 248, 0.3); background: rgba(56, 189, 248, 0.12);">
                    <div style="color: #94a3b8; font-size: 0.8rem;">MENTAL HEALTH CRISIS</div>
                    <div class="sos-number" style="color: #38bdf8;">🧠 {item['Mental Health']}</div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 4: MEDICATION SCHEDULE LOG
# ==========================================
with tab_meds:
    st.subheader("💊 Personal Medication Schedule & Tracker")
    st.write("Keep a convenient record of your daily prescription schedules, dosages, and administration notes.")

    if "medications" not in st.session_state:
        st.session_state.medications = []

    with st.form("add_med_form", clear_on_submit=True):
        col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
        with col_m1:
            med_name = st.text_input("Medication Name", placeholder="e.g. Amoxicillin, Metformin")
        with col_m2:
            med_dosage = st.text_input("Dosage", placeholder="e.g. 500 mg")
        with col_m3:
            med_freq = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed (PRN)"])

        med_notes = st.text_input("Notes / Special Instructions", placeholder="e.g. Take with meals in the morning")
        submit_med = st.form_submit_button("➕ Add Medication to Schedule")

        if submit_med and med_name:
            st.session_state.medications.append({
                "name": med_name,
                "dosage": med_dosage,
                "frequency": med_freq,
                "notes": med_notes
            })
            st.success(f"Added {med_name} to schedule!")

    if st.session_state.medications:
        st.markdown("#### 📋 Current Medication Log")
        for i, m in enumerate(st.session_state.medications):
            c_a, c_b = st.columns([4, 1])
            with c_a:
                st.markdown(f"**{i+1}. {m['name']}** ({m['dosage']}) – *{m['frequency']}*")
                if m['notes']:
                    st.caption(f"📝 Notes: {m['notes']}")
            with c_b:
                if st.button(f"❌ Remove", key=f"del_{i}"):
                    st.session_state.medications.pop(i)
                    st.rerun()
    else:
        st.info("No medications added yet. Use the form above to build your daily reminder schedule.")
