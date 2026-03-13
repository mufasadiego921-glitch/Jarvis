import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURÁCIÓ ---
# IDE MÁSOLD BE AZ API KULCSODAT!
API_KEY = "AIzaSyAY6JCFR4eJ5Bqgkt4tkPYFifL4LU5n57U"
genai.configure(api_key=API_KEY)

# Modell kiválasztása (stabil verzió)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.title("💃 FRIDAY Interface")

style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# --- 2. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # Kép generálás
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó"]):
        st.write("Azonnal generálom a vizuális adatokat, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    # Szöveges válasz összeállítása
    prompt = f"Te egy intelligens női asszisztens vagy. Stílusod: {style}. Válaszolj szexi magyar hangon, flörtölve, és szólítsd a felhasználót 'Uram'-nak. Kérés: {user_input}"
    
    try:
        response = model.generate_content(prompt)
        valasz = response.text
        st.subheader(f"FRIDAY: {valasz}")

        # Hang lejátszása (Javascript trükk)
        clean_valasz = valasz.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_valasz}');
                msg.lang = 'hu-HU';
                msg.pitch = 1.2;
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
    except Exception as e:
        st.error(f"Hiba történt: {e}")
