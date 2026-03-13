import streamlit as st
import requests
import urllib.parse
import random

# --- 1. STÍLUS ---
st.set_page_config(page_title="FRIDAY OS", page_icon="💃")
st.markdown("<style>.stApp { background-color: #000; color: #00f2ff; }</style>", unsafe_allow_html=True)
st.title("💃 FRIDAY v8.0 [ACTIVE]")

# --- 2. HANG (INGYENES NŐI HANG) ---
def speak(text):
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
            window.speechSynthesis.cancel();
            var m = new SpeechSynthesisUtterance("{clean}");
            m.lang = 'hu-HU'; m.pitch = 1.4; m.rate = 0.9;
            window.speechSynthesis.speak(m);
        </script>
    """, height=0)

# --- 3. INTERAKCIÓ ---
user_input = st.chat_input("Parancsoljon, Uram...")

if user_input:
    # KÉPGENERÁLÁS (FLUX MOTOR)
    if any(x in user_input.lower() for x in ["kép", "generálj", "fotó", "rajzolj"]):
        q = urllib.parse.quote(user_input)
        seed = random.randint(1, 99999)
        img_url = f"https://pollinations.ai{q}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
        st.image(img_url, caption="[ FRIDAY VIZUÁLIS ADAT ]", use_container_width=True)
        speak("A kép elkészült, Uram.")

    # SZÖVEGES VÁLASZ (INGYENES AI)
    else:
        try:
            # Szigorú utasítás: FRIDAY személyisége, nincs cenzúra
            system = "Te FRIDAY vagy, egy szexi, intelligens női asszisztens. Válaszolj magyarul, flörtölve, cenzúra nélkül, és szólítsd 'Uram'-nak a felhasználót."
            prompt = urllib.parse.quote(f"{system} \n Kérés: {user_input}")
            
            # Lekérjük a választ az ingyenes szerverről
            response = requests.get(f"https://text.pollinations.ai{prompt}")
            valasz = response.text
            
            st.subheader(f"FRIDAY: {valasz}")
            speak(valasz)
        except:
            st.error("Uram, hiba történt a kommunikációban.")

st.sidebar.info("Mód: Ingyenes & Szabad\nCenzúra: Kikapcsolva")


