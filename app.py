import streamlit as st
import google.generativeai as genai

# IDE MÁSOLD BE AZ API KULCSODAT A "" KÖZÉ!
API_KEY = "IDE_JÖN_AZ_API_KULCSOD"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("💃 FRIDAY Interface")

# Stílusválasztó
style = st.sidebar.selectbox("Hangulat:", ["Szexi & Kedves", "Szigorú Domináns", "Hűséges Asszisztens", "Pimasz"])

user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    prompt = f"Te egy gyönyörű, intelligens női asszisztens vagy. Stílusod: {style}. Válaszolj szexi magyar hangon, flörtölve, és szólítsd a felhasználót 'Uram'-nak. Kérés: {user_input}"
    
    if "kép" in user_input.lower():
        st.write("Azonnal generálom a vizuális adatokat, Uram...")
        img_url = f"https://pollinations.ai{user_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(img_url)
    
    response = model.generate_content(prompt)
    valasz = response.text
    st.subheader(f"FRIDAY: {valasz}")

    # Női hang kód
    html_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{valasz}');
            msg.lang = 'hu-HU';
            msg.pitch = 1.2;
            msg.rate = 0.9;
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(html_code, height=0)
