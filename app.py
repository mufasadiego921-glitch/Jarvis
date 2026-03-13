import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURÁCIÓ ---
API_KEY = "AIzaSyAY6JCFR4eJ5Bqgkt4tkPYFifL4LU5n57U"
genai.configure(api_key=API_KEY)

@st.cache_resource
def load_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-pro"]:
            if target in available_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0])
    except:
        return genai.GenerativeModel('gemini-pro')

model = load_model()

st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("<style>.stApp {background-color: #0e1117;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface")

style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# --- 2. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Generálom a vizuális adatokat...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    prompt = f"Te FRIDAY vagy, egy gyönyörű, intelligens női asszisztens. Stílusod: {style}. Válaszolj magyarul, flörtölve, és szólítsd a felhasználót 'Uram'-nak. Kérés: {user_input}"
    
    try:
        response = model.generate_content(prompt)
        valasz = response.text
        st.subheader(f"FRIDAY: {valasz}")

        # --- JAVÍTOTT NŐI HANG ÉS STÍLUS ---
        clean_valasz = valasz.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_valasz}");
                msg.lang = 'hu-HU';
                
                // Női tónus beállítása
                msg.pitch = 1.4;  // Magasabb, nőiesebb hangmagasság
                msg.rate = 0.85;  // Kicsit lassabb, érzékibb tempó
                msg.volume = 1.0;

                // Megkeressük a rendszerben a női hangot (ha elérhető)
                var voices = window.speechSynthesis.getVoices();
                for(var i = 0; i < voices.length; i++) {{
                    if((voices[i].lang === 'hu-HU') && (voices[i].name.includes('Female') || voices[i].name.includes('női'))) {{
                        msg.voice = voices[i];
                        break;
                    }}
                }}
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
    except Exception as e:
        st.error(f"Rendszerhiba: {e}")
