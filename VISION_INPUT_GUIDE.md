# 📹 Multi-Source Vision Input Guide

## Overview
The AI Drone system now supports **5 different video input methods** on both cloud and local deployments!

---

## 🎯 Quick Start

### Option 1: 🎥 IP Camera (RTSP)
Perfect for security cameras with network streaming.

**Steps:**
1. Go to "📹 Live Vision" → "🎥 IP Camera (RTSP)" tab
2. Enter your camera's RTSP URL
3. Click start - real-time AI detection begins!

**Common RTSP URLs:**
```
rtsp://username:password@192.168.1.100:554/stream
rtsp://admin:admin@camera-ip:554/stream1
rtsp://192.168.1.50:554/stream
```

**Supported cameras:**
- Hikvision
- Dahua
- Axis
- Ubiquiti
- Any RTSP-capable camera

---

### Option 2: 📤 Upload Video
Analyze your own video files.

**Steps:**
1. Go to "📹 Live Vision" → "📤 Upload Video" tab
2. Click "Choose a video file"
3. Select MP4, AVI, MOV, MKV, etc.
4. AI processes the entire video with detection

**Supported formats:**
- MP4
- AVI
- MOV
- MKV
- FLV
- WMV

**Best for:**
- Security footage analysis
- Surveillance recordings
- Traffic monitoring
- Custom video analysis

---

### Option 3: 🌐 Stream URL
Connect to any public video stream.

**Steps:**
1. Go to "📹 Live Vision" → "🌐 Stream URL" tab
2. Enter HTTP, HTTPS, or HLS stream URL
3. Real-time detection on the stream

**Supported URLs:**
```
https://example.com/stream.mp4
https://example.com/stream.m3u8
https://example.com/live/video.mp4
```

**Common sources:**
- Security camera HTTP streams
- YouTube/Twitch streams (if accessible)
- RTSP to HTTP bridges
- Public traffic cameras

---

### Option 4: 📹 Live Camera
Use your system's connected USB camera (local only).

**Steps:**
1. Go to "📹 Live Vision" → "📹 Live Camera" tab
2. Click "🎥 Start Local Camera"
3. Real-time detection from your webcam

**Note:** Only works locally with connected camera. ⚠️ Cloud deployment will show disabled message.

---

### Option 5: 🎬 Demo Mode
See simulated AI detection (works everywhere).

**Steps:**
1. Go to "📹 Live Vision" → "🎬 Demo Mode" tab
2. Click "▶️ Start Demo"
3. Watch 5 frames of simulated detection

**Good for:**
- Testing the app
- Demonstrating capabilities
- Learning how detection works
- No internet required

---

## 🔑 Key Features

### Real-Time Detection
All inputs show live metrics:
- 👥 **Humans Detected** - Count of people
- 🚗 **Vehicles Detected** - Cars, trucks, buses
- 🦁 **Animals Detected** - Pets, wildlife

### Object Detection
Each detection includes:
- 📍 **Bounding Box** - Rectangle around object
- 📊 **Confidence** - AI certainty (0.0-1.0)
- 🏷️ **Label** - Object type classification

### Performance
- Processes every other frame for speed
- Works smoothly on cloud and locally
- Handles various resolutions

---

## 📋 Setup Examples

### Example 1: Home Security Camera (Hikvision)
```
IP: 192.168.1.100
Port: 554
Username: admin
Password: admin123

RTSP URL: rtsp://admin:admin123@192.168.1.100:554/stream
```

### Example 2: Workplace Security System (Dahua)
```
IP: 10.0.0.50
Stream: Main stream

RTSP URL: rtsp://root:admin@10.0.0.50:554/stream1
```

### Example 3: Public Traffic Camera
```
HTTP URL: https://traffic.example.com/camera1.mp4
```

---

## ⚙️ Configuration

### Network Requirements
- **For RTSP:** Camera must be on same network or port-forwarded
- **For HTTP/HTTPS:** Public internet connection
- **For Upload:** Local file system or cloud storage

### Bandwidth
- RTSP: 1-5 Mbps recommended
- HTTP Stream: 2-10 Mbps depending on quality
- Upload: File-dependent

