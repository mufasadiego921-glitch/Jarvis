import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. GOLYÓÁLLÓ KONFIGURÁCIÓ ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    @st.cache_resource
    def load_best_model():
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Sorrend: ha a 2.0 betelt, próbálja az 1.5-öt, az stabilabb ingyen
        for target in ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-2.0-flash"]:
            if target in available:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available[0])

    model = load_best_model()
except Exception as e:
    st.error(f"Rendszerhiba: {e}")
    st.stop()

# --- 2. HANGMINTA LEJÁTSZÓ ---
def play_voice_sample(file_name):
    if os.path.exists(file_name):
        audio_file = open(file_name, 'rb')
        st.audio(audio_file.read(), format="audio/mp3", autoplay=True)
    else:
        st.warning(f"A(z) '{file_name}' nincs feltöltve!")

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY OS v1.3")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    if any(x in user_input.lower() for x in ["szia", "helló", "üdv"]):
        play_voice_sample("szexi_valasz.mp3")
        st.subheader("FRIDAY: Üdvözlöm, Uram. Már vártam Önre.")

    elif any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Vizuális adatok betöltése...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)

    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            
            clean_valasz = valasz.replace('"', '').replace("'", "")
            html_code = f"""<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance("{clean_valasz}");m.lang='hu-HU';m.pitch=1.4;m.rate=0.9;window.speechSynthesis.speak(m);</script>"""
            st.components.v1.html(html_code, height=0)
        except Exception as e:
            if "429" in str(e):
                st.error("Uram, a Google korlátozta a hozzáférést a túl sok kérés miatt. Kérem, várjon 1 percet, és folytathatjuk!")
            else:
                st.error(f"Kommunikációs hiba: {e}")


