class CommandClassifier:

    def __init__(self):
        self.command_map = {
            "take off": "DRONE_TAKEOFF",
            "takeoff": "DRONE_TAKEOFF",
            "land": "DRONE_LAND",
            "increase altitude": "DRONE_UP",
            "go up": "DRONE_UP",
            "decrease altitude": "DRONE_DOWN",
            "go down": "DRONE_DOWN",
            "move forward": "DRONE_FORWARD",
            "forward": "DRONE_FORWARD",
            "move backward": "DRONE_BACKWARD",
            "backward": "DRONE_BACKWARD",
            "move left": "DRONE_LEFT",
            "move right": "DRONE_RIGHT",
            "stop": "DRONE_STOP",
            "start monitoring": "START_MONITORING"
        }

    def classify(self, text_command):

        if text_command is None:
            return None

        for key in self.command_map:
            if key in text_command:
                return self.command_map[key]

        return "UNKNOWN_COMMAND"