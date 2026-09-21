# Complete Usage Guide - AI Crime Detection System

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd "C:\Users\Lenovo\Desktop\test\crime type and occurence sabari"
pip install -r requirements.txt
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Start Server
```bash
python manage.py runserver
```

**Access at:** http://127.0.0.1:8000/

---

## Complete Workflow

### 1. First Time Setup

#### A. Test Installation
```bash
python test_installation.py
```

This will verify:
- Python version
- All dependencies
- YOLO models
- Project structure

#### B. Create Media Directory
```bash
mkdir media
```

#### C. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. User Registration

1. Go to: http://127.0.0.1:8000/
2. Click **"Register"**
3. Fill in the form:
   - Name
   - Email
   - Mobile Number
   - Password
   - Upload Profile Photo
4. Click **"Register"**
5. Wait for admin approval

### 3. Admin Approval

1. Go to: http://127.0.0.1:8000/admin-login/
2. Login with:
   - **Username:** admin
   - **Password:** admin
3. Click **"View Dashboard"**
4. Find registered user
5. Click **"Activate"** button
6. User can now login

### 4. User Login

1. Go to: http://127.0.0.1:8000/user-login/
2. Enter credentials
3. Access dashboard

---

## Feature Guide

### 🖼️ Image Detection

**Purpose:** Detect weapons, persons, and crime objects in images

**Steps:**
1. From dashboard, click **"Upload Image"** card
2. Click upload area or drag & drop image
3. Select image file (JPG, PNG, JPEG)
4. Click **"🔍 Detect Objects"**
5. Wait for processing (5-10 seconds)

**Results Show:**
- Original vs Detected image comparison
- Risk level badge (HIGH/MEDIUM/NORMAL)
- Total objects detected
- Person count
- Weapon count
- Segmentation results (blood/glass)
- Detailed object list with confidence scores
- Bounding box coordinates

**Actions:**
- Print report
- Download results as JSON
- Back to dashboard

---

### 🎥 Video Detection

**Purpose:** Process video files frame-by-frame with object tracking

**Steps:**
1. From dashboard, click **"Upload Video"** card
2. Select video file (MP4, AVI, MOV)
3. Click **"🎬 Process Video"**
4. Wait for processing (depends on video length)

**Processing Time:**
- 30 second video: ~2-3 minutes
- 1 minute video: ~5-6 minutes
- 5 minute video: ~25-30 minutes

**Results Show:**
- Original vs Processed video (side-by-side)
- Frames processed count
- Detection summary (bar chart)
- Object counts per class
- FPS information

**Actions:**
- Play/pause videos
- Download processed video
- Print report
- Back to dashboard

---

### 📹 Live Detection

**Purpose:** Real-time crime detection using webcam

**Steps:**
1. From dashboard, click **"Start Live Feed"** card
2. Browser will ask for camera permission - **Allow**
3. Click **"🚀 Start Detection"**
4. Detection runs in real-time

**Features:**
- Live video feed with overlays
- Real-time object detection
- FPS counter
- Object count
- Risk level indicator
- Detection log (scrollable)
- Automatic alerts for weapons
- Frame capture capability

**Controls:**
- **Start Detection** - Begin processing
- **Stop Detection** - Pause processing
- **Capture Frame** - Save current frame as image
- **Back to Dashboard** - Return to main page

**Live Stats:**
- Total detections
- Person count
- Weapon count
- Frames processed

**Alerts:**
- Yellow alert: Person detected
- Red alert: Weapon detected
- Auto-dismiss after 5 seconds

---

## Detection Classes Explained

### Objects Detected by YOLO

| Class | Description | Risk Factor |
|-------|-------------|-------------|
| Person | Human detection | Medium (if with weapon) |
| Knife | Sharp weapon | High |
| Scissors | Sharp object | Medium |
| Bottle | Blunt object (proxy for bat) | Low |
| Sports ball | Proxy for bullet shell | Low |

### Segmentation Detection

| Type | Method | Indicator |
|------|--------|-----------|
| Blood Stains | HSV color detection (red) | High risk |
| Broken Glass | Edge detection + shape analysis | Medium risk |

### Risk Level Calculation

```
HIGH RISK:
- Person + Weapon detected
- Person + Blood detected

MEDIUM RISK:
- Weapon only
- 3+ persons
- Blood or glass detected

NORMAL:
- No weapons
- 1-2 persons
- No blood/glass
```

---

## Understanding Results

### Detection Results Page

**Risk Badge Colors:**
- 🔴 Red = HIGH RISK
- 🟠 Orange = MEDIUM RISK
- 🟢 Green = NORMAL

**Confidence Score:**
- 0.90-1.00 = Very confident
- 0.70-0.89 = Confident
- 0.50-0.69 = Moderate
- Below 0.50 = Low confidence (filtered out)

