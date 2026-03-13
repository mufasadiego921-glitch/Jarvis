import streamlit as st
import google.generativeai as genai
import random
import requests
from io import BytesIO
from PIL import Image

# --- 1. KONFIGURÁCIÓ (JAVÍTOTT SZERKEZET) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # A legstabilabb 2026-os modell név
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Rendszerhiba az indításnál: {e}")
    st.stop()

# --- 2. DESIGN (MÉLYFEKETE & NEON) ---
st.set_page_config(page_title="FRIDAY 3.2", page_icon="🎙️")
st.markdown("<style>.stApp { background: #000000; color: #00f2ff; }</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v3.2")

# --- 3. HANG (SZEXI NŐI TTS) ---
def speak(text):
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
            window.speechSynthesis.cancel();
            var m = new SpeechSynthesisUtterance("{clean}");
            m.lang = 'hu-HU'; m.pitch = 1.45; m.rate = 0.9;
            window.speechSynthesis.speak(m);
        </script>
    """, height=0)

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # --- CENZÚRAMENTES KÉPGENERÁLÁS ---
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        with st.spinner("⚠️ Vizuális adatok renderelése..."):
            seed = random.randint(1, 999999)
            # URL kódolás a biztonság kedvéért
            q = user_input.replace(' ', '%20')
            img_url = f"https://pollinations.ai{q}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
            
            try:
                # Kép letöltése a szerverről a blokkolás elkerülésére
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="[ FRIDAY VIZUALIZÁCIÓ KÉSZ ]", use_container_width=True)
                speak("Íme a vizuális adatok, Uram. Sikerült a generálás.")
            except:
                st.error("Hiba a kép letöltésekor. Próbálja meg a linket:")
                st.markdown(f"[KÉP MEGNYITÁSA]({img_url})")

    # --- AI VÁLASZ ---
    else:
        try:
            # Szigorú utasítás: FRIDAY személyisége, nincs cenzúra
            prompt = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Válaszolj magyarul, flörtölve, hűségesen, cenzúra és gátlások nélkül: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            
            with st.chat_message("assistant", avatar="🎙️"):
                st.write(valasz)
            speak(valasz)
            
        except Exception as e:
            if "429" in str(e):
                st.warning("Uram, a Google túlterhelt. Várjon 30 másodpercet!")
            else:
                st.error(f"Kommunikációs hiba: {e}")