### Security
- 🔒 Credentials in RTSP URLs are private (not logged)
- 🔐 Use strong passwords for network cameras
- 📡 RTSP works better on private networks

---

## 🐛 Troubleshooting

### "Failed to connect to stream"
**Causes:**
- Wrong URL or credentials
- Camera offline
- Network not accessible
- Port blocked by firewall

**Solutions:**
1. Verify URL is correct
2. Test URL in VLC media player first
3. Check camera is powered on
4. Verify network connectivity
5. Check firewall/port forwarding

### "Stream ended or connection lost"
**Causes:**
- Network interrupted
- Camera crashed
- Connection timeout

**Solutions:**
1. Check network stability
2. Restart camera
3. Try shorter stream URL
4. Reduce processing frame rate

### Video Upload too slow
**Solutions:**
- Compress video first (reduce resolution)
- Use shorter video clips
- Try local deployment for better performance

---

## 🌐 Cloud Deployment (Streamlit Cloud)

### What Works on Cloud
✅ **IP Camera (RTSP)** - Stream from network cameras  
✅ **Stream URL** - Any HTTP/HTTPS stream  
✅ **Upload Video** - Your own video files  
✅ **Demo Mode** - Always available  

### What Doesn't Work on Cloud
⚠️ **Live Camera** - No USB camera on cloud servers  

### For Best Results on Cloud
1. Use IP cameras or public streams
2. Keep RTSP URLs accessible from internet
3. Upload smaller video files (< 100MB)
4. Use Demo Mode for quick testing

---

## 🚀 Advanced Usage

### Batch Processing
Upload multiple video files:
```
1. Upload first video → See results
2. Upload second video → See results
3. Compare detection patterns
```

### 24/7 Monitoring
Connect to IP camera RTSP stream:
```
- Leave tab open for continuous monitoring
- Real-time detection
- Runs in browser
```

### Archive Analysis
Upload security footage:
```
1. Export video from recorder
2. Upload to cloud deployment
3. Get AI analysis of archived events
```

---

## 📊 Detection Classes

The AI detects 3 main categories:

### 👥 Humans (Class 0)
- People detection
- Person counting
- Crowd analysis

### 🚗 Vehicles (Classes 2, 3, 5, 7)
- Cars
- Trucks
- Buses
- Motorcycles

### 🦁 Animals (Classes 15-19)
- Dogs, cats
- Birds
- Wildlife
- Livestock

---

## 🔗 Integration Ideas

### IP Camera Integration
```
1. Set up RTSP camera in your home/office
2. Open app in browser
3. Enter camera URL
4. Get real-time AI surveillance
```

### Video Analysis Pipeline
```
1. Record security footage
2. Upload to cloud app
3. Get AI detection report
4. Export or archive results
```

### Multi-Camera Monitoring
```
1. Open app in multiple browser tabs
2. Each tab: different camera RTSP URL
3. Monitor multiple cameras simultaneously
```

---

## ✨ Tips & Best Practices

1. **Test with Demo Mode first** - Verify detection works
2. **Start with IP cameras** - Most reliable on cloud
3. **Use strong credentials** - For network cameras
4. **Monitor bandwidth** - RTSP streams consume data
5. **Keep URLs accessible** - Test URLs before deploying
6. **Use compression** - For uploaded videos
7. **Verify firewall rules** - For network access

---

## 🆘 Support

If something doesn't work:
1. Try Demo Mode to verify app works
2. Test camera URL in VLC first
3. Check internet connectivity
4. Review error message carefully
5. Try a different video source

---

## 🎯 Summary

| Method | Cloud | Local | Best For |
|--------|:-----:|:-----:|----------|
| IP Camera | ✅ | ✅ | Security cameras |
| Upload Video | ✅ | ✅ | Archived footage |
| Stream URL | ✅ | ✅ | Public streams |
| Live Camera | ❌ | ✅ | Webcam input |
| Demo Mode | ✅ | ✅ | Testing |

**Choose the method that works best for your use case!** 🚀
