# AI-Based Crime Scene Detection System

Complete Django application with YOLOv8 for real-time crime detection.

## Features

✅ Image Detection - Upload and analyze crime scene images
✅ Video Detection - Process video files frame-by-frame
✅ Live Detection - Real-time webcam monitoring
✅ Object Detection - Detect weapons, persons, and crime-related objects
✅ Segmentation - Blood stains and broken glass detection
✅ Person Tracking - Track individuals with unique IDs
✅ Risk Assessment - Automatic risk level calculation
✅ User Management - Admin approval system
✅ Modern UI - Responsive dashboard with real-time stats

## Detection Classes

- Person
- Knife
- Gun/Rifle
- Bat
- Rope
- Bullet Shell
- Blood Stains (Segmentation)
- Broken Glass (Segmentation)

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **AI/ML**: YOLOv8 (Ultralytics), OpenCV, PyTorch
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default)

## Installation

### 1. Clone/Navigate to Project

```bash
cd "C:\Users\Lenovo\Desktop\test\crime type and occurence sabari"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download YOLOv8 Models

The models will auto-download on first run, or manually download:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt'); YOLO('yolov8n-seg.pt')"
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Media Directories

```bash
mkdir media
mkdir media/uploads
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Server will start at: **http://127.0.0.1:8000/**

## Usage Guide

### 1. Access the Application

Open browser and go to: `http://127.0.0.1:8000/`

### 2. Register User Account

- Click "Register"
- Fill in details (name, email, mobile, password, upload photo)
- Wait for admin approval

### 3. Admin Login

- Go to: `http://127.0.0.1:8000/admin-login/`
- Username: `admin`
- Password: `admin`
- Approve registered users from dashboard

### 4. User Login

- Login with approved credentials
- Access user dashboard

### 5. Image Detection

1. Click "Upload Image" card
2. Select crime scene image
3. Click "Detect Objects"
4. View results with bounding boxes and risk level

### 6. Video Detection

1. Click "Upload Video" card
2. Select video file (MP4, AVI, MOV)
3. Click "Process Video"
4. Wait for processing
5. View annotated video with detection stats

### 7. Live Detection

1. Click "Start Live Feed" card
2. Allow camera access
3. Click "Start Detection"
4. Real-time detection with alerts
5. Capture frames as needed

## API Endpoints

```
POST /detect-image/          - Upload and detect objects in image
POST /detect-video/          - Upload and process video
GET  /live-detection/        - Live camera detection page
GET  /detection-results/<id>/ - View detection results
```

## Project Structure

```
crime type and occurence sabari/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── sai/                          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                        # Main app
│   ├── models.py                 # User model
│   ├── views.py                  # All views and detection logic
│   ├── admin.py
│   └── utils/                    # Detection modules
│       ├── yolo_detector.py      # YOLO object detection
│       ├── segmentation.py       # Blood/glass segmentation
│       └── tracker.py            # Person tracking
│
├── templates/                    # HTML templates
│   ├── home.html
│   ├── register.html
│   ├── user_login.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── users/
│       ├── user_base.html
│       ├── user_homepage.html    # Main dashboard
│       ├── detection_results.html
│       ├── video_results.html
│       └── live_detection.html
│
└── media/                        # Uploaded files
    └── uploads/
```

## How It Works

### Object Detection Flow

1. **Image Upload** → Saved to media folder
2. **YOLO Processing** → YOLOv8 detects objects
3. **Bounding Boxes** → Drawn on image with labels
4. **Risk Calculation** → Based on person + weapon logic
5. **Results Display** → Annotated image + JSON data

### Risk Level Logic

```python
if (person_count > 0 AND weapon_count > 0):
    risk = "HIGH RISK"
elif (weapon_count > 0):
    risk = "MEDIUM RISK"
elif (person_count > 3):
    risk = "MEDIUM RISK"
else:
    risk = "NORMAL"
```

### Segmentation Process

1. **Blood Detection** → HSV color space red detection
2. **Glass Detection** → Edge detection + shape analysis
3. **YOLO Segmentation** → Mask overlay on objects
4. **Combined Results** → All segments merged

### Person Tracking

1. **Centroid Tracking** → Calculate object centers
2. **Distance Matching** → Match across frames
3. **Unique IDs** → Assign persistent IDs
4. **Trajectory Drawing** → Show movement path

## Configuration

### Settings (sai/settings.py)

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email settings for OTP (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Model Selection

Edit `users/utils/yolo_detector.py`:

```python
# Change model size (n=nano, s=small, m=medium, l=large, x=xlarge)
self.model = YOLO('yolov8n.pt')  # Fastest
self.model = YOLO('yolov8s.pt')  # Balanced
self.model = YOLO('yolov8m.pt')  # More accurate
```

## Troubleshooting

### Issue: Models not downloading

```bash
# Manually download
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-seg.pt
```

### Issue: OpenCV error

```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

### Issue: CUDA not available

```bash
# Install CPU version of PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Camera not working

- Check browser permissions
- Use HTTPS or localhost
- Try different browser (Chrome recommended)

## Performance Tips

1. **Use GPU** - Install CUDA-enabled PyTorch for faster detection
2. **Reduce Resolution** - Lower video resolution for faster processing
3. **Adjust FPS** - Process fewer frames per second
4. **Use Smaller Model** - yolov8n is fastest, yolov8x is most accurate

## Custom Training (Optional)

To train on custom crime dataset:

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov8n.pt')

# Train on custom dataset
model.train(
    data='crime_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)
```

## Security Notes

⚠️ **Important:**
- Change admin credentials in production
- Use environment variables for secrets
- Enable HTTPS in production
- Implement proper authentication
- Sanitize file uploads
- Add rate limiting

## Future Enhancements

- [ ] Database storage for detection history
- [ ] Export reports as PDF
- [ ] Email alerts for high-risk detections
- [ ] Multi-camera support
- [ ] Custom model training interface
- [ ] REST API with authentication
- [ ] Mobile app integration
- [ ] Cloud deployment

## License

MIT License - Free to use and modify

## Support

For issues or questions:
- Check troubleshooting section
- Review Django logs: `python manage.py runserver`
- Check browser console for frontend errors

## Credits

- YOLOv8: Ultralytics
- Django: Django Software Foundation
- OpenCV: OpenCV Team

---

**Ready to use!** Just follow installation steps and start detecting.
