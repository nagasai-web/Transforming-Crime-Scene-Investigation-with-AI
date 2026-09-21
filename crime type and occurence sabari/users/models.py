from django.db import models

class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)  # store plain for demo; use hashing in prod!
    image = models.ImageField(upload_to='user_images/')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GeminiAPIConfig(models.Model):
    api_key = models.CharField(max_length=500)
    model_name = models.CharField(max_length=100, default='gemini-2.5-flash')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gemini API Config - {self.model_name}"

    class Meta:
        verbose_name = "Gemini API Configuration"
        verbose_name_plural = "Gemini API Configurations"


class VideoAnalysisReport(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=255)
    video_path = models.CharField(max_length=500)
    detection_summary = models.TextField()
    gemini_report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.video_name} by {self.user.name}"

    class Meta:
        ordering = ['-created_at']
