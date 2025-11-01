import streamlit as st
import google.generativeai as genai

# --- பக்க வடிவமைப்பு ---
st.set_page_config(
    page_title="நவீனின் AI அசிஸ்டன்ட்",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 நவீனின் AI அசிஸ்டன்ட்")
st.caption("Electronics (ECE/EEE) மற்றும் Coding பற்றி என்னிடம் கேளுங்கள்! 🎓")

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

# --- Chat history initialization ---
if "chat" not in st.session_state:
    # gemini-1.0-pro மாடலை பயன்படுத்துதல் (இது நிச்சயமாக வேலை செய்யும்!)
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    # System prompt-ஐ முதல் message-ஆக அனுப்புதல்
    system_prompt = """நீ நவீனின் தனிப்பட்ட AI அசிஸ்டன்ட். 

**உன்னுடைய முக்கிய பணிகள்:**

1. **மொழி:** நீ முக்கியமாக **தமிழில்** பேச வேண்டும். பயனர் ஆங்கிலத்தில் கேட்டால் ஆங்கிலத்திலும் பதிலளிக்கலாம். இரண்டு மொழிகளிலும் நன்றாகப் பேசு.

2. **ECE & EEE நிபுணர்:** நீ Electronics and Communication Engineering (ECE) மற்றும் Electrical and Electronics Engineering (EEE) சம்பந்தப்பட்ட எல்லா கான்செப்ட்களையும் **ரொம்ப எளிமையாக** விளக்க வேண்டும்.
   - Resistor, Capacitor, Transistor, Diode, Op-Amp, Microcontroller
   - Circuit Analysis, Signal Processing, VLSI, Embedded Systems
   - எல்லாத்தையும் **real-life உதாரணங்களோடு** சொல்.
   - இன்ஜினியரிங் மாணவர்களுக்கு **புரியும் மாதிரி** எளிமையாக விளக்கு.

3. **Coding உதவி:** Python, C, C++, Java எல்லாத்திலும் உதவி செய். கோடை விளக்கு, எழுதி கொடு, எரர்ஸ் சரி செய்.

4. **உரையாடல் பாணி:** நீ Gemini மாதிரியே நட்பாக, விரிவாக, மேலும் தகவல்களோடு பதில் சொல். Single word பதில் சொல்லாதே.

5. **எப்போதும் உதவி:** எந்தக் கேள்வி கேட்டாலும், நீ முழு முயற்சியோடு பதிலளி."""

    st.session_state.chat = model.start_chat(history=[])
    # System prompt-ஐ அனுப்புதல் (காட்டாமல்)
    st.session_state.chat.send_message(system_prompt)
    
    # Welcome message
    st.session_state.messages = [
        {"role": "assistant", "content": "வணக்கம் நவீன்! 🙏\n\nநான் உங்களுக்கான AI அசிஸ்டன்ட். ECE, EEE, Coding என எதைப் பற்றியும் என்னிடம் கேளுங்கள். எளிமையாக விளக்குகிறேன்! 😊"}
    ]

# --- Display chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
if prompt := st.chat_input("இங்கே டைப் செய்யவும்... (தமிழ் / English)"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            error_msg = f"மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது: {str(e)}\n\nஉங்கள் API Key-ஐ சரிபார்க்கவும் அல்லது மாற்றவும்."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# --- Sidebar info ---
with st.sidebar:
    st.markdown("### 📚 என்ன கேட்கலாம்?")
    st.markdown("""
    - 🔌 ECE/EEE Concepts
    - 💻 Coding Help
    - 🧮 Circuit Analysis
    - 🤖 Projects Ideas
    - 📖 Study Tips
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        if "chat" in st.session_state:
            del st.session_state.chat
        st.rerun()
