# 🚀 Quick Start Guide - AI Drone System

## Local Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser.

---

## Cloud Deployment (Streamlit Cloud)

### Option A: Manual Deployment
1. Push code to GitHub:
   ```bash
   git add -A
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. Visit https://share.streamlit.io
3. Click "New app"
4. Select your repo, branch, and `app.py` file
5. Done! App will be live in ~2 minutes

### Option B: Automated Deployment
**Windows:**
```bash
deploy.bat
```

**Mac/Linux:**
```bash
bash deploy.sh
```

---

## Feature Availability

### ✅ Works Everywhere
- 🎨 Professional UI with light/dark theme
- 🎤 Voice command interface
- 🔐 Voice authentication UI
- 🤖 Autonomous mission controls

### ⚠️ Local Only (Camera Required)
- 📹 Live vision with camera feed
- Real-time object detection
- Direct microphone input

### 💡 Demo Mode (Cloud Available)
- Simulated AI detection showcase
- Perfect for demonstrations
- No camera/microphone needed

---

## Using Demo Mode (Best for Cloud)

1. Deploy to Streamlit Cloud
2. Open the app
3. Go to "📹 Live Vision"
4. Click "🎬 Demo Mode"
5. Watch simulated AI detections in action

---

## System Requirements

### Minimum (Local)
- Python 3.8+
- 4GB RAM
- 2GB disk space

### Recommended (Local with Camera)
- Python 3.9+
- 8GB RAM
- GPU (NVIDIA with CUDA) for faster detection
- USB camera or built-in webcam

### Streamlit Cloud
- No installation needed
- Access from any browser
- Free tier available

---

## Troubleshooting

### "Camera not available"
→ This is normal on cloud. Try Demo Mode instead.

### OpenCV errors locally
→ Install: `pip install opencv-python`

### Slow performance
→ Run locally for better speed, or use Demo Mode on cloud.

### Issues deploying to cloud?
1. Ensure all code is pushed to GitHub
2. Check `.streamlit/config.toml` is present
3. Verify `requirements.txt` has all dependencies
4. Try redeploying app on Streamlit Cloud dashboard

---

## File Structure
```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── DEPLOYMENT_GUIDE.md    # Detailed deployment docs
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # Secrets (gitignored)
├── core/                  # AI modules
│   ├── voice_auth.py
│   ├── command_classifier.py
│   ├── vision_engine.py
│   └── ...
└── data/                  # Data storage
    ├── known_faces/
    └── registered_voices/
```

---

## Next Steps

1. **Try Locally First**
   ```bash
   streamlit run app.py
   ```

2. **Test All Features**
   - Try camera mode if available
   - Test demo mode
   - Explore voice controls

3. **Deploy to Cloud**
   ```bash
   ./deploy.bat  # Windows
   bash deploy.sh  # Mac/Linux
   ```

4. **Share Your Link**
   - Share Streamlit cloud URL with others
   - Works on desktop and mobile

---

**Questions?** Check `DEPLOYMENT_GUIDE.md` for detailed information.
