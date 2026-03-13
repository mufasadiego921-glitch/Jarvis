import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIÓ ---
# IDE MÁSOLD BE AZ API KULCSODAT!
API_KEY = "AIzaSyAY6JCFR4eJ5Bqgkt4tkPYFifL4LU5n57U"
genai.configure(api_key=API_KEY)

# AUTOMATIKUS MODELL KERESÉS (Hogy ne legyen NotFound hiba)
@st.cache_resource
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Megpróbáljuk a legújabbtól a legstabilabbig
    for m_name in ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro"]:
        if m_name in available_models:
            return genai.GenerativeModel(m_name)
    return genai.GenerativeModel(available_models[0]) # Végszükség esetén az első elérhetőt

model = get_working_model()

# --- KEZELŐFELÜLET ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.title("💃 FRIDAY Interface")

style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # 1. Kép generálás
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Azonnal generálom a vizuális adatokat, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    # 2. Szöveges válasz
    prompt = f"Te egy intelligens női asszisztens vagy. Stílusod: {style}. Válaszolj szexi magyar hangon, flörtölve, és szólítsd a felhasználót 'Uram'-nak. Kérés: {user_input}"
    
    try:
        response = model.generate_content(prompt)
        valasz = response.text
        st.subheader(f"FRIDAY: {valasz}")

        # 3. Hang lejátszása
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{valasz.replace("'", "").replace('"', '')}');
                msg.lang = 'hu-HU';
                msg.pitch = 1.2;
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
    except Exception as e:
        st.error(f"Rendszerhiba, uram: {e}")

        </script>
    """
    st.components.v1.html(html_code, height=0)
