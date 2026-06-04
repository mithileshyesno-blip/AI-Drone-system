import numpy as np


class Sort:

    def __init__(self):

        self.next_id = 1

        self.tracks = {}

    def update(self, detections):

        results = []

        for det in detections:

            x1, y1, x2, y2, _ = det

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            assigned_id = None

            for track_id, (px, py) in self.tracks.items():

                distance = np.sqrt(
                    (cx - px) ** 2 +
                    (cy - py) ** 2
                )

                if distance < 50:

                    assigned_id = track_id

                    break

            if assigned_id is None:

                assigned_id = self.next_id

                self.next_id += 1

            self.tracks[assigned_id] = (cx, cy)

            results.append([
                x1,
                y1,
                x2,
                y2,
                assigned_id
            ])

        return np.array(results)