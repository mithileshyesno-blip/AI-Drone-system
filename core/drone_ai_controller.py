from core.drone_decision_engine import DroneDecisionEngine


class DroneAIController:

    def __init__(self):

        self.decision_engine = DroneDecisionEngine()

    def process_target(self,
                       target_x,
                       frame_center_x,
                       obstacle=False):

        decision = self.decision_engine.decide(
            target_x,
            frame_center_x,
            obstacle=obstacle
        )

        print("AI Decision:", decision)

        return decision