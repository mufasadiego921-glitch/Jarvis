import streamlit as st
import google.generativeai as genai
import time

# --- 1. BULLETPROOF ENGINE (SELF-REPAIRING + RETRYING) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    @st.cache_resource
    def load_best_model():
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # 1.5-flash is the most stable and allows the most free requests
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in all_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(all_models[0])

    model = load_best_model()
except Exception as e:
    st.error(f"System error: {e}")
    st.stop()

# --- 2. SEXY FEMALE VOICE (JS) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    html_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'hu-HU';
            msg.pitch = 1.5;
            msg.rate = 0.85;
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(html_code, height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v1.8")

# --- 4. INTERACTION WITH SMART WAITING ---
user_input = st.chat_input("Command, Sir...")

if user_input:
    if any(x in user_input.lower() for x in ["image", "generate", "photo"]):
        st.write("Generating visual data, Sir...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
        speak("Here is the requested visualization, Sir.")
    else:
        # RETRY LOGIC (Max 3 attempts)
        success = False
        attempts = 0
        prompt = f"You are FRIDAY, a sexy female assistant. Answer in Hungarian, flirting, and address the user as 'Sir': {user_input}"
        
        while not success and attempts < 3:
            try:
                response = model.generate_content(prompt)
                valasz = response.text
                st.subheader(f"FRIDAY: {valasz}")
                speak(valasz)
                success = True
            except Exception as e:
                if "429" in str(e):
                    attempts += 1
                    with st.spinner(f"Google is overloaded, waiting... ({attempts}/3)"):
                        time.sleep(5) # Wait 5 seconds and retry
                else:
                    st.error(f"Error: {e}")
                    break
        
        if not success and attempts >= 3:
            st.warning("Sir, Google has currently closed the tap completely. Please take a 1-minute break!")

