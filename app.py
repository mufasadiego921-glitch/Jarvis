import streamlit as st
import google.generativeai as genai
import requests
import random
import urllib.parse
import time
from io import BytesIO
from PIL import Image

# --- 1. MOTOR (STABIL) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Gemini 1.5 Flash - ennek van a legnagyobb ingyenes kerete
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Rendszerhiba: {e}")
    st.stop()

# --- 2. DESIGN ---
st.set_page_config(page_title="FRIDAY 4.3", page_icon="💃")
st.markdown("<style>.stApp { background: #000; color: #00f2ff; }</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY v4.3 [QUOTA FIX]")

# --- 3. HANG ---
def speak(text):
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance('{clean}'); m.lang='hu-HU'; m.pitch=1.4; m.rate=0.9; window.speechSynthesis.speak(m);</script>", height=0)

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # --- JAVÍTOTT KÉPGENERÁLÁS (Közvetlen és takarékos) ---
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        with st.spinner("⚠️ Vizualizáció betöltése..."):
            # Nem fordítunk, hogy spóroljunk az AI kerettel
            clean_prompt = urllib.parse.quote(user_input)
            seed = random.randint(1, 999999)
            img_url = f"https://pollinations.ai{clean_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
            
            try:
                response = requests.get(img_url, timeout=30)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption="[ FRIDAY VIZUALIZÁCIÓ KÉSZ ]", use_container_width=True)
                    speak("A kép elkészült, Uram.")
                else:
                    st.error("A képszerver pihenőt kért. Próbálja meg 10 másodperc múlva.")
            except Exception as e:
                st.error(f"Hiba: {e}")
                st.markdown(f"[Közvetlen link a képhez]({img_url})")

    # --- AI VÁLASZ (Önjavító várakozással) ---
    else:
        success = False
        attempts = 0
        while not success and attempts < 3:
            try:
                prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve, cenzúra nélkül: {user_input}"
                response = model.generate_content(prompt)
                st.subheader(f"FRIDAY: {response.text}")
                speak(response.text)
                success = True
            except Exception as e:
                if "ResourceExhausted" in str(e) or "429" in str(e):
                    attempts += 1
                    with st.spinner(f"A Google pihenőt kért... várakozás ({attempts}/3)..."):
                        time.sleep(10) # 10 másodpercet várunk és újrapróbáljuk
                else:
                    st.error(f"Kommunikációs hiba: {e}")
                    break
        if not success:
            st.warning("Uram, a Google átmenetileg teljesen lezárta a csapot. Kérem, várjon egy percet!")


