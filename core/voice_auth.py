import os
import numpy as np
import librosa
import soundfile as sf


class VoiceAuthenticator:

    def __init__(self, registered_path=r"data\registered_voices"):
        self.registered_path = os.path.normpath(registered_path)
        if not os.path.isdir(self.registered_path):
            os.makedirs(self.registered_path, exist_ok=True)
        self.voice_database = self.load_registered_voices()

    def extract_features(self, file_path):
        audio, sr = sf.read(file_path)

        # stereo to mono
        if len(audio.shape) > 1:
            audio = audio[:, 0]

        # limit to 2 sec
        audio = audio[:sr * 2]

        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        return np.mean(mfcc, axis=1)

    def load_registered_voices(self):

        database = []

        print("Reading registered auth voice files...")

        if not os.path.isdir(self.registered_path):
            print(f"Registered voice folder does not exist, creating: {self.registered_path}")
            return database

        for file in os.listdir(self.registered_path):
            if file.lower().endswith(".wav"):
                full_path = os.path.join(self.registered_path, file)
                print("Loading:", file)
                try:
                    features = self.extract_features(full_path)
                    database.append(features)
                except Exception as e:
                    print(f"Failed to load {file}: {e}")

        print("Total auth voices loaded:", len(database))
        return database

    def authenticate(self, input_voice_file):
        if not self.voice_database:
            raise FileNotFoundError(
                f"No registered voice samples found in '{self.registered_path}'. "
                "Please add 'auth_*.wav' files to the directory."
            )

        input_features = self.extract_features(input_voice_file)

        for stored_features in self.voice_database:

            distance = np.linalg.norm(input_features - stored_features)

            if distance < 60:
                return True

        return False