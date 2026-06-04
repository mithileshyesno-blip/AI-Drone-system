import sys
import os
from core.command_classifier import CommandClassifier

sys.path.append

os.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


clf = CommandClassifier()

while True:
    cmd = input("Speak text (simulate): ")

    result = clf.classify(cmd)

    print("Drone Command:", result)

    if cmd == "exit":
        break