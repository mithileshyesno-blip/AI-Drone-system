from core.vision_engine import VisionEngine
from core.mission_manager import MissionManager


class AutonomousDroneSystem:

    def __init__(self):

        self.vision = VisionEngine()

        self.mission = MissionManager()

    def start(self):

        print("Autonomous Drone System Started")

        self.vision.run()