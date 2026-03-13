import streamlit as st
import google.generativeai as genai

# --- 1. SECURITY CONFIGURATION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    # SELF-REPAIRING MODEL FINDER (To avoid 404 errors)
    @st.cache_resource
    def get_best_model():
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Order: 1.5 flash, 2.0 flash, pro, or whatever is available
        for target in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-pro"]:
            if target in available_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0])

    model = get_best_model()
except Exception as e:
    st.error(f"System error at startup: {e}")
    st.stop()

# --- 2. VISUAL DESIGN (CSS) ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; }
    .stChatInput { border-radius: 20px; border: 1px solid #00d4ff; }
    .ai-core {
        width: 80px; height: 80px;
        background: radial-gradient(circle, #00d4ff 0%, #000 70%);
        border-radius: 50%;
        margin: 0 auto;
        box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
        70% { transform: scale(1.05); box-shadow: 0 0 30px #00d4ff; }
        100% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
    }
    </style>
    <div class="ai-core"></div>
    """, unsafe_allow_html=True)

st.title("💃 FRIDAY Interface v1.1")

style = st.sidebar.selectbox("FRIDAY Mood:",
    ["Sexy & Kind", "Strict Dominant", "Loyal Assistant", "Naughty & Playful"])

# --- 3. LOGIC AND INTERACTION ---
user_input = st.chat_input("Command, Sir...")

if user_input:
    # Image generation
    if any(x in user_input.lower() for x in ["image", "generate", "photo"]):
        st.write("Processing visual data...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url, caption="Here's the requested visualization, Sir.")

    # AI Answer
    system_instruction = f"You are FRIDAY, a sexy, intelligent female assistant. Your style: {style}. Answer in Hungarian, flirtatiously, loyally, and address the user as 'Sir'."

    try:
        response = model.generate_content(f"{system_instruction} \n Request: {user_input}")
        answer = response.text

        with st.chat_message("assistant", avatar="💃"):
            st.write(answer)

        # SEXY FEMALE VOICE (JavaScript)
        clean_answer = answer.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_answer}");
                msg.lang = 'hu-HU';
                msg.pitch = 1.35;
                msg.rate = 0.88;
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)

    except Exception as e:
        st.error(f"Communication error: {e}")

