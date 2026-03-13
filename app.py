import streamlit as st
import google.generativeai as genai
import os

# --- 1. GOLYÓÁLLÓ KONFIGURÁCIÓ (ÖNJAVÍTÓ MODELLKERESŐ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    @st.cache_resource
    def load_best_model():
        # Lekérjük, mi érhető el a kulcsodhoz
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Sorrend: 1.5 flash, 2.0 flash, pro
        for target in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-pro"]:
            if target in available:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available[0]) # Végső esetben az első működő

    model = load_best_model()
except Exception as e:
    st.error(f"Rendszerhiba az indításnál: {e}")
    st.stop()

# --- 2. HANGMINTA LEJÁTSZÓ ---
def play_voice_sample(file_name):
    if os.path.exists(file_name):
        audio_file = open(file_name, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    else:
        st.warning(f"A(z) '{file_name}' fájl nincs feltöltve a GitHubra!")

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY OS v1.2")

# --- 4. INTERAKCIÓ (CSAK EGYSZER!) ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # SPECIÁLIS HANGMINTA: Ha köszön, a feltöltött MP3 szólal meg
    if any(x in user_input.lower() for x in ["szia", "helló", "üdv"]):
        play_voice_sample("szexi_valasz.mp3")
        st.subheader("FRIDAY: Üdvözlöm, Uram. Már vártam Önre.")

    # KÉPGENERÁLÁS
    elif any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Azonnal generálom a vizuális adatokat...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)

    # ÁLTALÁNOS AI VÁLASZ (Google Motor)
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve, és szólítsd 'Uram'-nak a felhasználót. Kérés: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            
            # Tartalék női hang (Javascript)
            clean_valasz = valasz.replace('"', '').replace("'", "")
            html_code = f"""<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance("{clean_valasz}");m.lang='hu-HU';m.pitch=1.4;m.rate=0.9;window.speechSynthesis.speak(m);</script>"""
            st.components.v1.html(html_code, height=0)
        except Exception as e:
            st.error(f"Kommunikációs hiba: {e}")

