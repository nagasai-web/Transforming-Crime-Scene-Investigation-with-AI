#!/bin/bash

# Enhanced Crime Detection System - Quick Start Script
# This script helps you get started with the enhanced detection features

echo "=========================================="
echo "Enhanced Crime Detection System Setup"
echo "=========================================="
echo ""

# Check if weapon model exists
if [ ! -d "cs2-yolo12m-weapon-detection" ]; then
    echo "❌ Weapon detection model not found!"
    echo "📥 Cloning weapon detection model from HuggingFace..."
    git clone https://huggingface.co/jparedesDS/cs2-yolo12m-weapon-detection
    echo "✅ Model downloaded successfully!"
else
    echo "✅ Weapon detection model found!"
fi

echo ""
echo "Checking Python dependencies..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created!"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

echo ""
echo "Installing/Updating dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 Starting Django development server..."
echo ""
echo "Access the application at: http://127.0.0.1:8000/"
echo ""
echo "Default Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Enhanced Features Available:"
echo "  ✓ Weapon Detection (19 types)"
echo "  ✓ Blood Stain Detection"
echo "  ✓ Broken Glass Detection"
echo "  ✓ Bullet Shell Detection"
echo "  ✓ Violence/Fight Detection"
echo "  ✓ Comprehensive Risk Assessment"
echo ""
echo "=========================================="
echo ""

python manage.py runserver
