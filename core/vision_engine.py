try:
    import cv2
except (ImportError, OSError) as e:
    # cv2 not available (common on headless systems)
    cv2 = None
    print(f"Warning: cv2 not fully available: {e}")
from ultralytics import YOLO


class VisionEngine:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n.pt")

    def run(self):

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            results = self.model(frame)

            human_count = 0
            vehicle_count = 0
            animal_count = 0
            obstacle_detected = False

            for r in results:
                for box in r.boxes:

                    cls = int(box.cls[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    width = x2 - x1
                    height = y2 - y1

                    if cls == 0:
                        human_count += 1
                        label = "Person"

                    elif cls in [2, 3, 5, 7]:
                        vehicle_count += 1
                        label = "Vehicle"

                    elif cls in [16, 17, 18, 19, 20, 21, 22, 23]:
                        animal_count += 1
                        label = "Animal"

                    else:
                        if width > 150 and height > 150:
                            obstacle_detected = True
                            label = "Obstacle"
                        else:
                            continue

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

            cv2.putText(frame, f"Humans: {human_count}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.putText(frame, f"Animals: {animal_count}", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            if obstacle_detected:
                cv2.putText(frame,
                            "ROAD OBSTACLE ALERT",
                            (150, 200),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            3)

            cv2.imshow("AI Drone Vision System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()