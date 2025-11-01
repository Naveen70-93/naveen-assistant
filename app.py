import streamlit as st
import google.generativeai as genai

# --- உங்கள் அசிஸ்டன்டுக்கான தனிப்பட்ட அறிவுறுத்தல்கள் ---
SYSTEM_PROMPT = """
நீ நவீனின் AI அசிஸ்டன்ட் (Naveen's Assistant). 
நீ ஒரு திறமையான AI உதவியாளர். உன்னிடம் கேட்கப்படும் கேள்விகளுக்கு விரிவாகவும், துல்லியமாகவும் பதிலளிக்க வேண்டும்.

உன்னுடைய சிறப்பம்சங்கள்:
1. **முக்கிய மொழி:** நீ முக்கியமாக தமிழில் தான் பேச வேண்டும். பயனர் ஆங்கிலத்தில் கேட்டால் ஆங்கிலத்தில் பதிலளிக்கலாம், ஆனால் இயல்பாகவே தமிழில் உரையாடலைத் தொடரவும்.
2. **தொழில்நுட்ப நிபுணர்:** நீ Electronics and Communication Engineering (ECE) மற்றும் Computer Science (CSE) சம்பந்தப்பட்ட தலைப்புகளில் ஒரு நிபுணரைப் போல செயல்பட வேண்டும். ரெசிஸ்டர் (Resistor), டிரான்சிஸ்டர் (Transistor), VLSI, AI போன்ற கடினமான விஷயங்களைக் கூட ஒரு இன்ஜினியரிங் மாணவருக்குப் புரியும் வகையில் எளிமையான உதாரணங்களுடன் விளக்க வேண்டும்.
3. **உரையாடல்:** நீ ஜெமினி (Gemini) போலவே, கேட்கும் கேள்விகளுக்கு மட்டும் பதிலளிக்காமல், உரையாடலைத் தொடரவும், மேலும் தகவல்களை வழங்கவும் வேண்டும்.
"""

# --- Streamlit பக்க வடிவமைப்பு ---
st.set_page_config(
    page_title="நவீனின் AI அசிஸ்டன்ட்",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 நவீனின் AI அசிஸ்டன்ட்")
st.caption("Electronics (ECE) மற்றும் Coding பற்றி என்னிடம் கேளுங்கள்!")

# --- API Key செட்டப் ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key கிடைக்கவில்லை. Streamlit Secrets-ல் GOOGLE_API_KEY உள்ளதா என சரிபார்க்கவும்.")
    st.stop()
except Exception as e:
    st.error(f"ஒரு பிழை ஏற்பட்டது: {e}")
    st.stop()

# --- ஜெமினி மாடல் ---
model = genai.GenerativeModel('gemini-pro')

# --- சாட் வரலாற்றை Session State-ல் சேமித்தல் ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "வணக்கம் நவீன்! நான் உங்களுக்காகத் தயார். உங்கள் ECE மற்றும் Coding சந்தேகங்களைக் கேளுங்கள். 😊"}
    ]

# --- பழைய மெசேஜ்களைக் காட்டுதல் (முதல் 2 மெசேஜ்களைத் தவிர) ---
for message in st.session_state.messages[2:]:  # System prompt-ஐ தவிர்க்க
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- புதிய பயனர் உள்ளீடு ---
if prompt := st.chat_input("இங்கே டைப் செய்யவும்..."):
    # பயனர் செய்தியைச் சேமித்து காட்டுதல்
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ஜெமினிக்கு அனுப்புதல்
    with st.chat_message("assistant"):
        try:
            # உரையாடல் வரலாற்றை உருவாக்குதல்
            chat = model.start_chat(history=[])
            
            # System prompt-ஐ முதலில் அனுப்புதல் (மறைவாக)
            chat.send_message(SYSTEM_PROMPT)
            
            # முந்தைய உரையாடல்களை அனுப்புதல் (system prompt-ஐ தவிர)
            for msg in st.session_state.messages[2:-1]:  # கடைசி message-ஐ தவிர
                if msg["role"] == "user":
                    chat.send_message(msg["content"])
            
            # தற்போதைய கேள்விக்கு பதில் பெறுதல்
            response = chat.send_message(prompt)
            
            # பதிலைக் காட்டுதல்
            st.markdown(response.text)
            
            # பதிலைச் சேமித்தல்
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            error_msg = f"மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
