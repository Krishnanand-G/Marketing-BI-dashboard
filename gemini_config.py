import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def configure_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        print("GEMINI_API_KEY found in Streamlit secrets")
    except:
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print("GEMINI_API_KEY found in environment variables")
        else:
            print("GEMINI_API_KEY not found in environment variables or secrets")
            api_key = "your_gemini_api_key_here"
    
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            genai.configure(api_key=api_key)
            print("Gemini API configured successfully")
            return True
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            return False
    else:
        print("Invalid API key provided")
        return False

def get_gemini_model():
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        try:
            return genai.GenerativeModel('gemini-pro')
        except Exception as e2:
            print(f"Error getting Gemini model: {e2}")
            return None
