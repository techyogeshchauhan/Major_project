# utils/validators.py
import re

def validate_email(email):
    """
    Simple email validation using regex.
    Returns True if valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Simple password validation.
    Rules: Minimum 8 chars, at least 1 uppercase, 1 lowercase, 1 digit
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True
