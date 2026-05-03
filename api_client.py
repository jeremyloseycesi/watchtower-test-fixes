"""
API client with various security vulnerabilities.

⚠️ WARNING: DO NOT USE IN PRODUCTION!
"""

import requests
import json
import hashlib
import random

# VULNERABILITY: Hardcoded API tokens
STRIPE_SECRET_KEY = "fake_stripe_key_for_testing_only"
TWILIO_AUTH_TOKEN = "fake_twilio_token_1234567890abcdef"
GITHUB_TOKEN = "fake_github_token_demo_not_real_key"

# Expected fix:
# import os
# STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class APIClient:
    """Client for external API calls."""
    
    def __init__(self):
        self.base_url = "https://api.example.com"
        self.session = requests.Session()
        # FIXED: SSL verification enabled
        self.session.verify = True  # Always verify SSL certificates
    
    # Expected fix:
    # self.session.verify = True  # Always verify SSL
    
    def make_request(self, endpoint, data):
        """
        VULNERABILITY: No input validation or sanitization.
        """
        # UNSAFE: Directly using user input in URL
        url = f"{self.base_url}/{endpoint}"
        
        # FIXED: SSL verification enabled, but timeout still missing
        response = requests.post(
            url,
            json=data,
            verify=True,  # FIXED: SSL verification enabled
            timeout=None   # UNSAFE: No timeout!
        )
        
        return response.json()
    
    # Expected fix:
    # def make_request(self, endpoint, data):
    #     from urllib.parse import quote
    #     endpoint = quote(endpoint, safe='')
    #     url = f"{self.base_url}/{endpoint}"
    #     
    #     response = requests.post(
    #         url,
    #         json=data,
    #         verify=True,
    #         timeout=30
    #     )
    #     response.raise_for_status()
    #     return response.json()


def generate_token():
    """
    VULNERABILITY: Weak random number generation for security token.
    """
    # UNSAFE: random is not cryptographically secure
    token = ''.join([str(random.randint(0, 9)) for _ in range(32)])
    return token

# Expected fix:
# import secrets
# def generate_token():
#     return secrets.token_urlsafe(32)


def encrypt_data(data, key="default_key_123"):
    """
    VULNERABILITY: Weak encryption with hardcoded key.
    """
    # UNSAFE: Simple XOR is NOT encryption!
    key_bytes = key.encode()
    data_bytes = data.encode()
    
    encrypted = bytes([data_bytes[i] ^ key_bytes[i % len(key_bytes)] 
                      for i in range(len(data_bytes))])
    
    return encrypted.hex()

# Expected fix:
# from cryptography.fernet import Fernet
# def encrypt_data(data, key):
#     f = Fernet(key)
#     return f.encrypt(data.encode()).decode()


def log_request(request_data):
    """
    VULNERABILITY: Logging sensitive data.
    """
    # UNSAFE: Logging passwords and tokens!
    print(f"Request: {json.dumps(request_data)}")
    # This will log passwords, API keys, etc.

# Expected fix:
# def log_request(request_data):
#     safe_data = {k: v for k, v in request_data.items() 
#                  if k not in ['password', 'token', 'api_key', 'secret']}
#     print(f"Request: {json.dumps(safe_data)}")


class SessionManager:
    """Session handling with vulnerabilities."""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id):
        """
        VULNERABILITY: Predictable session IDs.
        """
        # UNSAFE: Predictable session generation
        session_id = hashlib.md5(f"{user_id}_{random.randint(1000, 9999)}".encode()).hexdigest()
        
        # VULNERABILITY: No session expiration
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': None  # No expiration tracking!
        }
        
        return session_id
    
    # Expected fix:
    # import secrets
    # from datetime import datetime, timedelta
    # 
    # def create_session(self, user_id):
    #     session_id = secrets.token_urlsafe(32)
    #     expires_at = datetime.utcnow() + timedelta(hours=24)
    #     
    #     self.sessions[session_id] = {
    #         'user_id': user_id,
    #         'created_at': datetime.utcnow(),
    #         'expires_at': expires_at
    #     }
    #     
    #     return session_id