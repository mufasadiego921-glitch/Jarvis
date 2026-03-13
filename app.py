import streamlit as st
import google.generativeai as genai
import random
import urllib.parse

# --- 1. MOTOR ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    @st.cache_resource
    def load_model():
        all_m = [m.name for m in genai.list_models()]
        for t in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-pro"]:
            if t in all_m: return genai.GenerativeModel(t)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    model = load_model()
except:
    st.error("API kulcs hiba!")
    st.stop()

# --- 2. HANG ---
def speak(text):
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance('{clean}'); m.lang='hu-HU'; m.pitch=1.5; m.rate=0.85; window.speechSynthesis.speak(m);</script>", height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v2.3")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        # JAVÍTÁS: Új, stabilabb képgeneráló URL (Flux-Turbo motor)
        q = urllib.parse.quote(user_input)
        seed = random.randint(1, 999999)
        # Ez a link most a leggyorsabb és legbiztosabb ingyenes elérés
        img_url = f"https://pollinations.ai{q}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
        
        # Megjelenítés: st.image helyett st.markdown-t használunk a biztos betöltésért
        st.markdown(f'<img src="{img_url}" width="100%" style="border-radius:10px; border:2px solid #00d4ff;">', unsafe_allow_html=True)
        st.write(f"🔗 [Közvetlen link a képhez, ha nem töltene be]({img_url})")
        speak("A vizuális adatok feldolgozva. Íme a kép, Uram.")
    
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            speak(valasz)
        except Exception as e:
            st.error(f"Hiba: {e}")

