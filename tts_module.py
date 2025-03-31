import pyttsx3

def speak(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    # print(voices[1].name)
    # print(voices[1].id)
    engine.setProperty('voice', voices[1].id) # This the voice of david which i likes

    engine.setProperty('rate', 192) # This rate of speed feels like natural
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait() # This is mendatory to keep alive the engine until text is not spoken