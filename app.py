# app.py
import streamlit as st
import threading
import time
from transcription import transcribe_audio
from translation import translate_text
from gtts import gTTS
import os

# Custom CSS for styling
custom_css = """
<style>
.stApp {
    background-color: #f0f2f6;
    font-family: Arial, sans-serif;
}
.stTextInput > div > div > input {
    border: 2px solid #007bff;
    border-radius: 5px;
}
.stButton > button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #0056b3;
}
.stTextArea > div > div > textarea {
    border: 2px solid #007bff;
    border-radius: 5px;
    font-size: 16px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Healthcare Translation Web App")

input_language = st.selectbox("Input Language", ["English", "Spanish"])
output_language = st.selectbox("Output Language", ["Spanish", "English"])

if input_language == "English" and output_language == "Spanish":
    model_name = "Helsinki-NLP/opus-mt-en-es"
elif input_language == "Spanish" and output_language == "English":
    model_name = "Helsinki-NLP/opus-mt-es-en"
else:
    st.error("Unsupported language pair. Please select English-Spanish or Spanish-English.")
    model_name = None

# Initialize session state variables
if 'original_transcript' not in st.session_state:
    st.session_state.original_transcript = ""
if 'translated_transcript' not in st.session_state:
    st.session_state.translated_transcript = ""
if 'transcribing' not in st.session_state:
    st.session_state.transcribing = False

def update_transcripts():
    while st.session_state.transcribing:
        text = transcribe_audio()
        if text:
            st.session_state.original_transcript += f"{text} "
            translated_text = translate_text(text, model_name)
            st.session_state.translated_transcript += f"{translated_text} "
            st.experimental_rerun()

if st.button("Start Transcription"):
    st.session_state.transcribing = True
    threading.Thread(target=update_transcripts).start()

if st.button("Stop Transcription"):
    st.session_state.transcribing = False

with st.spinner("Transcribing..."):
    st.text_area("Original Transcript", value=st.session_state.original_transcript, height=200, key="original")
    st.text_area("Translated Transcript", value=st.session_state.translated_transcript, height=200, key="translated")

def play_audio(text):
    tts = gTTS(text=text, lang=output_language.lower())
    tts.save("output.mp3")
    st.audio("output.mp3", format='audio/mp3')
    os.remove("output.mp3")

if st.button("Speak Translated Text"):
    play_audio(st.session_state.translated_transcript)

# Add a section for error messages
if st.session_state.get('error_message'):
    st.error(st.session_state.error_message)