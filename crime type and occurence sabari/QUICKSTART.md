# 🚀 QUICK START GUIDE

## Installation (5 Minutes)

### Option 1: Automated (Windows)
```bash
# Double-click start.bat
# OR run in terminal:
start.bat
```

### Option 2: Manual
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Start server
python manage.py runserver
```

## Access URLs

- **Home:** http://127.0.0.1:8000/
- **User Login:** http://127.0.0.1:8000/user-login/
- **Admin Login:** http://127.0.0.1:8000/admin-login/

## Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin`

## First Steps

1. ✅ Register new user account
2. ✅ Login as admin and activate user
3. ✅ Login as user
4. ✅ Upload image/video for detection
5. ✅ View results

## Features

✅ **Image Detection** - Upload crime scene images
✅ **Video Detection** - Process video files
✅ **Live Detection** - Real-time webcam monitoring
✅ **Object Detection** - Weapons, persons, objects
✅ **Segmentation** - Blood stains, broken glass
✅ **Person Tracking** - Track individuals with IDs
✅ **Risk Assessment** - Automatic risk calculation
✅ **Modern Dashboard** - Beautiful responsive UI

## Detection Classes

- Person
- Knife
- Gun/Rifle
- Bat
- Rope
- Bullet Shell
- Blood Stains
- Broken Glass

## Risk Levels

🔴 **HIGH RISK** - Person + Weapon + Blood
🟠 **MEDIUM RISK** - Weapon only or 3+ persons
🟢 **NORMAL** - No threats detected

## File Structure

```
crime type and occurence sabari/
├── manage.py                    # Django management
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── USAGE_GUIDE.md              # Detailed usage guide
├── start.bat                    # Quick start script
├── test_installation.py         # Installation test
├── db.sqlite3                   # Database
│
├── sai/                         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                       # Main app
│   ├── models.py
│   ├── views.py                # Detection logic
│   ├── admin.py
│   └── utils/                  # AI modules
│       ├── yolo_detector.py    # Object detection
│       ├── segmentation.py     # Blood/glass detection
│       └── tracker.py          # Person tracking
│
├── templates/                   # HTML templates
│   ├── home.html
│   ├── register.html
│   ├── user_login.html
│   ├── admin_login.html
│   └── users/
│       ├── user_homepage.html  # Main dashboard
│       ├── detection_results.html
│       ├── video_results.html
│       └── live_detection.html
│
└── media/                       # Uploaded files
```

## Commands Cheat Sheet

```bash
# Start server
python manage.py runserver

# Test installation
python test_installation.py

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Install dependencies
pip install -r requirements.txt

# Check installed packages
pip list
```

## Troubleshooting

### Camera not working?
- Allow camera permissions in browser
- Use Chrome or Edge
- Check if other apps are using camera

### Slow detection?
- Use smaller images (640x640)
- Use shorter videos (< 1 minute)
- Close other applications

### Import errors?
```bash
pip install -r requirements.txt --upgrade
```

### Database errors?
```bash
python manage.py migrate --run-syncdb
```

## Performance Tips

**Faster Detection:**
- Use GPU (install CUDA PyTorch)
- Use yolov8n (nano) model
- Reduce image resolution
- Process fewer video frames

**Better Accuracy:**
- Use yolov8x (xlarge) model
- Use higher resolution images
- Increase confidence threshold

## Tech Stack

- **Backend:** Django 5.0
- **AI:** YOLOv8, OpenCV, PyTorch
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite

## System Requirements

- Python 3.8+
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Webcam (for live detection)
- Modern browser (Chrome/Edge)

## Support

📖 **Full Documentation:** README.md
📋 **Usage Guide:** USAGE_GUIDE.md
🧪 **Test Script:** test_installation.py

## Next Steps

1. Read USAGE_GUIDE.md for detailed instructions
2. Run test_installation.py to verify setup
3. Start the server and explore features
4. Customize detection classes as needed
5. Train custom models (optional)

---

**Ready to detect crime scenes!** 🔍

Run `python manage.py runserver` and open http://127.0.0.1:8000/
