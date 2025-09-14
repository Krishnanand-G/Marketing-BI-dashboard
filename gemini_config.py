import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def configure_gemini():
    api_key = None
    
    print("Checking secrets...")
    print("Has secrets attr:", hasattr(st, 'secrets'))
    
    if hasattr(st, 'secrets'):
        print("Available secrets keys:", list(st.secrets.keys()))
        try:
            if "secrets" in st.secrets:
                api_key = st.secrets["secrets"]["GEMINI_API_KEY"]
                print(f"GEMINI_API_KEY found in Streamlit secrets (nested): {api_key[:10]}...")
            else:
                api_key = st.secrets["GEMINI_API_KEY"]
                print(f"GEMINI_API_KEY found in Streamlit secrets (direct): {api_key[:10]}...")
        except KeyError as e:
            print(f"GEMINI_API_KEY not found in Streamlit secrets: {e}")
        except Exception as e:
            print(f"Error accessing secrets: {e}")
    else:
        print("No secrets available")
    
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print(f"GEMINI_API_KEY found in environment variables: {api_key[:10]}...")
        else:
            print("GEMINI_API_KEY not found in environment variables")
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