**Bounding Box Format:**
```
[x1, y1, x2, y2]
x1, y1 = Top-left corner
x2, y2 = Bottom-right corner
```

### JSON Export Format

```json
{
  "detection": {
    "objects": [
      {
        "class": "person",
        "confidence": 0.92,
        "bbox": [100, 150, 300, 450]
      }
    ],
    "count": {
      "person": 1,
      "weapon": 0,
      "total": 1
    },
    "risk_level": "NORMAL"
  },
  "segmentation": {
    "blood": {
      "blood_detected": false,
      "count": 0
    },
    "glass": {
      "glass_detected": false,
      "count": 0
    }
  }
}
```

---

## Troubleshooting

### Camera Not Working

**Problem:** Live detection shows black screen

**Solutions:**
1. Check browser permissions (Settings → Privacy → Camera)
2. Use Chrome or Edge (best compatibility)
3. Try HTTPS or localhost only
4. Close other apps using camera
5. Restart browser

### Slow Detection

**Problem:** Processing takes too long

**Solutions:**
1. Use smaller images (resize to 640x640)
2. Use shorter videos (under 1 minute)
3. Close other applications
4. Use GPU if available
5. Switch to yolov8n (nano) model

### Model Download Fails

**Problem:** YOLO models won't download

**Solutions:**
1. Check internet connection
2. Manually download:
   ```bash
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```
3. Download from: https://github.com/ultralytics/assets/releases

### Import Errors

**Problem:** Module not found errors

**Solutions:**
```bash
# Reinstall dependencies
pip uninstall -y ultralytics opencv-python torch
pip install -r requirements.txt

# Or install individually
pip install ultralytics==8.1.0
pip install opencv-python==4.9.0.80
pip install torch==2.1.2
```

### Database Errors

**Problem:** Database locked or migration errors

**Solutions:**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate

# Or reset migrations
python manage.py migrate --run-syncdb
```

---

## Performance Optimization

### For Faster Detection

1. **Use GPU:**
   ```bash
   # Install CUDA-enabled PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Reduce Image Size:**
   - Resize images to 640x640 before upload
   - Use image compression

3. **Use Smaller Model:**
   Edit `users/utils/yolo_detector.py`:
   ```python
   self.model = YOLO('yolov8n.pt')  # Fastest
   ```

4. **Process Fewer Frames:**
   Edit `users/utils/yolo_detector.py` in `detect_video()`:
   ```python
   # Process every 2nd frame instead of all
   if frame_count % 2 == 0:
       # Run detection
   ```

### For Better Accuracy

1. **Use Larger Model:**
   ```python
   self.model = YOLO('yolov8x.pt')  # Most accurate
   ```

2. **Increase Confidence Threshold:**
   ```python
   results = self.model(img, conf=0.5)  # Only 50%+ confidence
   ```

3. **Use Higher Resolution:**
   ```python
   results = self.model(img, imgsz=1280)  # Larger image size
   ```

---

## API Usage (For Developers)

### Image Detection API

```python
import requests

url = 'http://127.0.0.1:8000/detect-image/'
files = {'image': open('crime_scene.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### Video Detection API

```python
import requests

url = 'http://127.0.0.1:8000/detect-video/'
files = {'video': open('footage.mp4', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

---

## Best Practices

### For Image Detection
- Use clear, well-lit images
- Avoid blurry or low-resolution images
- Center objects in frame
- Use images with good contrast

### For Video Detection
- Keep videos under 2 minutes for faster processing
- Use 30 FPS videos
- Ensure good lighting
- Stable camera (not shaky)

### For Live Detection
- Position camera at eye level
- Ensure good lighting
- Stable internet connection
- Close unnecessary browser tabs

---

## Security Recommendations

⚠️ **Before Production Deployment:**

1. Change admin password
2. Use environment variables for secrets
3. Enable HTTPS
4. Add rate limiting
5. Implement proper authentication
6. Sanitize file uploads
7. Add file size limits
8. Use secure database (PostgreSQL)

---

## Support & Help

### Getting Help

1. Check this guide first
2. Review README.md
3. Run test_installation.py
4. Check Django logs in terminal
5. Check browser console (F12)

### Common Commands

```bash
# Start server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test installation
python test_installation.py

# Check Python packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## Keyboard Shortcuts

### In Browser
- `Ctrl + Shift + I` - Open developer tools
- `F5` - Refresh page
- `Ctrl + P` - Print report
- `Esc` - Close modal

### In Terminal
- `Ctrl + C` - Stop server
- `Ctrl + Z` - Pause process
- `↑` - Previous command

---

**System Ready!** Follow the steps above to start detecting crime scenes.
