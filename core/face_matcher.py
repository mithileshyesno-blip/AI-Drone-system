try:
    import numpy as np
except ImportError as e:
    raise ImportError(f"NumPy is required but not installed: {e}")

try:
    import cv2
except (ImportError, OSError) as e:
    # cv2 not available (common on headless systems)
    cv2 = None
    print(f"Warning: cv2 not fully available: {e}")

import os


class FaceMatcher:

    def __init__(self, face_dir="data/known_faces"):

        self.known_faces = []

        if not os.path.exists(face_dir):
            return

        for file in os.listdir(face_dir):

            path = os.path.join(
                face_dir,
                file
            )

            img = cv2.imread(path)

            if img is None:
                continue

            img = cv2.resize(img, (100, 100))

            img = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            self.known_faces.append(img)

    def match(self, face_img):

        if face_img.size == 0:
            return False

        face_img = cv2.resize(
            face_img,
            (100, 100)
        )

        face_img = cv2.cvtColor(
            face_img,
            cv2.COLOR_BGR2GRAY
        )

        for known in self.known_faces:

            diff = cv2.absdiff(
                known,
                face_img
            )

            score = np.mean(diff)

            if score < 35:
                return True

        return False