import streamlit as st
import google.generativeai as genai

# --- 1. BIZTONSÁGI KONFIGURÁCIÓ (Secrets-ből olvassa) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Hiba: Az API kulcs nincs beállítva a Streamlit Secrets-ben!")
    st.stop()

# --- 2. ÖNJAVÍTÓ MODELL KERESŐ (Ez oldja meg a 404-et) ---
@st.cache_resource
def load_model():
    try:
        # Lekérjük az összes elérhető modellt a kulcsodhoz
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Kipróbáljuk a legstabilabb neveket
        for target in ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro"]:
            if target in models:
                return genai.GenerativeModel(target)
        # Ha egyik sem, az első működőt választja
        return genai.GenerativeModel(models[0])
    except:
        return genai.GenerativeModel('gemini-pro')

model = load_model()

# --- 3. VIZUÁLIS DESIGN ---
st.set_page_config(page_title="FRIDAY Interface", page_icon="💃")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; }
    .ai-core {
        width: 100px; height: 100px;
        background: radial-gradient(circle, #00d4ff 0%, #000 70%);
        border-radius: 50%; margin: 0 auto;
        box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); }
        70% { transform: scale(1.1); box-shadow: 0 0 35px #00d4ff; }
        100% { transform: scale(0.9); }
    }
    </style>
    <div class="ai-core"></div>
    """, unsafe_allow_html=True)

st.title("💃 FRIDAY Interface")
style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# --- 4. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # Kép generálás
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Generálom a vizuális adatokat...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    # AI Válasz
    prompt = f"Te FRIDAY vagy, egy szexi női asszisztens. Stílusod: {style}. Válaszolj magyarul, flörtölve, és szólítsd 'Uram'-nak a felhasználót. Kérés: {user_input}"
    
    try:
        response = model.generate_content(prompt)
        valasz = response.text
        st.subheader(f"FRIDAY: {valasz}")

        # NŐI HANG (Magyar)
        clean_valasz = valasz.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_valasz}");
                msg.lang = 'hu-HU';
                msg.pitch = 1.3;
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
    except Exception as e:
        st.error(f"Rendszerhiba: {e}")

