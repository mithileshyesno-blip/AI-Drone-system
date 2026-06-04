class DroneDecisionEngine:

    def decide(self,
               target_cx,
               frame_cx,
               collision=False,
               obstacle=False):

        if collision:
            return "MOVE_BACK"

        if obstacle:
            return "MOVE_UP"

        if target_cx is None:
            return "SEARCH_TARGET"

        if target_cx < frame_cx - 50:
            return "MOVE_LEFT"

        elif target_cx > frame_cx + 50:
            return "MOVE_RIGHT"

        else:
            return "FOLLOW_FORWARD"