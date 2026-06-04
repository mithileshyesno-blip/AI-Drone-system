from core.speech_recognition_module import SpeechRecognizer

from core.command_classifier import CommandClassifier

from core.drone_command_executor import DroneCommandExecutor
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)



speech = SpeechRecognizer()

classifier = CommandClassifier()

executor = DroneCommandExecutor()


while True:

    text = speech.listen_command()

    command = classifier.classify(text)

    print("Detected Command:",
          command)

    executor.execute(command)

    if command == "DRONE_STOP":

        print("Drone System Stopped")

        break