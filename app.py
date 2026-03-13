import streamlit as st
import google.generativeai as genai
import time

# --- 1. MOTOR (ÖNJAVÍTÓ + ÚJRAPRÓBÁLKOZÓ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    @st.cache_resource
    def load_best_model():
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in all_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(all_models[0])

    model = load_best_model()
except Exception as e:
    st.error(f"Rendszerhiba: {e}")
    st.stop()

# --- 2. SZEXI NŐI HANG (JS) ---
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
st.title("💃 FRIDAY Interface v1.9")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # KÉPGENERÁLÁS DETEKTÁLÁSA
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        with st.spinner("Vizuális adatok feldolgozása, Uram..."):
            # A prompt kinyerése és URL baráttá tétele
            img_prompt = user_input.replace(" ", "%20")
            img_url = f"https://pollinations.ai{img_prompt}?width=1024&height=1024&nologo=true"
            
            st.image(img_url, caption=f"Generált vizualizáció: {user_input}")
            speak("Íme a kért kép, Uram. Remélem, elnyeri tetszését.")
    
    # AI VÁLASZ (Várakozási logikával)
    else:
        success = False
        attempts = 0
        prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve, és szólítsd 'Uram'-nak a felhasználót: {user_input}"
        
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
                    with st.spinner("Google túlterhelt, várakozás..."):
                        time.sleep(5)
                else:
                    st.error(f"Hiba: {e}")
                    break
