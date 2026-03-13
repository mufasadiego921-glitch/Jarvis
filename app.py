import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACIO
# IDE MASOLD BE AZ API KULCSODAT A KET MACSKAKOROM KOZE!
API_KEY = "AIzaSyAY6JCFR4eJ5Bqgkt4tkPYFifL4LU5n57U"
genai.configure(api_key=API_KEY)

# A legstabilabb modell kivalasztasa
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.title("💃 FRIDAY Interface")

style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

# 2. INTERAKCIO
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # Kep generalas
    if any(x in user_input.lower() for x in ["kep", "generalj", "foto"]):
        st.write("Azonnal generalom a vizualis adatokat, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    # Szoveges valasz
    prompt = f"Te egy intelligens noi asszisztens vagy. Stilusa: {style}. Valaszolj szexi magyar hangon, flortolve, es szolids a felhasznalot 'Uram'-nak. Kerdes: {user_input}"
    
    try:
        response = model.generate_content(prompt)
        valasz = response.text
        st.subheader(f"FRIDAY: {valasz}")

        # Hang lejatszasa
        clean_valasz = valasz.replace("'", "").replace('"', '').replace("\n", " ")
        html_code = f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_valasz}");
                msg.lang = 'hu-HU';
                msg.pitch = 1.2;
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(html_code, height=0)
    except Exception as e:
        st.error(f"Hiba tortent: {e}")
