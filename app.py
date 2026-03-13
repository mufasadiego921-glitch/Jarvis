import streamlit as st
import google.generativeai as genai
import requests
import random
import urllib.parse
from io import BytesIO
from PIL import Image

# --- 1. MOTOR ÉS BIZTONSÁG ---
try:
    # Google API a gondolkodáshoz, ElevenLabs a szexi hanghoz
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVEN_KEY = st.secrets["ELEVEN_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Hiányzik egy API kulcs a Secrets-ből!")
    st.stop()

# --- 2. HANGMINTA FUNKCIÓ (ELEVENLABS - NEM ROBOT) ---
def play_human_voice(text):
    # 'Gigi' hang ID-ja (szexi női). Cserélheted férfiéra is.
    VOICE_ID = "jBpfuIE2acnXOq7pEycI" 
    url = f"https://api.elevenlabs.io{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    try:
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            st.audio(resp.content, format="audio/mp3", autoplay=True)
    except: pass

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY 6.0", page_icon="💃")
st.markdown("<style>.stApp { background: #000; color: #00f2ff; }</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY v6.0 [CORE]")

# --- 4. INTERAKCIÓ (HALLJA A HANGOD ÉS ÍRNI IS TUDSZ) ---
# A telefonodon a chat mezőbe kattintva a mikrofon ikonnal tudsz beszélni hozzá!
user_input = st.chat_input("Parancsoljon, Uram... (Használja a mikrofont a billentyűzeten!)")

if user_input:
    # KÉPGENERÁLÁS (FLUX - CENZÚRA NÉLKÜL)
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        with st.spinner("⚠️ Vizualizáció..."):
            q = urllib.parse.quote(user_input)
            seed = random.randint(1, 999999)
            img_url = f"https://pollinations.ai{q}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
            try:
                resp = requests.get(img_url)
                st.image(Image.open(BytesIO(resp.content)), use_container_width=True)
                play_human_voice("A kép elkészült, Uram.")
            except: st.markdown(f"[KÉP MEGNYITÁSA]({img_url})")

    # AI VÁLASZ (CENZÚRA NÉLKÜL)
    else:
        try:
            # Szigorú utasítás: FRIDAY személyisége, nincs cenzúra
            prompt = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Válaszolj magyarul, flörtölve, cenzúra és gátlások nélkül: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            # Itt szólal meg a szexi hangminta!
            play_human_voice(valasz)
        except Exception as e:
            st.error(f"Hiba: {e}")

