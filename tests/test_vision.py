from core.vision_engine import VisionEngine
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
vision = VisionEngine()

vision.run()