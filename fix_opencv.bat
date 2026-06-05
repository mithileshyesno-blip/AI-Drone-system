@echo off
REM Fix OpenCV installation for AI Drone System (Windows)

echo.
echo 🔧 Fixing OpenCV installation...
echo This script will install the correct version of OpenCV
echo.

REM Uninstall conflicting versions
echo 📦 Removing conflicting packages...
pip uninstall opencv-python -y
pip uninstall opencv-contrib-python -y

REM Install the correct version
echo 📦 Installing opencv-python-headless...
pip install opencv-python-headless --upgrade --force-reinstall

REM Install requirements
echo 📦 Installing all dependencies...
pip install -r requirements.txt --upgrade

echo.
echo ✅ OpenCV installation fixed!
echo.
echo To run the app:
echo   streamlit run app.py
echo.
pause
