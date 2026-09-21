# Troubleshooting Common Errors

## Error: "partially initialized module 'torchvision' has no attribute 'extension'"

### Cause
This error occurs due to a circular import issue with PyTorch/torchvision, often caused by:
- Mismatched torch/torchvision versions
- Corrupted installation
- Python cache issues

### Solution 1: Reinstall PyTorch (Recommended)
```bash
# Uninstall existing packages
pip uninstall -y torch torchvision torchaudio

# Reinstall with compatible versions
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Solution 2: Clear Python Cache
```bash
# Find and remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Or on Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

### Solution 3: Use Virtual Environment
```bash
# Create fresh virtual environment
python -m venv venv_new

# Activate it
# Windows:
venv_new\Scripts\activate
# Linux/Mac:
source venv_new/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Solution 4: Check for Conflicting Files
```bash
# Make sure there's no file named 'torch.py' or 'torchvision.py' in your project
find . -name "torch.py" -o -name "torchvision.py"
```

---

## Error: "Model file not found"

### Solution
```bash
# Clone the weapon detection model
git clone https://huggingface.co/jparedesDS/cs2-yolo12m-weapon-detection
```

---

## Error: "CUDA not available" or GPU errors

### Solution
Use CPU version of PyTorch:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

## Error: "No module named 'cv2'"

### Solution
```bash
pip install opencv-python
# or
pip install opencv-python-headless
```

---

## Error: "Django migrations not applied"

### Solution
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Error: "Permission denied" on startup script

### Solution (Linux/Mac)
```bash
chmod +x start_enhanced.sh
./start_enhanced.sh
```

---

## Error: Video processing is very slow

### Solutions
1. Process shorter videos
2. Reduce video resolution
3. Edit `enhanced_detector.py` line 286: Change `if frame_count % 3 == 0:` to `if frame_count % 5 == 0:` (process every 5th frame)

---

## Error: "File upload failed"

### Check
1. File size limits in Django settings
2. Media directory exists and is writable
3. File format is supported

---

## Error: "Database is locked"

### Solution
```bash
# Close all Django processes
# Delete db.sqlite3.lock if it exists
rm db.sqlite3.lock

# Restart server
python manage.py runserver
```

---

## General Debugging Steps

1. **Check Django Console**
   - Look for error messages in the terminal where you ran `python manage.py runserver`

2. **Check Browser Console**
   - Press F12 in browser
   - Look for JavaScript errors

3. **Verify Dependencies**
   ```bash
   pip list
   ```

4. **Test Basic Functionality**
   ```bash
   python manage.py check
   ```

5. **Check Python Version**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

---

## Still Having Issues?

1. Check all documentation files
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Try creating a fresh virtual environment
5. Check file permissions
6. Verify database migrations

---

**Last Updated**: March 30, 2026
