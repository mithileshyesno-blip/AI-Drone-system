class DashboardData:

    def __init__(self):

        self.human_count = 0
        self.vehicle_count = 0
        self.animal_count = 0

        self.drone_status = "IDLE"

        self.ai_decision = "WAITING"

        self.target_locked = False

    def update_humans(self, count):

        self.human_count = count

    def update_vehicles(self, count):

        self.vehicle_count = count

    def update_animals(self, count):

        self.animal_count = count

    def update_status(self, status):

        self.drone_status = status

    def update_decision(self, decision):

        self.ai_decision = decision

    def lock_target(self):

        self.target_locked = True

    def unlock_target(self):

        self.target_locked = False