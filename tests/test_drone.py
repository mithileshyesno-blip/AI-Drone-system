from core.command_classifier import CommandClassifier
from core.drone_simulator import DroneSimulator
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

clf = CommandClassifier()
drone = DroneSimulator()

while True:
    text = input("Command: ")

    if text == "exit":
        break

    cmd = clf.classify(text)
    drone.execute(cmd)