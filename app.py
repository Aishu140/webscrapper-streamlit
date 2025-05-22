import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Configure Gemini API key
genai.configure(api_key="AIzaSyAvMKtbmGRUvgaKU5E02Wv4jqt9Rke7OEM")

# Initialize the Gemini model correctly (no .from_pretrained())
model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"

def text_to_speech(text):
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

st.title("AI Voice Bot (Text-to-Speech)")

input_method = st.radio("Choose input method:", ["Text"])

if input_method == "Text":
    user_input = st.text_input("Type your message here:")

    if user_input:
        st.write("You said:", user_input)
        with st.spinner("Getting response..."):
            response = get_gemini_response(user_input)
        st.success(response)

        audio_data = text_to_speech(response)
        st.audio(audio_data, format="audio/mp3")
