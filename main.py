from groq_module import groq_response
from tts_module import speak
from speech_recognition_module import voice_recognition
from file_search_module import search_and_open_file

if __name__ == '__main__':
    while True:
        text = voice_recognition()
        if text:
            if text.lower().startwith('search for '):
                filename = text[10:].strip()
                if filename:
                    response = search_and_open_file(filename)
                else:
                    response = "Please specify a filename to search for."
            else:
                response = groq_response(text)
                speak(response)
