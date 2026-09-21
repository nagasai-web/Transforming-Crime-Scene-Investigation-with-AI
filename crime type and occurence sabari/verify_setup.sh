#!/bin/bash
# Installation and Setup Verification Script
# Run this after installation to verify everything is ready

echo "=========================================="
echo "AI Crime Detection System"
echo "Installation Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
CHECKS_PASSED=0
TOTAL_CHECKS=0

# Function to check file exists
check_file() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/ exists"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $1/ missing"
        return 1
    fi
}

echo "Checking Core Files..."
check_file "manage.py"
check_file "requirements.txt"
check_file "README.md"
check_file "USAGE_GUIDE.md"
check_file "QUICKSTART.md"
check_file "PROJECT_SUMMARY.md"
check_file "test_installation.py"
echo ""

echo "Checking Project Structure..."
check_dir "sai"
check_file "sai/settings.py"
check_file "sai/urls.py"
check_dir "users"
check_file "users/views.py"
check_file "users/models.py"
echo ""

echo "Checking AI Modules..."
check_dir "users/utils"
check_file "users/utils/__init__.py"
check_file "users/utils/yolo_detector.py"
check_file "users/utils/segmentation.py"
check_file "users/utils/tracker.py"
echo ""

echo "Checking Templates..."
check_dir "templates"
check_dir "templates/users"
check_file "templates/users/user_homepage.html"
check_file "templates/users/detection_results.html"
check_file "templates/users/video_results.html"
check_file "templates/users/live_detection.html"
echo ""

echo "=========================================="
echo "Verification Results"
echo "=========================================="
echo -e "Checks Passed: ${GREEN}${CHECKS_PASSED}${NC}/${TOTAL_CHECKS}"
echo ""

if [ $CHECKS_PASSED -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Install dependencies: pip install -r requirements.txt"
    echo "2. Run migrations: python manage.py migrate"
    echo "3. Start server: python manage.py runserver"
    echo "4. Open browser: http://127.0.0.1:8000/"
    echo ""
    echo "Admin Login:"
    echo "  URL: http://127.0.0.1:8000/admin-login/"
    echo "  Username: admin"
    echo "  Password: admin"
else
    echo -e "${RED}✗ SOME CHECKS FAILED${NC}"
    echo "Please ensure all files are present before running the server."
fi

echo "=========================================="
