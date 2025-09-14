# Gemini API Configuration
# Instructions:
# 1. Get your API key from: https://makersuite.google.com/app/apikey
# 2. Set your API key as an environment variable or replace the key below
# 3. For deployment, use environment variables for security

import os
import google.generativeai as genai

def configure_gemini():
    """Configure Gemini API with API key"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        # For local development, you can set the key directly here
        # WARNING: Never commit API keys to version control
        api_key = "AIzaSyCeuWmsjSNj9EMpXy-DHA53lZUUzBsKOVQ"  # Replace with your actual key
        
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
        return True
    else:
        return False

def get_gemini_model():
    """Get the Gemini model instance"""
    try:
        # Try the newer model name first
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        try:
            # Fallback to older model name
            return genai.GenerativeModel('gemini-pro')
        except Exception as e2:
            print(f"Error getting Gemini model: {e2}")
            return None
