class DroneCommandExecutor:

    def __init__(self):

        self.altitude = 0

    def execute(self, command):

        if command == "FOLLOW_FORWARD":

            print("AI: Following Target")

        elif command == "MOVE_LEFT":

            print("AI: Moving Left")

        elif command == "MOVE_RIGHT":

            print("AI: Moving Right")

        elif command == "MOVE_UP":

            print("AI: Moving Up")

        elif command == "MOVE_BACK":

            print("AI: Moving Back")

        elif command == "SEARCH_TARGET":

            print("AI: Searching Target")

        elif command == "STOP_FOR_OBSTACLE":

            print("AI: Obstacle Detected")

        else:

            print("Manual:", command)