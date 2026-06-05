import streamlit as st

from core.voice_auth import VoiceAuthenticator
from core.command_classifier import CommandClassifier
from core.drone_command_executor import DroneCommandExecutor


st.set_page_config(
    page_title="AI Drone Command Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_theme_values(mode: str):
    if mode == "Light":
        return {
            "bg": "#f8fafc",
            "bg_alt": "#ffffff",
            "sidebar_bg": "#f1f5f9",
            "text": "#0f172a",
            "text_secondary": "#475569",
            "card_border": "#e2e8f0",
            "button_bg": "#3b82f6",
            "button_text": "#ffffff",
            "button_hover": "#2563eb",
            "accent": "#3b82f6",
            "accent_light": "#e0e7ff",
            "success": "#10b981",
            "warning": "#f59e0b",
            "info": "#06b6d4",
            "info_bg": "#ecf0ff",
            "info_border": "#bfdbfe"
        }

    return {
        "bg": "#0a0e27",
        "bg_alt": "#131a2b",
        "sidebar_bg": "#0f1425",
        "text": "#e2e8f0",
        "text_secondary": "#94a3b8",
        "card_border": "#1e293b",
        "button_bg": "#06b6d4",
        "button_text": "#020617",
        "button_hover": "#0891b2",
        "accent": "#06b6d4",
        "accent_light": "#164e63",
        "success": "#10b981",
        "warning": "#f59e0b",
        "info": "#0ea5e9",
        "info_bg": "#0f172a",
        "info_border": "#334155"
    }


def apply_app_style(theme_values: dict):
    st.markdown(
        f"""
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html, body, .stApp {{
                background: linear-gradient(135deg, {theme_values['bg']} 0%, {theme_values['bg_alt']} 100%);
                color: {theme_values['text']};
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                letter-spacing: 0.3px;
            }}
            
            .css-1v3fvcr {{
                max-width: 1440px;
            }}
            
            .stSidebar {{
                background: linear-gradient(180deg, {theme_values['sidebar_bg']} 0%, {theme_values['bg_alt']}22 100%);
                border-right: 1px solid {theme_values['card_border']};
            }}
            
            .stButton>button {{
                background: linear-gradient(135deg, {theme_values['button_bg']} 0%, {theme_values['button_bg']}dd 100%) !important;
                color: {theme_values['button_text']} !important;
                border-radius: 14px !important;
                border: 1px solid {theme_values['button_bg']}44 !important;
                box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2) !important;
                font-weight: 600 !important;
                padding: 12px 28px !important;
                transition: all 0.3s ease !important;
                letter-spacing: 0.4px !important;
            }}
            
            .stButton>button:hover {{
                background: linear-gradient(135deg, {theme_values['button_hover']} 0%, {theme_values['button_hover']}dd 100%) !important;
                box-shadow: 0 16px 40px rgba(59, 130, 246, 0.35) !important;
                transform: translateY(-2px) !important;
            }}
            
            .stAlert {{
                border-radius: 16px !important;
                border-left: 4px solid !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
                padding: 16px 20px !important;
            }}
            
            .stTextInput>div>div>input {{
                border-radius: 14px !important;
                border: 2px solid {theme_values['card_border']} !important;
                padding: 14px 18px !important;
                background-color: {theme_values['bg_alt']} !important;
                color: {theme_values['text']} !important;
                transition: all 0.3s ease !important;
                font-size: 0.95rem !important;
            }}
            
            .stTextInput>div>div>input:focus {{
                border-color: {theme_values['accent']} !important;
                box-shadow: 0 0 0 3px {theme_values['accent']}22 !important;
            }}
            
            .metric-card {{
                background: linear-gradient(135deg, {theme_values['bg_alt']} 0%, {theme_values['bg_alt']}cc 100%);
                border: 1.5px solid {theme_values['card_border']};
                border-radius: 26px;
                padding: 28px;
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
                margin-bottom: 16px;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }}
            
            .metric-card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 28px 70px rgba(6, 182, 212, 0.2);
                border-color: {theme_values['accent']};
            }}
            
            .metric-label {{
                color: {theme_values['text_secondary']};
                font-size: 1rem;
                font-weight: 500;
                margin-bottom: 12px;
                letter-spacing: 0.5px;
                text-transform: uppercase;
            }}
            
            .metric-value {{
                color: {theme_values['accent']};
                font-size: 2.8rem;
                font-weight: 800;
                margin-bottom: 8px;
                letter-spacing: -1px;
            }}
            
            .metric-subtitle {{
                color: {theme_values['text_secondary']};
                font-size: 0.9rem;
                margin-top: 12px;
            }}
            
            .section-card {{
                background: linear-gradient(135deg, {theme_values['bg_alt']} 0%, {theme_values['bg_alt']}bb 100%);
                border: 1.5px solid {theme_values['card_border']};
                border-radius: 26px;
                padding: 32px;
                margin-bottom: 24px;
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }}
            
            .section-card:hover {{
                border-color: {theme_values['accent']}66;
                box-shadow: 0 24px 60px rgba(6, 182, 212, 0.15);
            }}
            
            .section-title {{
                color: {theme_values['text']};
                font-size: 1.6rem;
                font-weight: 800;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
                background: linear-gradient(135deg, {theme_values['text']} 0%, {theme_values['accent']} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .section-description {{
                color: {theme_values['text_secondary']};
                margin-top: 8px;
                margin-bottom: 20px;
                font-size: 1.05rem;
                line-height: 1.6;
            }}
            
            .status-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 16px;
            }}
            
            .status-item {{
                background: {theme_values['bg']}cc;
                border: 1px solid {theme_values['card_border']};
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s ease;
            }}
            
            .status-item:hover {{
                background: {theme_values['bg_alt']}99;
                border-color: {theme_values['accent']};
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                font-weight: 800;
                letter-spacing: -0.5px;
            }}
            
            hr {{
                border-color: {theme_values['card_border']} !important;
                margin: 28px 0 !important;
                opacity: 0.5;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric(title: str, value: str, subtitle: str, icon: str, theme_values: dict):
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 18px;">
                <div style="flex: 1;">
                    <div class="metric-label">{icon} {title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-subtitle">{subtitle}</div>
                </div>
                <div style="font-size: 3.2rem; opacity: 0.15;">{icon}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


theme_mode = st.sidebar.radio(
    "🎨 Theme",
    ["🌙 Dark", "☀️ Light", "🔄 Auto"],
    index=2,
)

if theme_mode == "🔄 Auto":
    theme_values = get_theme_values("Dark")
elif "Light" in theme_mode:
    theme_values = get_theme_values("Light")
else:
    theme_values = get_theme_values("Dark")

apply_app_style(theme_values)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding: 16px 0;">
        <div style="font-size: 2.4rem; margin-bottom: 8px;">🚁</div>
        <div style="font-size: 1.3rem; font-weight: 800; color: {theme_values['accent']}; margin-bottom: 6px;">
            AI DRONE
        </div>
        <div style="font-size: 1.1rem; font-weight: 800; color: {theme_values['text']};margin-bottom: 12px;">
            COMMAND CENTER
        </div>
        <div style="font-size: 0.85rem; color: {theme_values['text_secondary']}; line-height: 1.5;">
            Professional Surveillance & Automation
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "📋 Module",
    [
        "🏠 Home",
        "📹 Live Vision",
        "🔐 Voice Authentication",
        "🎤 Voice Control",
        "🤖 Autonomous Mode",
    ],
)

st.markdown(
    f"""
    <div class="section-card" style="margin-top: 8px; text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 12px;">🚁 🎯 📡</div>
        <div class="section-title" style="margin-bottom: 8px;">AI Drone Surveillance System</div>
        <p class="section-description" style="margin: 0;">Enterprise-grade autonomous surveillance with real-time vision analysis, voice-based command execution, and intelligent threat detection.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# HOME
# =========================

if "Home" in menu:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Mission Overview</div>
            <p class="section-description">Live system health and threat detection metrics with a clean operational dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric("Humans", "0", "Active targets detected", "🧍", theme_values)
    with col2:
        render_metric("Vehicles", "0", "Motion objects detected", "🚗", theme_values)
    with col3:
        render_metric("Animals", "0", "Non-human entities", "🦮", theme_values)

    st.markdown("---")

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">System Status</div>
            <p class="section-description">Drone is ready and listening for commands. Visual intelligence and autonomous readiness are enabled.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    status_col1, status_col2 = st.columns([1, 2])
    with status_col1:
        st.success("System Status: READY")
        st.info("AI Decision: WAITING FOR INPUT")
    with status_col2:
        st.markdown(
            """
            - **Safety mode:** Active
            - **Network:** Connected
            - **Battery:** 98%
            - **Mission state:** Standby
            """
        )


# =========================
# VOICE AUTHENTICATION
# =========================

elif "Authentication" in menu:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Voice Authentication</div>
            <p class="section-description">Verify operator identity using registered voice data before enabling critical controls.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    voice_path = st.text_input("Enter voice file path", value="data/registered_voices/sample.wav")

    if st.button("Authenticate"):
        try:
            auth = VoiceAuthenticator()
            result = auth.authenticate(voice_path)
            if result:
                st.success("ACCESS GRANTED")
                st.info("Authorized operator confirmed.")
            else:
                st.error("ACCESS DENIED")
                st.warning("Please use a registered voice sample.")
        except Exception as ex:
            st.error(str(ex))


# =========================
# VOICE CONTROL
# =========================

elif "Voice Control" in menu:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Voice Command Control</div>
            <p class="section-description">Issue natural language commands to the drone and watch the system interpret them in real time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    command_text = st.text_input("Enter command", value="Survey the perimeter")

    if st.button("Execute Command"):
        classifier = CommandClassifier()
        executor = DroneCommandExecutor()
        command = classifier.classify(command_text)
        st.markdown(f"**Detected Command:** {command}")
        executor.execute(command)
        st.success(f"Executed: {command}")


# =========================
# LIVE VISION
# =========================

elif "Vision" in menu:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Live AI Vision</div>
            <p class="section-description">Activate the camera to monitor live footage with object detection and bounding box analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        camera_mode = st.button("🎥 Start Camera", key="camera_btn")
    with col_mode2:
        demo_mode = st.button("🎬 Demo Mode", key="demo_btn")

    if camera_mode:
        try:
            import cv2
            # Try to open camera
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.warning("⚠️ Camera not available on this system.")
                st.info("💡 Try Demo Mode to see object detection in action with sample footage.")
            else:
                from ultralytics import YOLO
                
                model = YOLO("yolov8n.pt")
                frame_window = st.image([])
                stop_button = st.button("⏹️ Stop Camera")
                
                frame_count = 0
                while cap.isOpened() and not stop_button:
                    success, frame = cap.read()
                    if not success:
                        break
                    
                    frame_count += 1
                    if frame_count % 2 != 0:  # Process every other frame for performance
                        continue
                    
                    results = model(frame, conf=0.5)
                    human_count = 0
                    vehicle_count = 0
                    animal_count = 0
                    vehicle_classes = [2, 3, 5, 7]
                    animal_classes = [15, 16, 17, 18, 19]
                    
                    for result in results:
                        for box in result.boxes:
                            cls = int(box.cls[0])
                            confidence = float(box.conf[0])
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            label = ""
                            color = (0, 255, 0)
                            
                            if cls == 0:
                                human_count += 1
                                label = "Human"
                                color = (0, 255, 0)
                            elif cls in vehicle_classes:
                                vehicle_count += 1
                                label = "Vehicle"
                                color = (255, 0, 0)
                            elif cls in animal_classes:
                                animal_count += 1
                                label = "Animal"
                                color = (0, 0, 255)
                            else:
                                continue
                            
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                            cv2.putText(
                                frame,
                                f"{label} {confidence:.2f}",
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                color,
                                2,
                            )
                    
                    cv2.putText(frame, f"Humans: {human_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                    cv2.putText(frame, f"Animals: {animal_count}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_window.image(frame, channels="RGB")
                
                cap.release()
                st.success("Camera session ended.")
        
        except ImportError as e:
            st.error(f"❌ OpenCV import error: {str(e)}")
            st.info("💡 This is expected on Streamlit Cloud (no GUI). Try Demo Mode instead.")
        except Exception as ex:
            st.error(f"❌ Camera Error: {str(ex)}")
            st.info("💡 Try Demo Mode instead to see AI vision detection.")

    if demo_mode:
        st.info("🎬 **Demo Mode** - Live AI Vision Simulation")
        try:
            from PIL import Image, ImageDraw
            import random
            
            demo_container = st.container()
            frame_window = demo_container.image([])
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Humans Detected", "0", "Real-time count")
            with col2:
                st.metric("Vehicles Detected", "0", "Real-time count")
            with col3:
                st.metric("Animals Detected", "0", "Real-time count")
            
            st.success("✓ Demo mode ready - Simulating 5 detection frames...")
            
            for frame_num in range(5):
                img = Image.new('RGB', (640, 480), color=(20, 25, 50))
                draw = ImageDraw.Draw(img)
                
                # Simulate detections
                detections = [
                    {"label": "Human", "conf": 0.92, "box": (50, 80, 180, 300), "color": (0, 255, 0)},
                    {"label": "Vehicle", "conf": 0.88, "box": (300, 120, 500, 280), "color": (255, 0, 0)},
                    {"label": "Animal", "conf": 0.85, "box": (100, 250, 200, 400), "color": (0, 0, 255)},
                ]
                
                for det in detections:
                    x1, y1, x2, y2 = det["box"]
                    draw.rectangle([x1, y1, x2, y2], outline=det["color"], width=3)
                    label_text = f"{det['label']} {det['conf']:.2f}"
                    draw.text((x1, y1 - 15), label_text, fill=det["color"])
                
                # Draw stats
                draw.text((20, 20), f"Frame {frame_num + 1}/5", fill=(255, 255, 255))
                draw.text((20, 50), "Humans: 1", fill=(0, 255, 0))
                draw.text((20, 80), "Vehicles: 1", fill=(255, 0, 0))
                draw.text((20, 110), "Animals: 1", fill=(0, 0, 255))
                
                frame_window.image(img, channels="RGB", width=640)
                import time
                time.sleep(0.8)
            
            st.success("✓ Demo simulation complete!")
            st.markdown("> **Note:** For real camera feed, run locally on a system with a connected camera.")
        
        except Exception as ex:
            st.error(f"Demo mode error: {str(ex)}")


# =========================
# AUTONOMOUS MODE
# =========================

elif "Autonomous" in menu:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Autonomous Drone Mode</div>
            <p class="section-description">Enable mission automation for target detection, obstacle avoidance, and intelligent navigation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info("Mission Manager Ready")

    if st.button("Start Autonomous Mission"):
        st.success("Autonomous Mission Started")
        st.write("Target Detection Enabled")
        st.write("Obstacle Avoidance Enabled")
        st.write("AI Decision Engine Enabled")
