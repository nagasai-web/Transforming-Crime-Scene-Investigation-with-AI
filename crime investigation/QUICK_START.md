# 🚀 Quick Start Guide - Enhanced Detection

## ⚡ 5-Minute Setup

### Step 1: Start the System
```bash
# Windows
start_enhanced.bat

# Linux/Mac
chmod +x start_enhanced.sh
./start_enhanced.sh
```

### Step 2: Access the Application
Open browser: `http://127.0.0.1:8000/`

### Step 3: Login
**Admin**: admin / admin
**User**: Register → Get approved → Login

---

## 🎯 Quick Feature Guide

### Standard Detection vs Enhanced Detection

| Feature | Standard | Enhanced |
|---------|----------|----------|
| Persons | ✅ | ✅ |
| Basic Weapons | ✅ | ✅ |
| Specialized Weapons (19 types) | ❌ | ✅ |
| Blood Stains | ❌ | ✅ |
| Broken Glass | ❌ | ✅ |
| Bullet Shells | ❌ | ✅ |
| Violence Detection | ❌ | ✅ |
| Risk Assessment | Basic | Advanced |
| Processing Speed | Fast | Moderate |

---

## 📸 Using Enhanced Image Detection

1. **Login** to user dashboard
2. **Click** "Enhanced Image Detection" (red border card)
3. **Upload** your crime scene image
4. **Click** "Enhanced Detection"
5. **View** comprehensive results:
   - Weapons detected
   - Blood stains
   - Broken glass
   - Bullet shells
   - Violence indicators
   - Risk level

**Processing Time**: 2-5 seconds

---

## 🎬 Using Enhanced Video Analysis

1. **Login** to user dashboard
2. **Click** "Enhanced Video Analysis" (red border card)
3. **Upload** your video file (MP4, AVI, MOV)
4. **Click** "Enhanced Analysis"
5. **Wait** for processing (3-10 min per min of video)
6. **View** detailed results:
   - Annotated video
   - Frame-by-frame statistics
   - Detection breakdown
   - AI-generated report (if configured)

**Tip**: Shorter videos process faster!

---

## 🎨 Understanding Risk Levels

### 🔴 CRITICAL
- Blood + Weapons + Persons detected
- Violence score > 60
- Multiple weapons (>2)
- **Action**: Immediate attention required

### 🟠 HIGH RISK
- Weapons + Persons present
- Significant blood (>2 stains)
- Multiple bullet shells (>3)
- Violence score > 30
- **Action**: Investigation needed

### 🟡 MEDIUM RISK
- Any weapons detected
- Any blood/shells present
- Broken glass (>3 fragments)
- Many persons (>5)
- **Action**: Monitor situation

### 🟢 NORMAL
- No significant threats
- **Action**: Routine processing

---

## 🔍 Detection Capabilities

### Weapons (19 Types)
- AK47, M4A1-S, M4A1
- GALIL, FAMAS, TEC-9
- FIVE-SEVEN, GLOCK-18, USP-S
- EAGLE, BERETTAS, P2000
- MAC10, MP5, MP9, P90, P250
- SSG08, AWP

### Blood Detection
- Red color segmentation
- Area measurement
- Location tracking

### Broken Glass
- Edge detection
- Fragment analysis
- Irregular shape identification

### Bullet Shells
- Metallic color detection
- Cylindrical shape analysis
- Size filtering

### Violence/Fight
- Person proximity analysis
- Close contact detection
- Violence score (0-100)

---

## 💡 Tips for Best Results

### Image Quality
- ✅ Good lighting
- ✅ Clear focus
- ✅ High resolution (640x640+)
- ❌ Avoid blurry images
- ❌ Avoid extreme angles

### Video Quality
- ✅ Stable camera
- ✅ Good frame rate (30fps+)
- ✅ Clear subjects
- ❌ Avoid shaky footage
- ❌ Avoid low light

### File Sizes
- **Images**: < 10 MB recommended
- **Videos**: < 100 MB recommended
- **Formats**: JPG, PNG, MP4, AVI, MOV

---

## 🛠️ Troubleshooting

### Issue: Weapon model not found
**Solution**: Run `git clone https://huggingface.co/jparedesDS/cs2-yolo12m-weapon-detection`

### Issue: Slow video processing
**Solution**:
- Use shorter videos
- Reduce video resolution
- Process every Nth frame (edit code)

