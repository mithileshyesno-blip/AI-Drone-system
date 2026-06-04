from core.voice_auth import VoiceAuthenticator
from core.vision_engine import VisionEngine


def voice_authentication():

    auth = VoiceAuthenticator()

    test_file = input(
        "\nEnter voice file path: "
    ).strip()

    if auth.authenticate(test_file):

        print("\nACCESS GRANTED")

    else:

        print("\nACCESS DENIED")


def voice_control():

    from core.speech_recognition_module import (
        SpeechRecognizer
    )

    from core.command_classifier import (
        CommandClassifier
    )

    from core.drone_command_executor import (
        DroneCommandExecutor
    )

    speech = SpeechRecognizer()

    classifier = CommandClassifier()

    executor = DroneCommandExecutor()

    while True:

        text = speech.listen_command()

        command = classifier.classify(text)

        print(
            "\nDetected Command:",
            command
        )

        executor.execute(command)

        if command == "DRONE_STOP":

            print(
                "\nVoice Control Stopped"
            )

            break


def vision_system():

    vision = VisionEngine()

    vision.run()


def autonomous_mode():

    from core.autonomous_drone_system import (
        AutonomousDroneSystem
    )

    system = AutonomousDroneSystem()

    system.start()


def show_menu():

    print("\n")
    print("=" * 50)
    print("        AI DRONE SYSTEM")
    print("=" * 50)
    print("1. Voice Authentication")
    print("2. Voice Control")
    print("3. Vision System")
    print("4. Autonomous Mode")
    print("5. Exit")
    print("=" * 50)


def main():

    while True:

        show_menu()

        choice = input(
            "\nSelect Option: "
        ).strip()

        if choice == "1":

            voice_authentication()

        elif choice == "2":

            voice_control()

        elif choice == "3":

            vision_system()

        elif choice == "4":

            autonomous_mode()

        elif choice == "5":

            print(
                "\nExiting AI Drone System..."
            )

            break

        else:

            print(
                "\nInvalid Option. Try Again."
            )


if __name__ == "__main__":

    main()