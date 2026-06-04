import streamlit as st
import cv2
from ultralytics import YOLO

from core.voice_auth import VoiceAuthenticator
from core.command_classifier import CommandClassifier
from core.drone_command_executor import DroneCommandExecutor


st.set_page_config(
    page_title="AI Drone System",
    page_icon="🚁",
    layout="wide"
)


st.title("AI Drone Surveillance System")

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Home",
        "Live Vision",
        "Voice Authentication",
        "Voice Control",
        "Autonomous Mode"
    ]
)


# =========================
# HOME
# =========================

if menu == "Home":

    st.header("AI Drone Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Humans",
            value="0"
        )

    with col2:
        st.metric(
            label="Vehicles",
            value="0"
        )

    with col3:
        st.metric(
            label="Animals",
            value="0"
        )

    st.markdown("---")

    st.subheader("Drone Status")

    st.success("READY")

    st.subheader("AI Decision")

    st.info("WAITING FOR INPUT")


# =========================
# VOICE AUTHENTICATION
# =========================

elif menu == "Voice Authentication":

    st.header("Voice Authentication")

    voice_path = st.text_input(
        "Enter Voice File Path"
    )

    if st.button("Authenticate"):

        try:

            auth = VoiceAuthenticator()

            result = auth.authenticate(
                voice_path
            )

            if result:

                st.success(
                    "ACCESS GRANTED"
                )

            else:

                st.error(
                    "ACCESS DENIED"
                )

        except Exception as ex:

            st.error(str(ex))


# =========================
# VOICE CONTROL
# =========================

elif menu == "Voice Control":

    st.header("Voice Command Control")

    command_text = st.text_input(
        "Enter Command"
    )

    if st.button("Execute Command"):

        classifier = CommandClassifier()

        executor = DroneCommandExecutor()

        command = classifier.classify(
            command_text
        )

        st.write(
            "Detected Command:",
            command
        )

        executor.execute(command)

        st.success(
            f"Executed: {command}"
        )


# =========================
# LIVE VISION
# =========================

elif menu == "Live Vision":

    st.header("Live AI Vision")

    start_camera = st.button(
        "Start Camera"
    )

    if start_camera:

        model = YOLO(
            "yolov8n.pt"
        )

        cap = cv2.VideoCapture(0)

        frame_window = st.image([])

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            results = model(frame)

            human_count = 0
            vehicle_count = 0
            animal_count = 0

            vehicle_classes = [
                2,
                3,
                5,
                7
            ]

            animal_classes = [
                15,
                16,
                17,
                18,
                19
            ]

            for result in results:

                for box in result.boxes:

                    cls = int(
                        box.cls[0]
                    )

                    confidence = float(
                        box.conf[0]
                    )

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    label = ""

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
                        f"{label} {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

            cv2.putText(
                frame,
                f"Humans: {human_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Vehicles: {vehicle_count}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Animals: {animal_count}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame_window.image(
                frame,
                channels="RGB"
            )

        cap.release()


# =========================
# AUTONOMOUS MODE
# =========================

elif menu == "Autonomous Mode":

    st.header(
        "Autonomous Drone Mode"
    )

    st.info(
        "Mission Manager Ready"
    )

    if st.button(
        "Start Autonomous Mission"
    ):

        st.success(
            "Autonomous Mission Started"
        )

        st.write(
            "Target Detection Enabled"
        )

        st.write(
            "Obstacle Avoidance Enabled"
        )

        st.write(
            "AI Decision Engine Enabled"
        )