import speech_recognition as sr

def voice_recognition():
    """
    Listens for speech, recognizes it using Google Speech Recognition, and returns the text.
    Keeps listening until valid speech is detected.
    """
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust for noise

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text

            except sr.UnknownValueError:
                print("Could not understand the audio, please try again.")
                continue

            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue

            except sr.WaitTimeoutError:
                print("No speech detected, still listening...")
                continue