import streamlit as st
import google.generativeai as genai
import time
import random
import urllib.parse

# --- 1. MOTOR (ÖNJAVÍTÓ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    @st.cache_resource
    def load_model():
        available = [m.name for m in genai.list_models()]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available: return genai.GenerativeModel(target)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    model = load_model()
except:
    st.error("Rendszerhiba: API kulcs hiányzik!")
    st.stop()

# --- 2. SZEXI NŐI HANG (JS) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'hu-HU'; msg.pitch = 1.5; msg.rate = 0.85;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v2.0")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # JAVÍTOTT KÉPGENERÁLÁS
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        with st.spinner("Vizuális adatok kódolása..."):
            # Tisztítjuk a szöveget az URL-hez
            clean_prompt = urllib.parse.quote(user_input)
            # Véletlenszerű szám, hogy mindig frissüljön (Cache törlés)
            seed = random.randint(0, 99999)
            img_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
            
            # Megjelenítés
            st.image(img_url, use_container_width=True)
            st.markdown(f"[Kép megnyitása teljes méretben]({img_url})")
            speak("Íme a kért kép, Uram. Sikerült a generálás.")
    
    # AI VÁLASZ
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            speak(valasz)
        except Exception as e:
            if "429" in str(e): st.error("Google korlátozás. Várjunk 30 mp-et!")
            else: st.error(f"Hiba: {e}")

