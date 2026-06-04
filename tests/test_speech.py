from core.speech_recognition_module import SpeechRecognizer
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from core.voice_auth import VoiceAuthenticator

sr_engine = SpeechRecognizer()

while True:
    cmd = sr_engine.listen_command()

    if cmd:
        print("Command:", cmd)

    if cmd == "stop":
        print("Stopping test...")
        break