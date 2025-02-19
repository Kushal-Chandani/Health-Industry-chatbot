# transcription.py
import speech_recognition as sr

def transcribe_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            text = recognizer.recognize_google(audio)
            print(f"Transcribed: {text}")
            return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None