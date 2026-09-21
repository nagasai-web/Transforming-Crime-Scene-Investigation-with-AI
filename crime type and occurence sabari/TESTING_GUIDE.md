# Testing Guide - Enhanced Crime Detection System

## 🧪 Complete Testing Checklist

### Prerequisites
- [ ] Django server running (`python manage.py runserver`)
- [ ] Weapon detection model downloaded
- [ ] User account created and approved by admin
- [ ] Test images/videos prepared

---

## 1️⃣ Basic System Test

### Test Admin Login
1. Navigate to `http://127.0.0.1:8000/admin-login/`
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. ✅ Should redirect to admin dashboard
4. Verify user approval functionality

### Test User Registration & Login
1. Navigate to `http://127.0.0.1:8000/register/`
2. Fill registration form with test data
3. Upload a profile image
4. ✅ Should show "Wait for admin approval" message
5. Login as admin and approve the user
6. Navigate to `http://127.0.0.1:8000/user-login/`
7. Login with registered credentials
8. ✅ Should redirect to user dashboard

---

## 2️⃣ Standard Detection Tests

### Test Standard Image Detection
1. Login as user
2. Click "Image Detection" card
3. Upload a test image (person, object, etc.)
4. Click "Detect Objects"
5. ✅ Verify:
   - Image displays correctly
   - Bounding boxes drawn
   - Detection results shown
   - Risk level calculated

### Test Standard Video Detection
1. Click "Video Analysis" card
2. Upload a short test video (MP4)
3. Click "Process Video"
4. Wait for processing
5. ✅ Verify:
   - Video processes without errors
   - Annotated video plays
   - Frame count displayed
   - Detection summary shown

---

## 3️⃣ Enhanced Detection Tests

### Test Enhanced Image Detection - Weapons

**Test Case 1: Weapon Detection**
1. Click "Enhanced Image Detection" card (red border)
2. Upload image containing weapons/guns
3. Click "Enhanced Detection"
4. ✅ Expected Results:
   - Weapons detected with red bounding boxes
   - Weapon type labeled (AK47, M4A1, etc.)
   - Confidence score displayed
   - Risk level: HIGH RISK or CRITICAL
   - Weapon count in summary

**Test Case 2: Blood Detection**
1. Upload image with red/blood-like stains
2. Run enhanced detection
3. ✅ Expected Results:
   - Blood regions highlighted in magenta
   - "BLOOD" label on detected areas
   - Area measurement in pixels
   - Blood count in summary
   - Risk level elevated

**Test Case 3: Broken Glass Detection**
1. Upload image with broken glass/shattered surfaces
2. Run enhanced detection
3. ✅ Expected Results:
   - Glass fragments outlined in cyan
   - "GLASS" label on detected areas
   - Fragment count displayed
   - Property damage indicator

**Test Case 4: Bullet Shell Detection**
1. Upload image with metallic/golden cylindrical objects
2. Run enhanced detection
3. ✅ Expected Results:
   - Shells detected with orange boxes
   - "BULLET SHELL" label
   - Shell count in summary
   - Firearm discharge indicator

**Test Case 5: Violence/Fight Detection**
1. Upload image with multiple persons in close proximity
2. Run enhanced detection
3. ✅ Expected Results:
   - Violence score calculated (0-100)
   - Violence indicators listed
   - Alert banner if score > 0
   - Risk level elevated

**Test Case 6: Comprehensive Scene**
1. Upload image with multiple indicators:
   - Persons
   - Weapons
   - Blood
   - Glass
2. Run enhanced detection
3. ✅ Expected Results:
   - All elements detected
   - Risk level: CRITICAL
   - Comprehensive summary
   - All detection categories populated
   - "Alert Authorities" button visible

### Test Enhanced Video Detection

**Test Case 1: Weapon Video**
1. Click "Enhanced Video Analysis" card
2. Upload video containing weapons
3. Click "Enhanced Analysis"
4. Wait for processing (may take several minutes)
5. ✅ Expected Results:
   - Video processes every 3rd frame
   - Weapon detections accumulated
   - Frame counter visible
   - Detection breakdown by category
   - Progress bars showing detection frequency
   - Annotated video playable

**Test Case 2: Violence Video**
1. Upload video with multiple persons interacting
2. Run enhanced analysis
3. ✅ Expected Results:
   - Violence frames counted
   - Violence score calculated
   - Alert banner if high risk
   - Person proximity detected

**Test Case 3: Comprehensive Video**
1. Upload video with multiple crime indicators
2. Run enhanced analysis
3. ✅ Expected Results:
   - All detection types tracked
   - Comprehensive statistics grid
   - AI-generated report (if Gemini configured)
   - Download options available
   - High risk alert if applicable

---

## 4️⃣ UI/UX Tests

### Dashboard Tests
1. ✅ User avatar displays correctly
2. ✅ Login time shows in correct format
3. ✅ Stats cards display (even if 0)
4. ✅ Action cards are clickable
5. ✅ Enhanced cards have red border
6. ✅ Recent activity section populated
7. ✅ Modals open/close properly

