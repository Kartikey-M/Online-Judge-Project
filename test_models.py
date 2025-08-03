#!/usr/bin/env python
"""
Test script to check available Gemini models
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

import google.generativeai as genai
from django.conf import settings

def test_available_models():
    """Test available Gemini models."""
    print("Testing Available Gemini Models...")
    print("=" * 50)
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # List all available models
    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
    
    print("\n" + "=" * 50)
    
    # Test different model versions
    models_to_test = [
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash', 
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    for model_name in models_to_test:
        try:
            print(f"\nTesting {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello, this is a test message. Please respond briefly.")
            print(f"✅ {model_name}: Working - {response.text[:50]}...")
        except Exception as e:
            print(f"❌ {model_name}: {str(e)}")

if __name__ == "__main__":
    test_available_models()
