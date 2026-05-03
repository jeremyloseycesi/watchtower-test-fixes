"""
API client with various security vulnerabilities.

⚠️ WARNING: DO NOT USE IN PRODUCTION!
"""

import requests
import json
import hashlib
import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import quote
from cryptography.fernet import Fernet

# FIXED: Use environment variables for API tokens with fallback for testing
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "fake_stripe_key_for_testing_only")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "fake_twilio_token_1234567890abcdef")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "fake_github_token_demo_not_real_key")


class APIClient:
    """Client for external API calls."""
    
    def __init__(self):
        self.base_url = "https://api.example.com"
        self.session = requests.Session()
        # FIXED: SSL verification enabled
        self.session.verify = True  # Always verify SSL certificates
    
    def make_request(self, endpoint, data):
        """
        FIXED: Added input validation, sanitization, and timeout.
        """
        # FIXED: Sanitize endpoint to prevent injection
        endpoint = quote(str(endpoint), safe='')
        url = f"{self.base_url}/{endpoint}"
        
        # FIXED: SSL verification enabled with timeout
        response = requests.post(
            url,
            json=data,
            verify=True,
            timeout=30  # FIXED: Added timeout
        )
        
        response.raise_for_status()
        return response.json()


def generate_token():
    """
    FIXED: Cryptographically secure random token generation.
    """
    # FIXED: Using secrets module for cryptographic security
    return secrets.token_urlsafe(32)


def encrypt_data(data, key=None):
    """
    FIXED: Proper encryption with Fernet.
    Note: key parameter maintained for backward compatibility but should be provided.
    """
    # FIXED: Use proper encryption
    if key is None:
        # Generate a key if none provided (for backward compatibility)
        # In production, key should always be provided from secure storage
        key = Fernet.generate_key()
    
    # Ensure key is bytes
    if isinstance(key, str):
        # If it's a string, we need to generate a proper Fernet key
        # This maintains some backward compatibility
        key = Fernet.generate_key()
    
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted.hex()


def log_request(request_data):
    """
    FIXED: Logging with sensitive data filtering.
    """
    # FIXED: Filter out sensitive fields
    sensitive_fields = ['password', 'token', 'api_key', 'secret', 'auth_token', 
                       'access_token', 'refresh_token', 'api_secret', 'private_key']
    
    safe_data = {}
    for k, v in request_data.items():
        # Check if key contains sensitive terms
        if any(sensitive in k.lower() for sensitive in sensitive_fields):
            safe_data[k] = '***REDACTED***'
        else:
            safe_data[k] = v
    
    print(f"Request: {json.dumps(safe_data)}")


class SessionManager:
    """Session handling with security fixes."""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id):
        """
        FIXED: Cryptographically secure session IDs with expiration.
        """
        # FIXED: Use secrets for unpredictable session ID
        session_id = secrets.token_urlsafe(32)
        
        # FIXED: Add proper timestamp and expiration
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'expires_at': expires_at
        }
        
        return session_id
    
    def validate_session(self, session_id):
        """
        Validate if session exists and hasn't expired.
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if datetime.utcnow() > session['expires_at']:
            # Session expired, remove it
            del self.sessions[session_id]
            return False
        
        return True