"""
Test script to verify YOLO installation and detection
Run this to ensure everything is working before starting the server
"""

import sys
import os

print("=" * 60)
print("AI Crime Detection System - Installation Test")
print("=" * 60)
print()

# Test 1: Python version
print("[1/7] Checking Python version...")
print(f"Python {sys.version}")
if sys.version_info < (3, 8):
    print("❌ ERROR: Python 3.8+ required")
    sys.exit(1)
print("✅ Python version OK")
print()

# Test 2: Import Django
print("[2/7] Testing Django...")
try:
    import django
    print(f"✅ Django {django.get_version()} installed")
except ImportError:
    print("❌ ERROR: Django not installed. Run: pip install -r requirements.txt")
    sys.exit(1)
print()

# Test 3: Import OpenCV
print("[3/7] Testing OpenCV...")
try:
    import cv2
    print(f"✅ OpenCV {cv2.__version__} installed")
except ImportError:
    print("❌ ERROR: OpenCV not installed. Run: pip install opencv-python")
    sys.exit(1)
print()

# Test 4: Import NumPy
print("[4/7] Testing NumPy...")
try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} installed")
except ImportError:
    print("❌ ERROR: NumPy not installed. Run: pip install numpy")
    sys.exit(1)
print()

# Test 5: Import PyTorch
print("[5/7] Testing PyTorch...")
try:
    import torch
    print(f"✅ PyTorch {torch.__version__} installed")
    if torch.cuda.is_available():
        print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  CUDA not available (CPU mode - slower but works)")
except ImportError:
    print("❌ ERROR: PyTorch not installed. Run: pip install torch torchvision")
    sys.exit(1)
print()

# Test 6: Import Ultralytics YOLO
print("[6/7] Testing Ultralytics YOLO...")
try:
    from ultralytics import YOLO
    print("✅ Ultralytics installed")

    # Try loading model
    print("   Downloading/Loading YOLOv8 model (first time may take a while)...")
    model = YOLO('yolov8n.pt')
    print("✅ YOLOv8 detection model loaded successfully")

    # Try loading segmentation model
    print("   Loading YOLOv8 segmentation model...")
    seg_model = YOLO('yolov8n-seg.pt')
    print("✅ YOLOv8 segmentation model loaded successfully")

except ImportError:
    print("❌ ERROR: Ultralytics not installed. Run: pip install ultralytics")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Warning: {str(e)}")
    print("   Models will download on first use")
print()

# Test 7: Check project structure
print("[7/7] Checking project structure...")
required_dirs = ['users', 'templates', 'sai']
required_files = ['manage.py', 'requirements.txt']

all_ok = True
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"✅ {dir_name}/ exists")
    else:
        print(f"❌ {dir_name}/ missing")
        all_ok = False

for file_name in required_files:
    if os.path.exists(file_name):
        print(f"✅ {file_name} exists")
    else:
        print(f"❌ {file_name} missing")
        all_ok = False

# Check utils directory
if os.path.exists('users/utils'):
    print("✅ users/utils/ exists")
    utils_files = ['yolo_detector.py', 'segmentation.py', 'tracker.py']
    for util_file in utils_files:
        if os.path.exists(f'users/utils/{util_file}'):
            print(f"   ✅ {util_file}")
        else:
            print(f"   ❌ {util_file} missing")
            all_ok = False
else:
    print("❌ users/utils/ missing")
    all_ok = False

print()

# Final result
print("=" * 60)
if all_ok:
    print("✅ ALL TESTS PASSED!")
    print()
    print("Next steps:")
    print("1. Run migrations: python manage.py migrate")
    print("2. Start server: python manage.py runserver")
    print("3. Open browser: http://127.0.0.1:8000/")
    print()
    print("Admin credentials:")
    print("   URL: http://127.0.0.1:8000/admin-login/")
    print("   Username: admin")
    print("   Password: admin")
else:
    print("❌ SOME TESTS FAILED")
    print("Please fix the errors above before running the server")
print("=" * 60)
