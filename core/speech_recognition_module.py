import speech_recognition as sr


class SpeechRecognizer:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8

    def listen_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            command = command.lower()
            print("Recognized:", command)
            return command

        except sr.UnknownValueError:
            print("Speech not understood")
            return None

        except sr.RequestError:
            print("Speech service error")
            return None