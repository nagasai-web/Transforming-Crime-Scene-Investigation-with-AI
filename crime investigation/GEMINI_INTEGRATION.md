# 🤖 Google Gemini 2.5 Flash Integration Guide

## Overview

The system now includes Google Gemini 2.5 Flash AI integration for automatic video analysis report generation. When users upload videos, the system generates comprehensive AI-powered reports with timeline analysis, risk assessment, and recommendations.

---

## Features Added

### 1. Admin Configuration Page
- **URL:** http://127.0.0.1:8000/gemini-config/
- Configure Gemini API key
- Select model (Gemini 2.0 Flash recommended)
- Enable/disable AI report generation
- Test API key functionality

### 2. Automatic Report Generation
- AI reports generated automatically on video upload
- Timeline-based detection analysis
- Risk assessment and recommendations
- Professional format suitable for law enforcement

### 3. Reports Management
- **URL:** http://127.0.0.1:8000/view-reports/
- View all generated reports
- Download reports as text files
- Search and filter reports

---

## Setup Instructions

### Step 1: Install Google Generative AI Library

```bash
pip install google-generativeai==0.3.2
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Run Migrations

```bash
python manage.py migrate
```

This creates two new database tables:
- `GeminiAPIConfig` - Stores API configuration
- `VideoAnalysisReport` - Stores generated reports

### Step 3: Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the generated API key

### Step 4: Configure in Admin Panel

1. Login as admin: http://127.0.0.1:8000/admin-login/
   - Username: `admin`
   - Password: `admin`

2. Click "Gemini AI Configuration"

3. Paste your API key

4. Select model: `Gemini 2.0 Flash (Recommended)`

5. Set status to "Active"

6. Click "Save Configuration"

7. (Optional) Click "Test API Key" to verify

---

## How It Works

### Video Upload Flow

```
User uploads video
    ↓
YOLO processes video (frame-by-frame detection)
    ↓
Detection results collected
    ↓
Gemini API called with detection data
    ↓
AI generates comprehensive report
    ↓
Report saved to database
    ↓
User sees results + AI report
```

### Report Generation Process

1. **Detection Data Collection:**
   - Frames processed
   - Objects detected (type and count)
   - Detection timeline

2. **Gemini Analysis:**
   - Executive summary
   - Timeline breakdown
   - Object analysis
   - Risk assessment
   - Technical details
   - Recommendations

3. **Report Storage:**
   - Saved to database
   - Linked to user and video
   - Accessible by admin

---

## Using the System

### For Users

1. **Upload Video:**
   - Login to user account
   - Click "Upload Video"
   - Select video file
   - Click "Process Video"

2. **View Results:**
   - Wait for processing (1-3 minutes)
   - View detection statistics
   - Read AI-generated report
   - Download report as text file

### For Admins

1. **Configure Gemini:**
   - Go to Admin Home
   - Click "Gemini AI Configuration"
   - Add/update API key
   - Save configuration

2. **View All Reports:**
   - Go to Admin Home
   - Click "View Reports"
   - Browse all generated reports
   - Download any report

---

## Report Structure

### 1. Executive Summary
- Brief overview of video analysis
- Key findings
- Overall risk assessment

### 2. Detection Timeline
- Chronological breakdown
- Estimated timeframes
- Pattern analysis

### 3. Object Analysis
- Detailed analysis per object type
- Frequency and distribution
- Significance assessment

### 4. Risk Assessment
- Threat level (HIGH/MEDIUM/LOW)
- Specific concerns
- Recommended actions

### 5. Technical Details
- Detection methodology
- Confidence levels
- Processing statistics

### 6. Conclusions
- Summary of findings
- Next steps
- Investigation suggestions

---

## API Endpoints

### Gemini Configuration
```
GET  /gemini-config/          - View/edit configuration
POST /gemini-config/          - Save configuration
POST /test-gemini-api/        - Test API key
```

### Reports Management
```
GET  /view-reports/           - View all reports
GET  /download-report/<id>/   - Download specific report
```

### Video Detection (Updated)
```
POST /detect-video/           - Upload video + generate AI report
```

---

## Database Models

### GeminiAPIConfig
```python
- api_key: CharField (500)
- model_name: CharField (100)
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### VideoAnalysisReport
```python
- user: ForeignKey (RegisteredUser)
- video_name: CharField (255)
- video_path: CharField (500)
- detection_summary: TextField
- gemini_report: TextField
- created_at: DateTimeField
```

---

## Configuration Options

### Model Selection

**Gemini 2.0 Flash (Recommended):**
- Fastest response time
- Most cost-effective
- Best for real-time analysis