### Issue: False blood detections
**Reason**: Color-based detection picks up red objects
**Solution**: Review results manually

### Issue: No detections
**Check**:
- Image quality
- Object visibility
- Lighting conditions
- File format

### Issue: Server error
**Check**:
- Django console for errors
- Browser console (F12)
- Dependencies installed
- Database migrated

---

## 📊 Understanding Results

### Detection Item Format
```
Class: AK47
Confidence: 0.95 (95%)
Location: [x1, y1, x2, y2]
```

### Confidence Scores
- **0.90-1.00**: Very confident
- **0.75-0.89**: Confident
- **0.50-0.74**: Moderate
- **< 0.50**: Low confidence

### Bounding Box Colors
- 🔴 **Red**: Weapons
- 🟢 **Green**: Persons
- 🟣 **Magenta**: Blood
- 🔵 **Cyan**: Glass
- 🟠 **Orange**: Bullet shells

---

## 📥 Downloading Results

### Image Results
- **JSON**: Click "Download JSON" button
- **Print**: Click "Print Report" button
- **Image**: Right-click detected image → Save

### Video Results
- **Video**: Click "Download Video" button
- **Report**: Click "Download Report" button
- **JSON**: Includes all statistics

---

## 🔐 Security Notes

- ✅ User authentication required
- ✅ Admin approval system
- ✅ Session-based access
- ✅ Secure file uploads
- ⚠️ Change admin password in production
- ⚠️ Use HTTPS in production
- ⚠️ Set proper file size limits

---

## 📞 Getting Help

### Documentation
1. **ENHANCED_FEATURES.md** - Complete feature docs
2. **TESTING_GUIDE.md** - Testing procedures
3. **ENHANCEMENT_SUMMARY.md** - What's new
4. **README.md** - Original documentation

### Common Commands
```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Check for errors
python manage.py check
```

### Debug Mode
Check Django console output for detailed error messages

---

## 🎯 Quick Test Checklist

- [ ] Server starts without errors
- [ ] Can login as admin
- [ ] Can register new user
- [ ] Can approve user as admin
- [ ] Can login as user
- [ ] Dashboard loads correctly
- [ ] Can upload image
- [ ] Standard detection works
- [ ] Enhanced detection works
- [ ] Results display correctly
- [ ] Can download results
- [ ] Video processing works
- [ ] Enhanced video works

---

## 🚀 Performance Tips

### For Faster Processing
1. Use smaller images/videos
2. Reduce video resolution
3. Use GPU if available
4. Close other applications
5. Process during off-peak hours

### For Better Accuracy
1. Use high-quality images
2. Ensure good lighting
3. Clear, focused subjects
4. Stable camera for videos
5. Appropriate distance from subjects

---

## 📈 System Requirements

### Minimum
- Python 3.8+
- 4 GB RAM
- 2 GB free disk space
- Modern web browser

### Recommended
- Python 3.10+
- 8 GB RAM
- 10 GB free disk space
- GPU (CUDA-enabled)
- Chrome/Edge browser

---

## 🎓 Learning Path

### Beginner
1. Read README.md
2. Follow Quick Start Guide (this file)
3. Test standard detection
4. Test enhanced detection

### Intermediate
1. Read ENHANCED_FEATURES.md
2. Follow TESTING_GUIDE.md
3. Experiment with different images
4. Configure Gemini API

### Advanced
1. Read code documentation
2. Customize detection algorithms
3. Train custom models
4. Integrate with other systems

---

## 🌟 Best Practices

### For Law Enforcement
- Document all detections
- Cross-reference with physical evidence
- Use high-quality source material
- Maintain chain of custody
- Review AI results manually

### For Security
- Regular monitoring
- Set up alerts for high-risk
- Archive important detections
- Train staff on system use
- Keep system updated

### For Research
- Use consistent test data
- Document methodology
- Compare with ground truth
- Analyze false positives/negatives
- Publish findings responsibly

---

## ✅ Success Indicators

You're using the system correctly if:
- ✅ Detections make sense
- ✅ Risk levels are appropriate
- ✅ Processing completes without errors
- ✅ Results are downloadable
- ✅ UI is responsive and clear

---

## 🎉 You're Ready!

The enhanced crime detection system is now ready to use. Start with simple test images, then move to more complex scenarios. Review the documentation for detailed information.

**Happy Detecting! 🔍**

---

*Quick Start Guide v2.0*
*Last Updated: March 30, 2026*
*For support, see documentation files*
