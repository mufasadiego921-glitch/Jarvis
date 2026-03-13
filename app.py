import streamlit as st
import google.generativeai as genai
import random
import urllib.parse

# --- 1. MOTOR (ÖNJAVÍTÓ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    @st.cache_resource
    def load_model():
        all_models = [m.name for m in genai.list_models()]
        for t in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if t in all_models: return genai.GenerativeModel(t)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    model = load_model()
except:
    st.error("API kulcs hiányzik!")
    st.stop()

# --- 2. SZEXI NŐI HANG (JS) ---
def speak(text):
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance('{clean}'); m.lang='hu-HU'; m.pitch=1.5; m.rate=0.85; window.speechSynthesis.speak(m);</script>", height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v2.1")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # JAVÍTOTT KÉPGENERÁLÁS (Markdown módszerrel)
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        # Prompt tisztítása
        q = urllib.parse.quote(user_input)
        seed = random.randint(100, 99999)
        img_url = f"https://image.pollinations.ai{q}?width=1024&height=1024&seed={seed}&nologo=true"
        
        # Megjelenítés két módon a biztonság kedvéért
        st.markdown(f"![Generált kép]({img_url})")
        st.write(f"[Ha nem látod a képet, kattints ide]({img_url})")
        speak("Íme a vizuális adatok, Uram. Remélem, tetszik, amit lát.")
    
    # AI VÁLASZ
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            speak(valasz)
        except Exception as e:
            st.error(f"Hiba: {e}")

