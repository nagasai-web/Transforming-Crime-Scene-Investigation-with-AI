from django.shortcuts import render, redirect
from django.utils import timezone
from .models import RegisteredUser, VideoAnalysisReport
from django.core.files.storage import FileSystemStorage

def register_view(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        # Basic validation
        if not (name and email and mobile and password and image):
            msg = "All fields are required."
        else:
            # Save image manually
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            img_url = fs.url(filename)

            # Save user with is_active=False
            RegisteredUser.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                password=password,
                image=filename,
                is_active=False
            )
            msg = "Registered successfully! Wait for admin approval."

    return render(request, 'register.html', {'msg': msg})

from django.utils import timezone

from django.utils import timezone
import pytz

def user_login(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = RegisteredUser.objects.get(name=name, password=password)
            if user.is_active:
                # Convert current time to IST
                ist = pytz.timezone('Asia/Kolkata')
                local_time = timezone.now().astimezone(ist)

                # Save user info in session
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_image'] = user.image.url  # image URL
                request.session['login_time'] = local_time.strftime('%I:%M:%S %p')

                return redirect('user_homepage')
            else:
                msg = "Your account is not activated yet."
        except RegisteredUser.DoesNotExist:
            msg = "Invalid credentials."

    return render(request, 'user_login.html', {'msg': msg})

def admin_login(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if name == 'admin' and password == 'admin':
            return redirect('admin_home')
        else:
            msg = "Invalid admin credentials."

    return render(request, 'admin_login.html', {'msg': msg})

def admin_home(request):
    return render(request, 'admin_home.html')
    
def admin_dashboard(request):
    users = RegisteredUser.objects.all()
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    inactive_users = total_users - active_users

    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }
    return render(request, 'admin_dashboard.html', context)

def activate_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_dashboard')

def deactivate_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_dashboard')

def delete_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')



def home(request):
    return render(request, 'home.html')


def user_homepage(request):
    if 'user_id' not in request.session:
        # User not logged in, redirect to login page
        return redirect('user_login')

    user_name = request.session.get('user_name')
    user_image = request.session.get('user_image')
    login_time = request.session.get('login_time')

    # Project stats from VideoAnalysisReport data
    user = RegisteredUser.objects.get(id=request.session['user_id'])
    total_detections = VideoAnalysisReport.objects.filter(user=user).count()
    high_risk_cases = VideoAnalysisReport.objects.filter(
        user=user,
        detection_summary__contains="'risk_level': 'CRITICAL'"
    ).count()
    processed_today = VideoAnalysisReport.objects.filter(
        user=user,
        created_at__date=timezone.now().date()
    ).count()

    context = {
        'user_name': user_name,
        'user_image': user_image,
        'login_time': login_time,
        'total_detections': total_detections,
        'high_risk_cases': high_risk_cases,
        'processed_today': processed_today,
    }
    return render(request, 'users/user_homepage.html', context)

def user_logout(request):
    request.session.flush()  # Clears all session data
    return redirect('user_login')



import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import RegisteredUser

otp_storage = {}  # Temporary dictionary to store OTPs

def send_otp(email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    otp_storage[email] = otp

    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"
    from_email = "saikumardatapoint1@gmail.com"  # Change this to your email
    send_mail(subject, message, from_email, [email])

    return otp

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if RegisteredUser.objects.filter(email=email).exists():
            send_otp(email)
            request.session["reset_email"] = email  # Store email in session
            return redirect("verify_otp")
        else:
            messages.error(request, "Email not registered!")

    return render(request, "forgot_password.html")

def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        email = request.session.get("reset_email")

        if otp_storage.get(email) and str(otp_storage[email]) == otp_entered:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP!")

    return render(request, "verify_otp.html")

def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        email = request.session.get("reset_email")

        if RegisteredUser.objects.filter(email=email).exists():
            user = RegisteredUser.objects.get(email=email)
            user.password = new_password  # Updating password
            user.save()
            messages.success(request, "Password reset successful! Please log in.")
            return redirect("user_login")

    return render(request, "reset_password.html")


# ==================== GEMINI API CONFIGURATION ====================

from .models import GeminiAPIConfig, VideoAnalysisReport
from django.http import HttpResponse

def gemini_config(request):
    """
    Admin page to configure Gemini API
    """
    msg = ''
    error = ''
    current_config = GeminiAPIConfig.objects.first()

    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        model_name = request.POST.get('model_name', 'gemini-2.5-flash')
        is_active = request.POST.get('is_active', 'true') == 'true'

        if not api_key:
            error = "API Key is required"
        else:
            # Update or create configuration
            if current_config:
                current_config.api_key = api_key
                current_config.model_name = model_name
                current_config.is_active = is_active
                current_config.save()
                msg = "Gemini API configuration updated successfully!"
            else:
                GeminiAPIConfig.objects.create(
                    api_key=api_key,
                    model_name=model_name,
                    is_active=is_active
                )
                msg = "Gemini API configuration saved successfully!"

            current_config = GeminiAPIConfig.objects.first()

    context = {
        'current_config': current_config,
        'msg': msg,
        'error': error
    }

    return render(request, 'gemini_config.html', context)


def view_reports(request):
    """
    Admin page to view all video analysis reports
    """
    reports = VideoAnalysisReport.objects.all().order_by('-created_at')

    context = {
        'reports': reports
    }

    return render(request, 'view_reports.html', context)


def download_report(request, report_id):
    """
    Download report as text file
    """
    try:
        report = VideoAnalysisReport.objects.get(id=report_id)

        # Create text content
        content = f"""
VIDEO ANALYSIS REPORT
{'=' * 80}

Video Name: {report.video_name}
Analyzed By: {report.user.name}
Date: {report.created_at.strftime('%B %d, %Y %H:%M')}

{'=' * 80}

DETECTION SUMMARY:
{report.detection_summary}

{'=' * 80}

AI-GENERATED ANALYSIS (Gemini 2.5 Flash):
{report.gemini_report if report.gemini_report else 'Not available'}

{'=' * 80}

Generated by AI Crime Detection System
"""

        # Create HTTP response with text file
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="report_{report.id}.txt"'

        return response

    except VideoAnalysisReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)


def test_gemini_api(request):
    """
    Test Gemini API key
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        api_key = data.get('api_key')

        try:
            from .utils.gemini_report import GeminiReportGenerator

            gemini_gen = GeminiReportGenerator(api_key)

            # Test with simple prompt
            test_prompt = "Say 'API connection successful' if you can read this."
            response = gemini_gen.model.generate_content(test_prompt)

            return JsonResponse({
                'success': True,
                'message': 'API key is valid and working!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)
# ==================== CRIME DETECTION VIEWS ====================

import os
import json
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .utils.yolo_detector import CrimeDetector
from .utils.segmentation import CrimeSegmentation
from .utils.tracker import PersonTracker

# Initialize detectors
crime_detector = CrimeDetector()
crime_segmentation = CrimeSegmentation()
person_tracker = PersonTracker()

# Import enhanced detector
from .utils.enhanced_detector import EnhancedCrimeDetector
enhanced_detector = EnhancedCrimeDetector()

def detect_image(request):
    """
    Image detection endpoint
    Upload image -> Run YOLO -> Return results
    """
    if request.method == 'POST' and request.FILES.get('image'):
        # Check if user is logged in
        if 'user_id' not in request.session:
            return redirect('user_login')

        # Save uploaded image
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        try:
            # Run object detection
            annotated_img, detection_results = crime_detector.detect_objects(image_path)

            # Run segmentation
            seg_img, seg_results = crime_segmentation.segment_all(image_path)

            # Save annotated image
            output_filename = f"detected_{filename}"
            output_path = fs.path(output_filename)
            import cv2
            cv2.imwrite(output_path, annotated_img)

            # Save report record so homepage stats are up-to-date
            try:
                user = RegisteredUser.objects.get(id=request.session['user_id'])
                VideoAnalysisReport.objects.create(
                    user=user,
                    video_name=filename,
                    video_path=output_path,
                    detection_summary=str({
                        'object_detection': detection_results,
                        'segmentation': seg_results
                    }),
                    gemini_report=''
                )
            except Exception:
                pass

            # Prepare response
            context = {
                'success': True,
                'original_image': fs.url(filename),
                'detected_image': fs.url(output_filename),
                'detection_results': detection_results,
                'segmentation_results': seg_results,
                'user_name': request.session.get('user_name'),
                'user_image': request.session.get('user_image'),
            }

            return render(request, 'users/detection_results.html', context)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return redirect('user_homepage')


def detect_video(request):
    """
    Video detection endpoint
    Upload video -> Process frames -> Return annotated video
    """
    if request.method == 'POST' and request.FILES.get('video'):
        # Check if user is logged in
        if 'user_id' not in request.session:
            return redirect('user_login')

        # Save uploaded video
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        video_path = fs.path(filename)

        try:
            # Process video
            output_filename = f"detected_{filename}"
            output_path = fs.path(output_filename)

            # Run detection on video
            video_results = crime_detector.detect_video(video_path, output_path)

            # Get Gemini API configuration
            from .models import GeminiAPIConfig, VideoAnalysisReport, RegisteredUser

            gemini_report = None
            try:
                gemini_config = GeminiAPIConfig.objects.filter(is_active=True).first()

                if gemini_config:
                    # Generate AI report using Gemini
                    from .utils.gemini_report import GeminiReportGenerator

                    gemini_gen = GeminiReportGenerator(gemini_config.api_key)

                    # Prepare video info
                    video_info = {
                        'name': filename,
                        'duration': f"{video_results['frames_processed'] / 30:.2f} seconds"
                    }

                    # Generate report
                    gemini_report = gemini_gen.generate_video_report(video_results, video_info)

                    # Save report to database
                    user = RegisteredUser.objects.get(id=request.session['user_id'])
                    VideoAnalysisReport.objects.create(
                        user=user,
                        video_name=filename,
                        video_path=output_path,
                        detection_summary=str(video_results),
                        gemini_report=gemini_report
                    )
            except Exception as e:
                print(f"Gemini report generation failed: {str(e)}")
                gemini_report = None

            # Prepare response
            context = {
                'success': True,
                'original_video': fs.url(filename),
                'detected_video': fs.url(output_filename),
                'video_results': video_results,
                'gemini_report': gemini_report,
                'user_name': request.session.get('user_name'),
                'user_image': request.session.get('user_image'),
            }

            return render(request, 'users/video_results.html', context)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return redirect('user_homepage')


def live_detection(request):
    """
    Live camera detection
    Stream from webcam and run real-time detection
    """
    if 'user_id' not in request.session:
        return redirect('user_login')

    context = {
        'user_name': request.session.get('user_name'),
        'user_image': request.session.get('user_image'),
    }

    return render(request, 'users/live_detection.html', context)


def detection_results(request, detection_id):
    """
    View detection results by ID
    """
    if 'user_id' not in request.session:
        return redirect('user_login')

    # Placeholder for database retrieval
    context = {
        'detection_id': detection_id,
        'user_name': request.session.get('user_name'),
        'user_image': request.session.get('user_image'),
    }

    return render(request, 'users/detection_results.html', context)


# ==================== ENHANCED DETECTION VIEWS ====================

def enhanced_detect_image(request):
    """
    Enhanced image detection with weapons, blood, glass, bullet shells, violence
    """
    if request.method == 'POST' and request.FILES.get('image'):
        if 'user_id' not in request.session:
            return redirect('user_login')

        # Save uploaded image
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        try:
            # Run enhanced detection
            annotated_img, detection_results = enhanced_detector.detect_all(image_path)

            # Save annotated image
            output_filename = f"enhanced_{filename}"
            output_path = fs.path(output_filename)
            import cv2
            cv2.imwrite(output_path, annotated_img)

            # Save report for dashboard metrics
            try:
                user = RegisteredUser.objects.get(id=request.session['user_id'])
                VideoAnalysisReport.objects.create(
                    user=user,
                    video_name=filename,
                    video_path=output_path,
                    detection_summary=str(detection_results),
                    gemini_report=''
                )
            except Exception:
                pass

            # Prepare response
            context = {
                'success': True,
                'original_image': fs.url(filename),
                'detected_image': fs.url(output_filename),
                'detection_results': detection_results,
                'user_name': request.session.get('user_name'),
                'user_image': request.session.get('user_image'),
            }

            return render(request, 'users/enhanced_detection_results.html', context)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return redirect('user_homepage')


def enhanced_detect_video(request):
    """
    Enhanced video detection with comprehensive crime scene analysis
    """
    if request.method == 'POST' and request.FILES.get('video'):
        if 'user_id' not in request.session:
            return redirect('user_login')

        # Save uploaded video
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        video_path = fs.path(filename)

        try:
            # Process video
            output_filename = f"enhanced_{filename}"
            output_path = fs.path(output_filename)

            # Run enhanced detection on video
            video_results = enhanced_detector.detect_video(video_path, output_path)

            # Get Gemini API configuration for report generation
            from .models import GeminiAPIConfig, VideoAnalysisReport, RegisteredUser

            # Save a report entry even if Gemini fails
            try:
                user = RegisteredUser.objects.get(id=request.session['user_id'])
                VideoAnalysisReport.objects.create(
                    user=user,
                    video_name=filename,
                    video_path=output_path,
                    detection_summary=str(video_results),
                    gemini_report=''
                )
            except Exception:
                pass

            gemini_report = None
            try:
                gemini_config = GeminiAPIConfig.objects.filter(is_active=True).first()

                if gemini_config:
                    from .utils.gemini_report import GeminiReportGenerator

                    gemini_gen = GeminiReportGenerator(gemini_config.api_key)

                    # Prepare video info
                    video_info = {
                        'name': filename,
                        'duration': f"{video_results['frames_processed'] / 30:.2f} seconds"
                    }

                    # Generate enhanced report
                    gemini_report = gemini_gen.generate_video_report(video_results, video_info)

                    # Update report with gemini output
                    VideoAnalysisReport.objects.filter(
                        user=user,
                        video_name=filename,
                        video_path=output_path
                    ).update(gemini_report=gemini_report)
            except Exception as e:
                print(f"Gemini report generation failed: {str(e)}")
                gemini_report = None

            # Prepare response
            context = {
                'success': True,
                'original_video': fs.url(filename),
                'detected_video': fs.url(output_filename),
                'video_results': video_results,
                'gemini_report': gemini_report,
                'user_name': request.session.get('user_name'),
                'user_image': request.session.get('user_image'),
            }

            return render(request, 'users/enhanced_video_results.html', context)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return redirect('user_homepage')
