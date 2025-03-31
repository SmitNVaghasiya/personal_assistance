from speech_recognition_module import voice_recognition
from command_handler import handle_command

if __name__ == '__main__':
    while True:
        text = voice_recognition()
        handle_command(text)