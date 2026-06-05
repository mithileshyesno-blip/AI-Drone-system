try:
    import cv2
except (ImportError, OSError) as e:
    # cv2 not available (common on headless systems)
    cv2 = None
    print(f"Warning: cv2 not fully available: {e}")
from ultralytics import YOLO


class StreamlitCamera:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

        self.cap = cv2.VideoCapture(0)

    def get_frame(self):

        success, frame = self.cap.read()

        if not success:

            return None, 0, 0, 0

        results = self.model(frame)

        human_count = 0
        vehicle_count = 0
        animal_count = 0

        vehicle_classes = [2, 3, 5, 7]
        animal_classes = [15, 16, 17, 18, 19]

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                if cls == 0:

                    human_count += 1

                    label = "Human"

                elif cls in vehicle_classes:

                    vehicle_count += 1

                    label = "Vehicle"

                elif cls in animal_classes:

                    animal_count += 1

                    label = "Animal"

                else:

                    continue

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return (
            frame,
            human_count,
            vehicle_count,
            animal_count
        )