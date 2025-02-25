# app.py
import streamlit as st
import threading
import time
from queue import Queue
from transcription import transcribe_audio
from translation import translate_text
from gtts import gTTS
import os
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# Custom CSS for styling
custom_css = """
<style>
.stApp {
    background-color: #ffffff;
    font-family: 'Arial', sans-serif;
    color: #000000;
}
.stSelectbox > div > div > div {
    border: 2px solid #000000;
    border-radius: 5px;
    padding: 5px;
}
.stButton > button {
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    margin: 5px;
}
.stButton > button:hover {
    background-color: #333333;
}
.stTextArea > div > div > textarea {
    border: 2px solid #000000;
    border-radius: 5px;
    font-size: 16px;
    margin: 10px 0;
    padding: 10px;
    background-color: #000000;
    color: white;
}
.stAlert {
    margin-top: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Ensure the color name is valid
valid_colors = [
    "blue", "green", "orange", "red", "violet", "yellow", "gray", "black", "white"
]

color_name = "blue-70"  # Correct format

if color_name.split('-')[0] not in valid_colors or not color_name.split('-')[1].isdigit():
    st.error(f"Invalid color name: {color_name}. Please choose from {valid_colors} with intensity (e.g., 'blue-70').")
else:
    colored_header(
        label="Healthcare Translation Web App",
        description="Translate spoken input in real-time with accurate transcription and audio playback.",
        color_name=color_name
    )

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

# Queue for communication between threads
queue = Queue()

def update_transcripts():
    while st.session_state.transcribing:
        text = transcribe_audio()
        if text:
            queue.put(text)
            time.sleep(1)  # Sleep to avoid excessive reruns

def start_transcription():
    st.session_state.transcribing = True
    threading.Thread(target=update_transcripts).start()

def stop_transcription():
    st.session_state.transcribing = False

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Transcription"):
        start_transcription()
with col2:
    if st.button("Stop Transcription"):
        stop_transcription()

add_vertical_space(2)

with st.spinner("Transcribing...") if st.session_state.transcribing else st.empty():
    st.text_area("Original Transcript", value=st.session_state.original_transcript, height=200, key="original")
    st.text_area("Translated Transcript", value=st.session_state.translated_transcript, height=200, key="translated")

add_vertical_space(2)

def play_audio(text):
    if not text.strip():
        st.warning("No text to speak.")
        return
    tts = gTTS(text=text, lang=output_language.lower())
    tts.save("output.mp3")
    st.audio("output.mp3", format='audio/mp3')
    os.remove("output.mp3")

if st.button("Speak Translated Text"):
    play_audio(st.session_state.translated_transcript)

# Add a section for error messages
if st.session_state.get('error_message'):
    st.error(st.session_state.error_message)

# Process the queue in the main thread
while not queue.empty():
    text = queue.get()
    if text:
        st.session_state.original_transcript += f"{text} "
        translated_text = translate_text(text, model_name)
        if translated_text:
            st.session_state.translated_transcript += f"{translated_text} "
    st.experimental_rerun()