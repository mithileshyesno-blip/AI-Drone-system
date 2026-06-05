@echo off
REM Quick deployment script for Streamlit Cloud (Windows)

echo.
echo 🚀 AI Drone System - Streamlit Cloud Deployment
echo ================================================
echo.

REM Check if git is initialized
if not exist .git (
    echo ❌ Git repository not found
    echo Run: git init ^&^& git remote add origin ^<your-repo-url^>
    exit /b 1
)

REM Add all changes
echo 📝 Preparing files for deployment...
git add -A

REM Commit changes
echo 📝 Committing changes...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
git commit -m "AI Drone System update - %mydate%"

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push origin main

echo.
echo ✅ Deployment ready!
echo.
echo 📋 Next steps:
echo 1. Go to https://share.streamlit.io
echo 2. Click 'New app'
echo 3. Connect your GitHub repository
echo 4. Select this app.py file
echo.
echo 🌐 Your app will be available at:
echo    https://share.streamlit.io/[username]/[repo]/app.py
echo.
pause
