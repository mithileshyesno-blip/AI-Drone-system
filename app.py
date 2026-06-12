import os
import sys

# Fix for opencv-python-headless on systems without display
# This must be done before importing cv2
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_V4L_RANGE_PARSER_USE_OPEN_RANGE'] = '1'
os.environ['OPENCV_LOG_LEVEL'] = 'OFF'

try:
    # Suppress cv2 and numpy GUI-related warnings
    import numpy as np
    import cv2
    cv2.setNumThreads(2)
except Exception as e:
    print(f"Note: OpenCV/NumPy may have limited functionality: {e}")

import streamlit as st

from core.voice_auth import VoiceAuthenticator
from core.command_classifier import CommandClassifier
from core.drone_command_executor import DroneCommandExecutor
from core.dashboard_data import DashboardData


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

            .dashboard-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }}

            .tile-card {{
                background: linear-gradient(135deg, {theme_values['bg_alt']} 0%, {theme_values['bg_alt']}dd 100%);
                border: 1.5px solid {theme_values['card_border']};
                border-radius: 24px;
                padding: 24px;
                min-height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }}

            .tile-card:hover {{
                transform: translateY(-6px);
                border-color: {theme_values['accent']};
            }}

            .tile-icon {{
                font-size: 3.2rem;
                margin-bottom: 16px;
                opacity: 0.95;
            }}

            .status-pill {{
                background: {theme_values['accent']}22;
                color: {theme_values['accent']};
                border: 1px solid {theme_values['accent']}44;
                border-radius: 999px;
                padding: 10px 18px;
                font-size: 0.95rem;
                font-weight: 700;
                white-space: nowrap;
            }}

            .info-note {{
                background: {theme_values['accent_light']};
                border: 1px solid {theme_values['info_border']};
                border-radius: 18px;
                padding: 18px 22px;
                margin-top: 14px;
                color: {theme_values['text_secondary']};
            }}

            .hero-panel {{
                background: radial-gradient(circle at top left, {theme_values['accent']}22, transparent 40%),
                            linear-gradient(135deg, {theme_values['bg_alt']} 0%, {theme_values['bg']} 100%);
                border: 1px solid {theme_values['card_border']};
                border-radius: 32px;
                padding: 34px;
                margin-bottom: 24px;
                box-shadow: 0 32px 80px rgba(6, 182, 212, 0.15);
                backdrop-filter: blur(18px);
            }}

            .hero-heading {{
                font-size: 2.35rem;
                font-weight: 900;
                margin-bottom: 12px;
                line-height: 1.05;
            }}

            .hero-subtitle {{
                color: {theme_values['text_secondary']};
                font-size: 1.05rem;
                max-width: 740px;
                margin-bottom: 20px;
            }}

            .stat-chip {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 18px;
                border-radius: 999px;
                background: {theme_values['accent']}11;
                color: {theme_values['accent']};
                font-weight: 700;
                font-size: 0.95rem;
            }}

            .glow-card {{
                background: linear-gradient(180deg, {theme_values['bg_alt']}dd 0%, {theme_values['bg_alt']}cc 100%);
                border: 1.5px solid {theme_values['card_border']};
                border-radius: 28px;
                padding: 24px;
                box-shadow: 0 28px 60px rgba(6, 182, 212, 0.12);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }}

            .glow-card:hover {{
                transform: translateY(-4px);
                border-color: {theme_values['accent']};
            }}

            .hero-top {{
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 18px;
                flex-wrap: wrap;
            }}

            .hero-badge {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 18px;
                color: {theme_values['accent']};
                background: {theme_values['accent']}11;
                border: 1px solid {theme_values['accent']}44;
                border-radius: 999px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}

            .radar-panel {{
                width: 180px;
                height: 180px;
                border-radius: 999px;
                position: relative;
                background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 55%);
                border: 1px solid {theme_values['accent']}22;
                box-shadow: 0 0 40px rgba(6, 182, 212, 0.08);
                margin: 0 auto;
            }}

            .radar-sweep {{
                position: absolute;
                inset: 0;
                border-radius: 999px;
                background: conic-gradient(from 0deg, rgba(6, 182, 212, 0.16) 0%, rgba(6, 182, 212, 0.02) 45%, transparent 60%);
                animation: sweep 3.5s linear infinite;
            }}

            .radar-center {{
                position: absolute;
                top: 50%;
                left: 50%;
                width: 18px;
                height: 18px;
                border-radius: 50%;
                background: {theme_values['accent']};
                transform: translate(-50%, -50%);
                box-shadow: 0 0 24px rgba(6, 182, 212, 0.35);
            }}

            @keyframes sweep {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}

            .sparkline {{
                width: 100%;
                height: 92px;
                border-radius: 18px;
                background: linear-gradient(90deg, {theme_values['accent']}33, transparent 80%);
                margin-top: 18px;
            }}

            .section-hero {{
                padding: 32px;
                border-radius: 28px;
                background: linear-gradient(135deg, {theme_values['accent']}22 0%, {theme_values['bg_alt']} 100%);
                border: 1.5px solid {theme_values['card_border']};
                margin-bottom: 24px;
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


def render_info_tile(icon: str, title: str, value: str, detail: str, theme_values: dict):
    st.markdown(
        f"""
        <div class="tile-card">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 18px;">
                <div>
                    <div class="tile-icon">{icon}</div>
                    <div class="metric-label">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                <div class="status-pill">{detail}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


dashboard = DashboardData()

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
    dashboard.update_humans(2)
    dashboard.update_vehicles(1)
    dashboard.update_animals(0)
    dashboard.update_status("MISSION READY")
    dashboard.update_decision("PASSIVE SCAN")
    dashboard.unlock_target()

    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-top">
                <div style="max-width: 700px;">
                    <div class="hero-heading">AI Drone Command Bridge</div>
                    <div class="hero-subtitle">A sleek operational console for intelligent aerial surveillance, autonomous mission control, and secure voice-driven command execution.</div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin-top: 18px;">
                        <div class="stat-chip">🚀 Mission Ready</div>
                        <div class="stat-chip">🔐 Secure Access</div>
                        <div class="stat-chip">🌐 Live Vision</div>
                    </div>
                </div>
                <div class="hero-badge">PRIMARY AERIAL UNIT</div>
            </div>
            <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 18px; margin-top: 24px; align-items: stretch;">
                <div style="display: grid; gap: 16px;">
                    <div class="glow-card">
                        <div class="metric-label">Coverage</div>
                        <div class="metric-value">96%</div>
                        <div class="info-note">Real-time area scan capacity with precision tracking.</div>
                    </div>
                    <div class="glow-card">
                        <div class="metric-label">Response Time</div>
                        <div class="metric-value">140 ms</div>
                        <div class="info-note">Low-latency AI inference across live feeds.</div>
                    </div>
                </div>
                <div style="display: grid; gap: 16px;">
                    <div class="radar-panel">
                        <div class="radar-sweep"></div>
                        <div class="radar-center"></div>
                    </div>
                    <div class="glow-card" style="text-align: center;">
                        <div class="metric-label">Threat Level</div>
                        <div class="metric-value">LOW</div>
                        <div class="info-note">All sensors nominal. No immediate threats detected in the current survey area.</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="dashboard-grid">
            <div class="tile-card">
                <div class="tile-icon">🛰️</div>
                <div class="metric-label">Airspace Status</div>
                <div class="metric-value">Online</div>
                <div class="info-note">Navigation channels stable and encrypted for secure flight control.</div>
            </div>
            <div class="tile-card">
                <div class="tile-icon">⚡</div>
                <div class="metric-label">Battery Health</div>
                <div class="metric-value">98%</div>
                <div class="info-note">Mission reserve available for up to 42 minutes of sustained operation.</div>
            </div>
            <div class="tile-card">
                <div class="tile-icon">🎯</div>
                <div class="metric-label">Target Lock</div>
                <div class="metric-value">{ 'LOCKED' if dashboard.target_locked else 'STANDBY' }</div>
                <div class="info-note">Target acquisition systems are ready for intelligent tracking.</div>
            </div>
            <div class="tile-card">
                <div class="tile-icon">🧠</div>
                <div class="metric-label">AI Mode</div>
                <div class="metric-value">Predictive</div>
                <div class="info-note">Adaptive planning with anomaly detection and decision support.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    status_col1, status_col2 = st.columns([2, 1])
    with status_col1:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">Mission Telemetry</div>
                <p class="section-description">Live operational data and recent performance analytics from the drone ecosystem.</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-top: 18px;">
                    <div class="metric-card" style="padding: 20px;">
                        <div class="metric-label">Humans Detected</div>
                        <div class="metric-value">{dashboard.human_count}</div>
                        <div class="metric-subtitle">Current active human targets</div>
                    </div>
                    <div class="metric-card" style="padding: 20px;">
                        <div class="metric-label">Vehicles Detected</div>
                        <div class="metric-value">{dashboard.vehicle_count}</div>
                        <div class="metric-subtitle">Potential moving objects in range</div>
                    </div>
                    <div class="metric-card" style="padding: 20px;">
                        <div class="metric-label">Animals Detected</div>
                        <div class="metric-value">{dashboard.animal_count}</div>
                        <div class="metric-subtitle">Wildlife / non-human entities</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Recent Activity and Alerts", expanded=True):
            st.write("- 04:12 UTC — Autonomous sweep completed with zero anomalies.")
            st.write("- 04:03 UTC — New voice access request validated.")
            st.write("- 03:57 UTC — Live vision stream ready for deployment.")

    with status_col2:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">Operational Snapshot</div>
                <p class="section-description">Quick overview of system health, AI decision state, and mission readiness.</p>
                <div class="status-container">
                    <div class="status-item">
                        <strong>Status</strong><br>{dashboard.drone_status}
                    </div>
                    <div class="status-item">
                        <strong>Decision</strong><br>{dashboard.ai_decision}
                    </div>
                    <div class="status-item">
                        <strong>Lock State</strong><br>{'Locked' if dashboard.target_locked else 'Unlocked'}
                    </div>
                </div>
                <div class="info-note">Use the Live Vision tab to see detection results and the Voice Control tab to send commands safely.</div>
            </div>
            """,
            unsafe_allow_html=True,
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

    st.markdown("**Step 1: Upload the registered voice sample**")
    registered_voice = st.file_uploader("Upload authorized voice sample (.wav)", type=["wav"], key="registered_voice")

    st.markdown("**Step 2: Upload the voice sample to authenticate**")
    uploaded_voice = st.file_uploader("Upload test voice sample (.wav)", type=["wav"], key="test_voice")

    st.markdown("**Optional: Use existing registered voice folder**")
    registered_dir_input = st.text_input(
        "Registered voice samples folder",
        value="data/registered_voices",
        help="Folder containing authorized voice samples inside the repo."
    )

    if st.button("Authenticate"):
        try:
            if uploaded_voice is None:
                st.error("Please upload a test voice sample to authenticate.")
            else:
                import tempfile

                registered_dir = None
                temp_dir = None
                if registered_voice is not None:
                    temp_dir = tempfile.TemporaryDirectory()
                    registered_path = os.path.join(temp_dir.name, "registered.wav")
                    with open(registered_path, "wb") as registered_file:
                        registered_file.write(registered_voice.read())
                    registered_dir = temp_dir.name
                else:
                    registered_dir = os.path.normpath(registered_dir_input.strip())
                    if not os.path.isabs(registered_dir):
                        registered_dir = os.path.abspath(registered_dir)

                if registered_dir is None:
                    st.error("No authorized voice sample or folder specified.")
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(uploaded_voice.read())
                        input_voice_file = tmp.name

                    auth = VoiceAuthenticator(registered_path=registered_dir)

                    if not auth.voice_database:
                        st.warning(
                            f"No registered voice samples were found in '{auth.registered_path}'. "
                            "Upload an authorized voice sample or add files like 'auth_1.wav' into that folder."
                        )
                    else:
                        result = auth.authenticate(input_voice_file)
                        if result:
                            st.success("ACCESS GRANTED")
                            st.info("Authorized operator confirmed.")
                        else:
                            st.error("ACCESS DENIED")
                            st.warning("The uploaded voice sample did not match any registered voice.")

                    os.unlink(input_voice_file)
                if temp_dir is not None:
                    temp_dir.cleanup()
        except FileNotFoundError as ex:
            st.error(str(ex))
        except Exception as ex:
            st.error(f"Voice Authentication Error: {str(ex)}")


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
            <p class="section-description">Connect to cameras, upload videos, or stream live feeds with real-time AI object detection.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detect environment - Streamlit Cloud vs Local
    is_cloud = "STREAMLIT_SERVER_HEADLESS" in os.environ or "STREAMLIT_SERVER_RUNONSAVE" not in os.environ
    
    # Vision input options
    st.markdown("---")
    st.markdown("**📹 Select Vision Input Source:**")
    
    vision_mode = st.radio(
        "Choose input source:",
        [
            "🎥 IP Camera (RTSP)",
            "📤 Upload Video",
            "🌐 Stream URL",
            "📹 Live Camera",
            "🎬 Demo Mode",
        ],
        horizontal=True,
    )
    
    @st.cache_resource
    def load_yolo_model():
        from ultralytics import YOLO
        return YOLO("yolov8n.pt")
    
    yolo_model = None
    try:
        yolo_model = load_yolo_model()
    except Exception as e:
        st.warning(f"YOLO model could not be loaded right now: {e}")
        st.info("If you want only Demo Mode, skip the live/video tabs.")
    
    def process_video_frame(frame, frame_num, model):
        """Process frame with YOLO detection"""
        if model is None:
            return frame, 0, 0, 0
        try:
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
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            cv2.putText(frame, f"Humans: {human_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
            cv2.putText(frame, f"Animals: {animal_count}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame, human_count, vehicle_count, animal_count
        except Exception as e:
            st.error(f"Detection error: {str(e)}")
            return frame, 0, 0, 0
    
    if vision_mode == "🎥 IP Camera (RTSP)":
        st.markdown("### 🎥 Connect to IP Camera")
        st.markdown("Provide RTSP/HTTP streaming URL from your security camera:")
        
        rtsp_url = st.text_input(
            "Camera Stream URL",
            placeholder="rtsp://username:password@192.168.1.100:554/stream",
            help="Enter RTSP or HTTP URL from your IP camera"
        )
        
        if rtsp_url:
            try:
                st.info("🔗 Connecting to camera stream...")
                cap = cv2.VideoCapture(rtsp_url)
                
                if not cap.isOpened():
                    st.error("❌ Failed to connect to stream. Check URL and network access.")
                else:
                    frame_window = st.empty()
                    stop_button = st.button("⏹️ Stop Stream", key="stop_rtsp")
                    
                    col1, col2, col3 = st.columns(3)
                    metric1 = col1.empty()
                    metric2 = col2.empty()
                    metric3 = col3.empty()
                    
                    frame_count = 0
                    while cap.isOpened() and not stop_button:
                        success, frame = cap.read()
                        if not success:
                            st.warning("Stream ended or connection lost.")
                            break
                        
                        frame_count += 1
                        if frame_count % 2 == 0:  # Process every other frame
                            frame, h_count, v_count, a_count = process_video_frame(frame, frame_count, yolo_model)
                            
                            frame_window.image(frame, channels="RGB")
                            metric1.metric("Humans", h_count)
                            metric2.metric("Vehicles", v_count)
                            metric3.metric("Animals", a_count)
                    
                    cap.release()
                    st.success("✅ Stream stopped.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif vision_mode == "📤 Upload Video":
        st.markdown("### 📤 Upload Video File")
        st.markdown("Upload MP4, AVI, MOV, or other video formats for analysis:")
        
        video_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'])
        
        if video_file:
            try:
                # Save uploaded file temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                    tmp.write(video_file.read())
                    temp_path = tmp.name
                
                st.info("📹 Processing uploaded video...")
                cap = cv2.VideoCapture(temp_path)
                
                if not cap.isOpened():
                    st.error("❌ Failed to read video file.")
                else:
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    frame_window = st.empty()
                    progress_bar = st.progress(0)
                    
                    col1, col2, col3 = st.columns(3)
                    metric1 = col1.empty()
                    metric2 = col2.empty()
                    metric3 = col3.empty()
                    
                    frame_count = 0
                    while cap.isOpened():
                        success, frame = cap.read()
                        if not success:
                            break
                        
                        frame_count += 1
                        if frame_count % 2 == 0:  # Process every other frame
                            frame, h_count, v_count, a_count = process_video_frame(frame, frame_count, yolo_model)
                            
                            frame_window.image(frame, channels="RGB")
                            metric1.metric("Humans", h_count)
                            metric2.metric("Vehicles", v_count)
                            metric3.metric("Animals", a_count)
                            
                            progress = min(frame_count / total_frames, 1.0)
                            progress_bar.progress(progress)
                    
                    cap.release()
                    st.success(f"✅ Video analysis complete! Processed {frame_count} frames.")
                    
                    # Clean up
                    import os
                    os.unlink(temp_path)
            except Exception as e:
                st.error(f"❌ Error processing video: {str(e)}")
    
    elif vision_mode == "🌐 Stream URL":
        st.markdown("### 🌐 Stream from URL")
        st.markdown("Enter HTTP/HTTPS URL to any public video stream:")
        
        stream_url = st.text_input(
            "Stream URL",
            placeholder="https://example.com/stream.m3u8 or https://example.com/stream.mp4",
            help="HTTP, HTTPS, HLS (.m3u8), or MP4 URLs"
        )
        
        if stream_url:
            try:
                st.info("🔗 Connecting to stream...")
                cap = cv2.VideoCapture(stream_url)
                
                if not cap.isOpened():
                    st.error("❌ Failed to connect to stream. Check URL and format.")
                else:
                    frame_window = st.empty()
                    stop_button = st.button("⏹️ Stop Stream", key="stop_url")
                    
                    col1, col2, col3 = st.columns(3)
                    metric1 = col1.empty()
                    metric2 = col2.empty()
                    metric3 = col3.empty()
                    
                    frame_count = 0
                    while cap.isOpened() and not stop_button:
                        success, frame = cap.read()
                        if not success:
                            st.warning("Stream ended or connection lost.")
                            break
                        
                        frame_count += 1
                        if frame_count % 2 == 0:  # Process every other frame
                            frame, h_count, v_count, a_count = process_video_frame(frame, frame_count, yolo_model)
                            
                            frame_window.image(frame, channels="RGB")
                            metric1.metric("Humans", h_count)
                            metric2.metric("Vehicles", v_count)
                            metric3.metric("Animals", a_count)
                    
                    cap.release()
                    st.success("✅ Stream stopped.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif vision_mode == "📹 Live Camera":
        st.markdown("### 📹 Live Camera")
        
        if is_cloud:
            st.markdown("Use your browser camera for live capture from Streamlit Cloud:")
            camera_input = st.camera_input("Capture image from webcam")

            if camera_input is not None:
                try:
                    file_bytes = np.asarray(bytearray(camera_input.getvalue()), dtype=np.uint8)
                    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                    if frame is None:
                        st.error("❌ Unable to decode the captured image.")
                    else:
                        frame, h_count, v_count, a_count = process_video_frame(frame, 0, yolo_model)
                        st.image(frame, channels="RGB", caption=f"Humans: {h_count}  Vehicles: {v_count}  Animals: {a_count}")
                        st.success("✅ Frame processed from browser camera.")
                except Exception as e:
                    st.error(f"❌ Camera processing error: {str(e)}")
        else:
            if st.button("🎥 Start Local Camera"):
                try:
                    cap = cv2.VideoCapture(0)
                    
                    if not cap.isOpened():
                        st.error("❌ No camera detected on this system.")
                    else:
                        frame_window = st.empty()
                        stop_button = st.button("⏹️ Stop Camera")
                        
                        col1, col2, col3 = st.columns(3)
                        metric1 = col1.empty()
                        metric2 = col2.empty()
                        metric3 = col3.empty()
                        
                        frame_count = 0
                        while cap.isOpened() and not stop_button:
                            success, frame = cap.read()
                            if not success:
                                break
                            
                            frame_count += 1
                            if frame_count % 2 == 0:  # Process every other frame
                                frame, h_count, v_count, a_count = process_video_frame(frame, frame_count, yolo_model)
                                
                                frame_window.image(frame, channels="RGB")
                                metric1.metric("Humans", h_count)
                                metric2.metric("Vehicles", v_count)
                                metric3.metric("Animals", a_count)
                        
                        cap.release()
                        st.success("✅ Camera session ended.")
                except Exception as e:
                    st.error(f"❌ Camera Error: {str(e)}")
    
    elif vision_mode == "🎬 Demo Mode":
        st.markdown("### 🎬 Demo Mode")
        st.markdown("See simulated AI detection with sample objects:")
        
        if st.button("▶️ Start Demo"):
            try:
                from PIL import Image, ImageDraw
                import time
                
                frame_window = st.empty()
                progress_bar = st.progress(0)
                
                col1, col2, col3 = st.columns(3)
                metric1 = col1.empty()
                metric2 = col2.empty()
                metric3 = col3.empty()
                
                st.info("🎬 Simulating AI detection with 5 frames...")
                
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
                    
                    draw.text((20, 20), f"Frame {frame_num + 1}/5 - Demo", fill=(255, 255, 255))
                    draw.text((20, 50), "Humans: 1", fill=(0, 255, 0))
                    draw.text((20, 80), "Vehicles: 1", fill=(255, 0, 0))
                    draw.text((20, 110), "Animals: 1", fill=(0, 0, 255))
                    
                    frame_window.image(img, channels="RGB", width=640)
                    metric1.metric("Humans", "1")
                    metric2.metric("Vehicles", "1")
                    metric3.metric("Animals", "1")
                    
                    progress_bar.progress((frame_num + 1) / 5)
                    time.sleep(0.8)
                
                st.success("✅ Demo complete!")
                st.markdown("""
                ### What You Saw:
                - 🎯 **Bounding Boxes:** Object detection rectangles with confidence scores
                - 📊 **Confidence Scores:** AI model accuracy (0.0-1.0 scale)
                - 🏷️ **Classifications:** Human, Vehicle, Animal detection
                
                ### Ready for Real Feeds?
                Try the other tabs to connect to:
                - 🎥 IP cameras (RTSP streaming)
                - 📤 Your own video files
                - 🌐 Any public video stream
                """)
            except Exception as e:
                st.error(f"Demo error: {str(e)}")


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
