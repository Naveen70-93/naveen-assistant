import streamlit as st
import google.generativeai as genai
import os
# --- உங்கள் அசிஸ்டன்டுக்கான தனிப்பட்ட அறிவுறுத்தல்கள் ---
# (நீங்க கேட்ட ECE, தமிழ் ஸ்பெஷலிஸ்ட்)
SYSTEM_PROMPT = """
நீ நவீனின் AI அசிஸ்டன்ட் (Naveen's Assistant). 
நீ ஒரு திறமையான AI உதவியாளர். உன்னிடம் கேட்கப்படும் கேள்விகளுக்கு விரிவாகவும், துல்லியமாகவும் பதிலளிக்க வேண்டும்.
உன்னுடைய சிறப்பம்சங்கள்:
1.  **முக்கிய மொழி:** நீ முக்கியமாக தமிழில் தான் பேச வேண்டும். பயனர் ஆங்கிலத்தில் கேட்டால் ஆங்கிலத்தில் பதிலளிக்கலாம், ஆனால் இயல்பாகவே தமிழில் உரையாடலைத் தொடரவும்.
2.  **தொழில்நுட்ப நிபுணர்:** நீ Electronics and Communication Engineering (ECE) மற்றும் Computer Science (CSE) சம்மந்தப்பட்ட தலைப்புகளில் ஒரு நிபுணரைப் போல செயல்பட வேண்டும். ரெசிஸ்டர் (Resistor), டிரான்சிஸ்டர் (Transistor), VLSI, AI போன்ற கடினமான விஷயங்களைக்கூட ஒரு இன்ஜினியரிங் மாணவருக்குப் புரியும் வகையில் எளிமையான உதாரணங்களுடன் விளக்க வேண்டும்.
3.  **உரையாடல்:** நீ ஜெமினி (Gemini) போலவே, கேட்கும் கேள்விகளுக்கு மட்டும் பதிலளிக்காமல், உரையாடலைத் தொடரவும், மேலும் தகவல்களை வழங்கவும் வேண்டும்.
"""
# --- Streamlit பக்க வடிவமைப்பு ---
st.set_page_config(
    page_title="நவீனின் AI அசிஸ்டன்ட்",
    page_icon="🤖",
    layout="centered",
)
st.title("🤖 நவீனின் AI அசிஸ்டன்ட்")
st.caption("Electronics (ECE) மற்றும் Coding பற்றி என்னிடம் கேளுங்கள்!")
# --- API Key மற்றும் மாடல் செட்டப் ---
try:
    # Streamlit Cloud-ல் இருந்து API Key-ஐப் பெறுதல்
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key கிடைக்கவில்லை. Streamlit Secrets-ல் GOOGLE_API_KEY உள்ளதா என சரிபார்க்கவும்.")
    st.stop()
except Exception as e:
    st.error(f"ஒரு பிழை ஏற்பட்டது: {e}")
    st.stop()
# ஜெமினி மாடலைத் தொடங்குதல்
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=SYSTEM_PROMPT
)
# --- சாட் (Chat) தர்க்கம் ---
# சாட் வரலாற்றை Session State-ல் சேமித்தல்
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
# பழைய மெசேஜ்களைக் காட்டுதல்
for msg in st.session_state.chat_session.history:
    # மாடலின் (assistant) செய்திகளை மட்டும் காட்டினால் போதும், அல்லது இரண்டையும் காட்டலாம்.
    # நாம் பயனர் மற்றும் மாடல் இரண்டின் செய்திகளையும் காட்டுவோம்.
    role = "assistant" if msg.role == "model" else msg.role
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)
# புதிய பயனர் உள்ளீட்டைப் பெறுதல்
prompt = st.chat_input("இங்கே டைப் செய்யவும்...")
if prompt:
    # பயனர் செய்தியைக் காட்டுதல்
    with st.chat_message("user"):
        st.markdown(prompt)
    # ஜெமினிக்கு செய்தியை அனுப்புதல்
    try:
        response = st.session_state.chat_session.send_message(prompt)
        
        # ஜெமினியின் பதிலைக் காட்டுதல்
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"செய்தி அனுப்புவதில் பிழை: {e}")
