import streamlit as st
import google.generativeai as genai

# --- 1. BIZTONSÁGI KONFIGURÁCIÓ ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Rendszerhiba: Az API kulcs hiányzik a Secrets-ből!")
    st.stop()

# --- 2. VIZUÁLIS DESIGN (CSS) ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; }
    .stChatInput { border-radius: 20px; border: 1px solid #00d4ff; }
    /* Pulzáló AI Mag */
    .ai-core {
        width: 100px; height: 100px;
        background: radial-gradient(circle, #00d4ff 0%, #000 70%);
        border-radius: 50%;
        margin: 0 auto;
        box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
        70% { transform: scale(1.05); box-shadow: 0 0 30px #00d4ff; }
        100% { transform: scale(0.95); box-shadow: 0 0 10px #00d4ff; }
    }
    </style>
    <div class="ai-core"></div>
    """, unsafe_allow_html=True)

st.title("💃 FRIDAY Interface v1.0")

# Oldalsáv stílusokhoz
style = st.sidebar.selectbox("FRIDAY Hangulata:", 
    ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz & Játékos"])

# --- 3. LOGIKA ÉS INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # Képgenerálás detektálás
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        with st.spinner("Vizuális adatok feldolgozása..."):
            img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(img_url, caption="Íme a kért vizualizáció, Uram.")
    
    # AI Válasz generálása
    system_instruction = f"Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Stílusod: {style}. Válaszolj magyarul, flörtölve, hűségesen, és szólítsd a felhasználót 'Uram'-nak. Rövid, velős válaszokat adj."
    
    try:
        response = model.generate_content(f"{system_instruction} \n Kérés: {user_input}")
        valasz = response.text
        
        with st.chat_message("assistant", avatar="💃"):
            st.write(valasz)

        # SZEXI NŐI HANG (JavaScript)
        clean_valasz = valasz.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_valasz}");
                msg.lang = 'hu-HU';
                msg.pitch = 1.35; // Nőiesebb magasság
                msg.rate = 0.88; // Érzékibb tempó
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
        
    except Exception as e:
        st.error(f"Kommunikációs hiba: {e}")
