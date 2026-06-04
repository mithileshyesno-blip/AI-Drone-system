import os
import numpy as np
import librosa
import soundfile as sf


class VoiceAuthenticator:

    def __init__(self, registered_path=r"data\registered_voices"):
        self.registered_path = registered_path
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

        for file in os.listdir(self.registered_path):

            if file.startswith("auth") and file.endswith(".wav"):

                full_path = os.path.join(self.registered_path, file)

                print("Loading:", file)

                features = self.extract_features(full_path)

                database.append(features)

        print("Total auth voices loaded:", len(database))

        return database

    def authenticate(self, input_voice_file):

        input_features = self.extract_features(input_voice_file)

        for stored_features in self.voice_database:

            distance = np.linalg.norm(input_features - stored_features)

            if distance < 60:
                return True

        return False