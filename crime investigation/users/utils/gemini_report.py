"""
Google Gemini 2.5 Flash Integration
Generates AI-powered video analysis reports
"""

import google.generativeai as genai
from django.conf import settings

class GeminiReportGenerator:
    def __init__(self, api_key):
        """Initialize Gemini with API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Gemini 2.5 Flash

    def generate_video_report(self, detection_data, video_info):
        """
        Generate comprehensive video analysis report

        Args:
            detection_data: Dictionary with detection results
            video_info: Dictionary with video metadata

        Returns:
            String containing formatted report
        """

        # Prepare prompt for Gemini
        prompt = self._create_prompt(detection_data, video_info)

        try:
            # Generate report using Gemini
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating report: {str(e)}"

    def _create_prompt(self, detection_data, video_info):
        """Create detailed prompt for Gemini"""

        frames_processed = detection_data.get('frames_processed', 0)
        detections = detection_data.get('detections', {})
        video_name = video_info.get('name', 'Unknown')
        duration = video_info.get('duration', 'Unknown')

        # Build detection summary
        detection_summary = []
        for obj_class, count in detections.items():
            detection_summary.append(f"- {obj_class.title()}: {count} detections")

        detection_text = "\n".join(detection_summary) if detection_summary else "No objects detected"

        prompt = f"""
You are a professional crime scene analyst. Generate a comprehensive video analysis report based on the following detection data:

VIDEO INFORMATION:
- Video Name: {video_name}
- Duration: {duration}
- Frames Processed: {frames_processed}

DETECTION RESULTS:
{detection_text}

Please generate a detailed professional report with the following sections:

1. EXECUTIVE SUMMARY
   - Brief overview of the video analysis
   - Key findings and risk assessment

2. DETECTION TIMELINE
   - Chronological breakdown of detections
   - Estimated timeframes for each detection type
   - Pattern analysis

3. OBJECT ANALYSIS
   - Detailed analysis of each detected object type
   - Frequency and distribution
   - Potential significance

4. RISK ASSESSMENT
   - Overall threat level (HIGH/MEDIUM/LOW)
   - Specific concerns identified
   - Recommended actions

5. TECHNICAL DETAILS
   - Detection methodology
   - Confidence levels
   - Processing statistics

6. CONCLUSIONS AND RECOMMENDATIONS
   - Summary of findings
   - Next steps
   - Additional investigation suggestions

Format the report professionally with clear headings, bullet points, and proper structure.
Make it suitable for law enforcement or security personnel.
"""

        return prompt

    def generate_frame_analysis(self, frame_detections):
        """
        Generate analysis for specific frames

        Args:
            frame_detections: List of detections per frame

        Returns:
            String containing frame-by-frame analysis
        """

        prompt = f"""
Analyze the following frame-by-frame detection data and provide insights:

{frame_detections}

Provide:
1. Timeline of events
2. Key moments identified
3. Patterns or anomalies
4. Critical frames requiring attention
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating frame analysis: {str(e)}"

    def generate_summary(self, detection_results):
        """
        Generate quick summary of detections

        Args:
            detection_results: Dictionary with detection data

        Returns:
            String containing brief summary
        """

        prompt = f"""
Generate a brief 2-3 sentence summary of this crime scene video analysis:

Detection Results:
{detection_results}

Focus on the most critical findings and overall risk level.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
