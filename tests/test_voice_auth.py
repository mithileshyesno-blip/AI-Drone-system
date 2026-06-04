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


auth = VoiceAuthenticator()

voice_folder = "data/registered_voices"

for file in os.listdir(voice_folder):

    if file.endswith(".wav"):

        test_file = os.path.join(
            voice_folder,
            file
        )

        print("\nTesting:", file)

        if auth.authenticate(test_file):

            print("ACCESS GRANTED")

        else:

            print("ACCESS DENIED")