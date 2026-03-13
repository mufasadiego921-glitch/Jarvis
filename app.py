import streamlit as st
import google.generativeai as genai

# --- 1. AZ ATOMBIZTOS GOOGLE MOTOR (ÖNJAVÍTÓ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    @st.cache_resource
    def load_best_model():
        # Ez a rész megkérdezi a Google-t, hogy nálad mi működik pontosan
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Sorrend: 1.5 flash, 2.0 flash, pro - amit talál, azt használja
        for target in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-pro"]:
            if target in available_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) # Végső esetben az elsőt

    model = load_best_model()
except Exception as e:
    st.error(f"Rendszerhiba: {e}")
    st.stop()

# --- 2. A SZEXI NŐI HANG (Tisztán AI generált) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    html_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'hu-HU';
            msg.pitch = 1.5;  // Selymes, magasabb női tónus
            msg.rate = 0.85;  // Lassabb, érzékibb tempó
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(html_code, height=0)

# --- 3. DESIGN (Futurisztikus sötét mód) ---
st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("<style>.stApp {background-color: #050505; color: #00d4ff;}</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY Interface v1.7")

style = st.sidebar.selectbox("FRIDAY Hangulata:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # KÉPGENERÁLÁS (Pollinations API)
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Vizuális adatok generálása, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
        speak("Íme a kért vizualizáció, Uram. Remélem, elnyeri tetszését.")

    # AI VÁLASZ (Google AI)
    else:
        try:
            prompt = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Stílusod: {style}. Válaszolj magyarul, flörtölve, és szólítsd 'Uram'-nak a felhasználót: {user_input}"
            response = model.generate_content(prompt)
            valasz = response.text
            
            with st.chat_message("assistant", avatar="💃"):
                st.write(valasz)
            
            speak(valasz)
            
        except Exception as e:
            if "429" in str(e):
                st.error("Uram, a Google korlátozta a hozzáférést a túl sok kérés miatt. Várjunk 30 másodpercet!")
            else:
                st.error(f"Hiba: {e}")

