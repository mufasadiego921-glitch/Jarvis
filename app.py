import streamlit as st
import google.generativeai as genai

# --- 1. GOLYÓÁLLÓ MOTOR KERESŐ ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def load_best_model():
        # Lekérjük az összes modellt, amit a kulcsod ismer
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Próbálkozunk a legújabbakkal, pontos névvel
        targets = [
            "models/gemini-2.0-flash", 
            "models/gemini-1.5-flash", 
            "models/gemini-1.5-flash-latest",
            "models/gemini-pro"
        ]
        
        for t in targets:
            if t in all_models:
                return genai.GenerativeModel(t)
        
        # Ha egyik se, az elsőt adjuk vissza, amit a Google felajánl
        return genai.GenerativeModel(all_models[0])
    
    model = load_best_model()
except Exception as e:
    st.error(f"Rendszerindítási hiba: {e}")
    st.stop()

# --- 2. SZEXI NŐI HANG (JS) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    html_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'hu-HU';
            msg.pitch = 1.5;
            msg.rate = 0.85;
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(html_code, height=0)

# --- 3. DESIGN ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v1.6")

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Vizuális adatok generálása, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
        speak("Íme a kért kép, Uram.")
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Válaszolj magyarul, flörtölve, és szólítsd 'Uram'-nak a felhasználót: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            st.subheader(f"FRIDAY: {valasz}")
            speak(valasz)
        except Exception as e:
            st.error(f"Hiba: {e}")