### Results Page Tests
1. ✅ Images display side-by-side
2. ✅ Risk badge animates (pulse effect)
3. ✅ Detection items have hover effects
4. ✅ Confidence bars animate
5. ✅ Download buttons work
6. ✅ Print functionality works
7. ✅ Back to dashboard button works

### Video Results Tests
1. ✅ Video player controls work
2. ✅ Statistics grid displays correctly
3. ✅ Progress bars show accurate percentages
4. ✅ Detection breakdown organized by category
5. ✅ AI report displays (if available)
6. ✅ Download video button works
7. ✅ Download report button works

---

## 5️⃣ Performance Tests

### Image Processing Speed
- **Expected**: 2-5 seconds per image
- **Test**: Upload 5 different images, measure time
- ✅ Average time: _____ seconds

### Video Processing Speed
- **Expected**: 3-10 minutes per minute of video
- **Test**: Upload 30-second video, measure time
- ✅ Processing time: _____ seconds

### Memory Usage
- **Test**: Monitor system memory during video processing
- ✅ Peak memory usage: _____ MB

---

## 6️⃣ Error Handling Tests

### Invalid File Upload
1. Try uploading non-image file to image detection
2. ✅ Should show error message

### Large File Upload
1. Try uploading very large video (>100MB)
2. ✅ Should process or show size limit error

### Missing Model
1. Temporarily rename weapon model folder
2. Try enhanced detection
3. ✅ Should fallback to standard YOLOv8 with warning

### Network Interruption
1. Start video processing
2. Disconnect network (if using external APIs)
3. ✅ Should handle gracefully

---

## 7️⃣ Integration Tests

### Gemini API Integration (Optional)
1. Configure Gemini API key in admin
2. Process a video
3. ✅ AI report generated
4. ✅ Report saved to database
5. ✅ Report downloadable

### Database Tests
1. Process multiple detections
2. Check database for VideoAnalysisReport entries
3. ✅ Reports saved correctly
4. ✅ User associations correct

---

## 8️⃣ Security Tests

### Authentication Tests
1. Try accessing `/user-homepage/` without login
2. ✅ Should redirect to login
3. Try accessing enhanced detection without login
4. ✅ Should redirect to login

### File Upload Security
1. Try uploading executable files
2. ✅ Should reject or sanitize
3. Try uploading files with malicious names
4. ✅ Should handle safely

---

## 9️⃣ Browser Compatibility Tests

Test on multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

For each browser, verify:
- ✅ Dashboard loads correctly
- ✅ Modals work
- ✅ File uploads work
- ✅ Video playback works
- ✅ Animations smooth

---

## 🔟 Mobile Responsiveness Tests

Test on mobile devices or browser dev tools:
- [ ] Dashboard layout adapts
- [ ] Cards stack vertically
- [ ] Modals are usable
- [ ] Images scale properly
- [ ] Buttons are tappable

---

## 📊 Test Results Summary

| Test Category | Pass | Fail | Notes |
|---------------|------|------|-------|
| Basic System | ☐ | ☐ | |
| Standard Detection | ☐ | ☐ | |
| Enhanced Image Detection | ☐ | ☐ | |
| Enhanced Video Detection | ☐ | ☐ | |
| UI/UX | ☐ | ☐ | |
| Performance | ☐ | ☐ | |
| Error Handling | ☐ | ☐ | |
| Integration | ☐ | ☐ | |
| Security | ☐ | ☐ | |
| Browser Compatibility | ☐ | ☐ | |
| Mobile Responsiveness | ☐ | ☐ | |

---

## 🐛 Known Issues / Limitations

1. **Video Processing Speed**: Large videos may take significant time
   - Workaround: Process every 3rd frame (configurable)

2. **Blood Detection Accuracy**: Color-based detection may have false positives
   - Limitation: Red objects may be detected as blood

3. **Glass Detection**: Edge-based detection may miss some fragments
   - Limitation: Depends on image quality and lighting

4. **Violence Detection**: Proximity-based, not pose-based
   - Limitation: May miss some violence types

5. **Bullet Shell Detection**: Shape/color based, not ML model
   - Limitation: May have false positives with similar objects

---

## 📝 Test Report Template

```
Test Date: _______________
Tester Name: _______________
System: Windows/Linux/Mac
Browser: _______________
Python Version: _______________

Summary:
- Total Tests: _____
- Passed: _____
- Failed: _____
- Skipped: _____

Critical Issues Found:
1.
2.
3.

Recommendations:
1.
2.
3.

Overall Assessment: PASS / FAIL / NEEDS WORK
```

---

## 🚀 Quick Test Commands

```bash
# Test server is running
curl http://127.0.0.1:8000/

# Test admin login page
curl http://127.0.0.1:8000/admin-login/

# Test user login page
curl http://127.0.0.1:8000/user-login/

# Check if weapon model exists
ls cs2-yolo12m-weapon-detection/

# Check database
python manage.py dbshell
SELECT * FROM users_registereduser;
SELECT * FROM users_videoanalysisreport;
```

---

## 📞 Support

If tests fail:
1. Check Django console for errors
2. Check browser console (F12)
3. Verify all dependencies installed
4. Ensure weapon model downloaded
5. Check file permissions
6. Review ENHANCED_FEATURES.md

---

**Happy Testing! 🎉**
