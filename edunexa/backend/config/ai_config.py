import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_config():
    """Get Gemini AI configuration"""
    return {
        'api_key': os.getenv('GOOGLE_API_KEY'),
        'model_name': os.getenv('GEMINI_MODEL', 'gemini-1.5-pro'),
        'temperature': 0.7,
        'max_tokens': 2048,
        'top_p': 0.8,
        'top_k': 40
    }

def validate_ai_config():
    """Validate AI configuration"""
    config = get_gemini_config()
    
    if not config['api_key']:
        raise ValueError("GOOGLE_API_KEY is required in environment variables")
    
    return True