**Gemini 1.5 Flash:**
- Balanced performance
- Good accuracy
- Moderate cost

**Gemini 1.5 Pro:**
- Highest accuracy
- Slower response
- Higher cost

### Status Options

**Active:**
- AI reports generated automatically
- Gemini API called on every video upload

**Inactive:**
- AI reports disabled
- Only YOLO detection runs
- No API calls made

---

## Troubleshooting

### Issue: API Key Invalid

**Error:** "API key test failed"

**Solutions:**
1. Verify API key is correct (no extra spaces)
2. Check API key is enabled in Google AI Studio
3. Ensure billing is set up (if required)
4. Try generating a new API key

### Issue: Report Not Generated

**Error:** Report shows "Processing..." or empty

**Solutions:**
1. Check Gemini config is Active
2. Verify API key is valid
3. Check internet connection
4. Review Django logs for errors
5. Ensure google-generativeai is installed

### Issue: Import Error

**Error:** "No module named 'google.generativeai'"

**Solution:**
```bash
pip install google-generativeai==0.3.2
```

### Issue: Migration Error

**Error:** "No such table: users_geminiapiconfig"

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Cost Considerations

### Gemini 2.0 Flash Pricing (as of 2026)

**Free Tier:**
- 15 requests per minute
- 1 million tokens per day
- Suitable for testing and small deployments

**Paid Tier:**
- $0.075 per 1M input tokens
- $0.30 per 1M output tokens
- Typical report: ~2000 tokens = $0.0006

**Estimated Costs:**
- 100 videos/day: ~$0.06/day
- 1000 videos/day: ~$0.60/day
- Very affordable for most use cases

---

## Security Best Practices

### API Key Security

1. **Never commit API keys to Git:**
   ```bash
   # Add to .gitignore
   *.env
   local_settings.py
   ```

2. **Use environment variables (Production):**
   ```python
   import os
   api_key = os.environ.get('GEMINI_API_KEY')
   ```

3. **Restrict API key permissions:**
   - Only enable Generative AI API
   - Set usage quotas
   - Monitor usage regularly

4. **Rotate keys periodically:**
   - Generate new key every 90 days
   - Update in admin panel
   - Revoke old keys

---

## Advanced Usage

### Custom Prompts

Edit `users/utils/gemini_report.py` to customize report format:

```python
def _create_prompt(self, detection_data, video_info):
    prompt = f"""
    Your custom prompt here...

    Include detection data: {detection_data}
    Include video info: {video_info}

    Generate report with your custom sections...
    """
    return prompt
```

### Frame-by-Frame Analysis

Enable detailed frame analysis:

```python
# In detect_video view
frame_analysis = gemini_gen.generate_frame_analysis(frame_detections)
```

### Quick Summaries

Generate brief summaries:

```python
summary = gemini_gen.generate_summary(detection_results)
```

---

## Testing

### Test API Connection

```python
from users.utils.gemini_report import GeminiReportGenerator

api_key = "your-api-key-here"
gemini = GeminiReportGenerator(api_key)

test_data = {
    'frames_processed': 100,
    'detections': {'person': 5, 'knife': 1}
}

video_info = {
    'name': 'test.mp4',
    'duration': '10 seconds'
}

report = gemini.generate_video_report(test_data, video_info)
print(report)
```

### Test via Admin UI

1. Go to Gemini Configuration
2. Enter API key
3. Click "Test API Key"
4. Should show "✅ API Key is valid!"

---

## Files Modified/Created

### New Files
```
✅ users/utils/gemini_report.py       - Gemini integration
✅ templates/gemini_config.html       - Admin config page
✅ templates/view_reports.html        - Reports listing page
✅ GEMINI_INTEGRATION.md             - This guide
```

### Modified Files
```
✅ users/models.py                    - Added GeminiAPIConfig, VideoAnalysisReport
✅ users/views.py                     - Added gemini views, updated detect_video
✅ sai/urls.py                        - Added gemini routes
✅ templates/admin_home.html          - Added Gemini config link
✅ templates/users/video_results.html - Added AI report display
✅ requirements.txt                   - Added google-generativeai
```

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Get Gemini API key from Google AI Studio
4. ✅ Configure in admin panel
5. ✅ Test with sample video
6. ✅ Review generated report
7. ✅ Customize prompts if needed

---

## Support

### Documentation
- Google AI Studio: https://aistudio.google.com/
- Gemini API Docs: https://ai.google.dev/docs
- Django Docs: https://docs.djangoproject.com/

### Common Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Access admin
http://127.0.0.1:8000/admin-login/
```

---

**Gemini Integration Complete!** 🎉

The system now automatically generates AI-powered video analysis reports using Google Gemini 2.5 Flash.
