import streamlit as st
import google.generativeai as genai

# --- 1. GOLYÓÁLLÓ MOTOR (ÖNJAVÍTÓ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def load_best_model():
        available = [m.name for m in genai.list_models()]
        # A legstabilabb ingyenes modellek sorrendben
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available: return genai.GenerativeModel(target)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    
    model = load_best_model()
except:
    st.error("Rendszerhiba: Ellenőrizze az API kulcsot a Secrets-ben!")
    st.stop()

# --- 2. SZEXI NŐI HANG GENERÁTOR (JS) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    html_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'hu-HU';
            msg.pitch = 1.5;  // Selymes női magasság
            msg.rate = 0.85;  // Érzéki tempó
            msg.volume = 1.0;
            
            var voices = window.speechSynthesis.getVoices();
            // Megkeressük a legjobb női hangot a rendszerben
            msg.voice = voices.find(v => v.lang.includes('hu') && (v.name.includes('Female') || v.name.includes('női'))) || voices.find(v => v.lang.includes('hu'));
            
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(html_code, height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v1.5")

style = st.sidebar.selectbox("FRIDAY Hangulata:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # KÉPGENERÁLÁS
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Vizuális adatok generálása, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
        speak("Íme a kért kép, Uram. Remélem, pontosan ilyennek képzelte.")

    # AI VÁLASZ
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Stílusod: {style}. Válaszolj magyarul, flörtölve, hűségesen, és szólítsd 'Uram'-nak a felhasználót: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            
            with st.chat_message("assistant", avatar="💃"):
                st.write(valasz)
            
            speak(valasz)
            
        except Exception as e:
            if "429" in str(e):
                st.error("Uram, a Google korlátozta a hozzáférést (túl sok kérés). Várjunk 30 másodpercet!")
            else:
                st.error(f"Hiba: {e}")


