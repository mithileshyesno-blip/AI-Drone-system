class DroneSimulator:

    def __init__(self):
        self.altitude = 0
        self.is_flying = False

    def execute(self, command):

        if command == "DRONE_TAKEOFF":
            self.takeoff()

        elif command == "DRONE_LAND":
            self.land()

        elif command == "DRONE_UP":
            self.altitude += 1
            print("Drone going UP. Altitude:", self.altitude)

        elif command == "DRONE_DOWN":
            self.altitude -= 1
            print("Drone going DOWN. Altitude:", self.altitude)

        elif command == "DRONE_FORWARD":
            print("Drone moving FORWARD")

        elif command == "DRONE_BACKWARD":
            print("Drone moving BACKWARD")

        elif command == "DRONE_LEFT":
            print("Drone moving LEFT")

        elif command == "DRONE_RIGHT":
            print("Drone moving RIGHT")

        elif command == "DRONE_STOP":
            print("Drone STOPPED")

        else:
            print("Unknown drone command")

    def takeoff(self):
        if not self.is_flying:
            self.is_flying = True
            self.altitude = 1
            print("Drone TAKING OFF")

    def land(self):
        if self.is_flying:
            self.is_flying = False
            self.altitude = 0
            print("Drone LANDING")