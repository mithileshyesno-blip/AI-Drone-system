from core.drone_decision_engine import DroneDecisionEngine
from core.drone_command_executor import DroneCommandExecutor


class MissionManager:

    def __init__(self):

        self.decision_engine = DroneDecisionEngine()

        self.executor = DroneCommandExecutor()

    def process(self,
                target_x,
                frame_center_x,
                obstacle=False):

        decision = self.decision_engine.decide(
            target_x,
            frame_center_x,
            obstacle=obstacle
        )

        print("Mission Decision:",
              decision)

        self.executor.execute(decision)

        return decision