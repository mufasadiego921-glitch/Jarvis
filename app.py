import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURÁCIÓ (ÖNJAVÍTÓ MOTOR) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    @st.cache_resource
    def load_model():
        # Megkeressük a legstabilabb motort, ami nem dob 429-est vagy 404-est
        available = [m.name for m in genai.list_models()]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available: return genai.GenerativeModel(target)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    model = load_model()
except:
    st.error("Rendszerhiba az indításnál!")
    st.stop()

# --- 2. HANGMINTA ÉS SZEXI TTS ---
def play_voice(text, is_mp3=False, file_name=None):
    if is_mp3 and file_name and os.path.exists(file_name):
        # Fix MP3 lejátszása (pl. Szia esetén)
        audio_file = open(file_name, 'rb')
        st.audio(audio_file.read(), format="audio/mp3", autoplay=True)
    else:
        # GENERÁLT SZEXI NŐI HANG (Minden másra)
        clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'hu-HU';
                msg.pitch = 1.6;  // Magasabb, selymesebb női tónus
                msg.rate = 0.8;   // Lassabb, érzékibb beszédtempó
                msg.volume = 1.0;
                
                // Megkeressük a rendszer legjobb női hangját
                var voices = window.speechSynthesis.getVoices();
                msg.voice = voices.find(v => v.lang.includes('hu') && v.name.includes('Female')) || voices.find(v => v.lang.includes('hu'));
                
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v1.4")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # Speciális eset: SZIA (MP3 + Szöveg)
    if any(x in user_input.lower() for x in ["szia", "helló", "üdv"]):
        valasz = "Üdvözlöm, Uram. Már vártam Önre. Hogy szolgálhatom ma este?"
        st.subheader(f"FRIDAY: {valasz}")
        play_voice(valasz, is_mp3=True, file_name="szexi_valasz.mp3")

    # Képgenerálás
    elif any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Vizuális adatok generálása...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
        play_voice("Íme a kért vizualizáció, Uram. Remélem, elnyeri tetszését.")

    # Minden más (AI Válasz + Szexi generált hang)
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Válaszolj magyarul, flörtölve, hűségesen, és szólítsd 'Uram'-nak a felhasználót: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            play_voice(valasz)
        except Exception as e:
            st.error(f"Hiba: {e}")


