# Streamlit Deployment Guide

## Deploying to Streamlit Cloud

### Prerequisites
- GitHub account (code must be in a public GitHub repo)
- Streamlit Cloud account (free at https://streamlit.io)

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "AI Drone System - Ready for deployment"
   git push origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository and branch
   - Set main file path to `app.py`

3. **Configuration**
   - Advanced settings → Secrets
   - Add any environment variables if needed

### Features by Environment

#### Local Deployment (Recommended for Full Features)
- ✅ Live camera feed with real-time object detection
- ✅ Real-time video processing
- ✅ Full voice authentication
- ✅ Voice command control

**To run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

#### Streamlit Cloud Deployment
- ❌ No camera access (headless environment)
- ✅ Demo Mode available for vision showcase
- ✅ Voice authentication interface
- ✅ Command control UI
- ✅ Professional dark/light theme

**Limitations on Streamlit Cloud:**
- No real-time camera input
- Use **Demo Mode** to showcase AI vision capabilities
- Voice modules need local microphone (not available on cloud)

### Demo Mode Features
When deployed on Streamlit Cloud, users can:
1. Click **"🎬 Demo Mode"** in Live Vision section
2. See simulated AI detections
3. Understand object detection capabilities
4. Try other modules (Voice Auth, Commands, Autonomous Mode)

### Environment Variables (if needed)
Create `.streamlit/secrets.toml`:
```toml
# Add any required API keys or secrets here
```

### Troubleshooting

**"Camera not available" error:**
- This is normal on Streamlit Cloud
- Use Demo Mode instead

**OpenCV import errors:**
- Using `opencv-python-headless` for cloud compatibility
- Install locally: `pip install opencv-python`

**Performance issues:**
- Reduce video processing frame rate
- Use smaller YOLO model (yolov8n is already minimal)
- Limit streaming to local network

### Local vs Cloud Comparison

| Feature | Local | Cloud |
|---------|-------|-------|
| Live Camera | ✅ | ❌ |
| Demo Mode | ✅ | ✅ |
| Voice Auth | ✅ | ⚠️ |
| Command Control | ✅ | ✅ |
| AI Detection | ✅ | ✅ |
| Speed | Fast | Medium |

### Next Steps
1. Deploy to Streamlit Cloud for showcase
2. Test all features locally first
3. Share cloud link with stakeholders
4. Use local deployment for production with cameras

---
**Deployment URL Pattern:** `https://share.streamlit.io/[username]/[repo]/app.py`
