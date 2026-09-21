"""
URL configuration for sai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-homepage/', views.user_homepage, name='user_homepage'),  # new user homepage url
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path("forgot-password/",views.forgot_password, name="forgot_password"),
    path("verify-otp/",views.verify_otp, name="verify_otp"),
    path("reset-password/",views.reset_password, name="reset_password"),

    # Crime Detection Endpoints
    path('detect-image/', views.detect_image, name='detect_image'),
    path('detect-video/', views.detect_video, name='detect_video'),
    path('live-detection/', views.live_detection, name='live_detection'),
    path('detection-results/<int:detection_id>/', views.detection_results, name='detection_results'),

    # Enhanced Detection Endpoints
    path('enhanced-detect-image/', views.enhanced_detect_image, name='enhanced_detect_image'),
    path('enhanced-detect-video/', views.enhanced_detect_video, name='enhanced_detect_video'),

    # Gemini API Configuration
    path('gemini-config/', views.gemini_config, name='gemini_config'),
    path('view-reports/', views.view_reports, name='view_reports'),
    path('download-report/<int:report_id>/', views.download_report, name='download_report'),
    path('test-gemini-api/', views.test_gemini_api, name='test_gemini_api'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
