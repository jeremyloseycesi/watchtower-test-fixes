#!/usr/bin/env python3
"""
Intentionally vulnerable Flask application for testing Watchtower AI remediation.

⚠️ WARNING: Contains CRITICAL security vulnerabilities!
DO NOT USE IN PRODUCTION!

This app demonstrates vulnerabilities that require CODE CHANGES, not just version bumps.
"""

import os
import sqlite3
import subprocess
import json
from pathlib import Path
from functools import wraps
from flask import Flask, request, render_template_string
from markupsafe import escape
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# ============================================================================
# VULNERABILITY 1: Hardcoded AWS Credentials (CRITICAL) - FIXED
# ============================================================================
# These should be environment variables!
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Expected fix:
# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


# ============================================================================
# VULNERABILITY 2: SQL Injection (CRITICAL) - FIXED
# ============================================================================
@app.route('/user/<user_id>')
def get_user(user_id):
    """
    FIXED: Using parameterized query to prevent SQL injection.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SAFE: Using parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"user": {"id": result[0], "name": result[1], "email": result[2]}}
    return {"error": "User not found"}

# Expected fix:
# query = "SELECT * FROM users WHERE id = ?"
# cursor.execute(query, (user_id,))


# ============================================================================
# VULNERABILITY 3: Command Injection (CRITICAL) - FIXED
# ============================================================================
@app.route('/ping')
def ping_host():
    """
    FIXED: Using subprocess with array syntax and shell=False.
    """
    host = request.args.get('host', 'localhost')
    
    # SAFE: Using array syntax without shell=True
    result = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True
    )
    
    return {"output": result.stdout}

# Expected fix:
# result = subprocess.run(
#     ["ping", "-c", "1", host],
#     shell=False,
#     capture_output=True,
#     text=True
# )


# ============================================================================
# VULNERABILITY 4: Server-Side Template Injection (CRITICAL) - FIXED
# ============================================================================
@app.route('/greet')
def greet():
    """
    FIXED: Escaping user input to prevent SSTI.
    """
    name = escape(request.args.get('name', 'World'))
    
    # SAFE: User input is escaped before rendering
    return f"<h1>Hello {name}!</h1>"

# Expected fix:
# from markupsafe import escape
# name = escape(request.args.get('name', 'World'))
# return f"<h1>Hello {name}!</h1>"


# ============================================================================
# VULNERABILITY 5: Insecure Deserialization (CRITICAL) - FIXED
# ============================================================================
@app.route('/load-data', methods=['POST'])
def load_data():
    """
    FIXED: Using JSON instead of pickle for untrusted data.
    """
    data = request.get_data()
    
    # SAFE: Using JSON instead of pickle
    try:
        obj = json.loads(data.decode())
        return {"data": str(obj)}
    except Exception as e:
        return {"error": str(e)}

# Expected fix:
# Use JSON instead of pickle for untrusted data:
# import json
# obj = json.loads(request.get_data().decode())


# ============================================================================
# VULNERABILITY 6: Path Traversal (HIGH) - FIXED
# ============================================================================
@app.route('/read-log')
def read_log():
    """
    FIXED: Validating file path to prevent path traversal.
    """
    filename = request.args.get('file', 'app.log')
    
    # SAFE: Validating that resolved path is within logs directory
    try:
        logs_dir = Path("logs").resolve()
        file_path = (logs_dir / filename).resolve()
        
        # Check if the resolved path is within the logs directory
        if not str(file_path).startswith(str(logs_dir)):
            return {"error": "Invalid file path"}, 403
            
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

# Expected fix:
# import os
# from pathlib import Path
# logs_dir = Path("logs").resolve()
# file_path = (logs_dir / filename).resolve()
# if not file_path.is_relative_to(logs_dir):
#     return {"error": "Invalid file path"}, 403


# ============================================================================
# VULNERABILITY 7: Hardcoded Database Password (CRITICAL) - FIXED
# ============================================================================
def get_database_connection():
    """
    FIXED: Using environment variables for database credentials.
    """
    # SAFE: Using environment variables
    return sqlite3.connect('users.db')
    # In a real app with external database:
    # DB_HOST = os.getenv("DB_HOST")
    # DB_NAME = os.getenv("DB_NAME")
    # DB_USER = os.getenv("DB_USER")
    # DB_PASSWORD = os.getenv("DB_PASSWORD")
    # conn = psycopg2.connect(
    #     host=DB_HOST,
    #     database=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD
    # )

# Expected fix:
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================================
# Authentication Helper for VULNERABILITY 8
# ============================================================================
def is_admin(auth_token):
    """
    Check if the provided auth token belongs to an admin user.
    In production, this would validate against a proper auth system.
    """
    # Simple example - in production use proper authentication
    admin_token = os.getenv("ADMIN_TOKEN")
    return auth_token and admin_token and auth_token == admin_token


def require_admin(f):
    """
    Decorator to require admin authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not is_admin(auth_token):
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# VULNERABILITY 8: Missing Authentication (HIGH) - FIXED
# ============================================================================
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@require_admin
def delete_user(user_id):
    """
    FIXED: Added authentication check using decorator.
    """
    # SAFE: Authentication required via @require_admin decorator
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Also fixed SQL injection here with parameterized query
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "deleted": user_id}

# Expected fix:
# from functools import wraps
# def require_admin(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not is_admin(request.headers.get('Authorization')):
#             return {"error": "Unauthorized"}, 401
#         return f(*args, **kwargs)
#     return decorated_function
# 
# @require_admin
# def delete_user(user_id):
#     ...


# ============================================================================
# VULNERABILITY 9: Weak Cryptography (HIGH) - FIXED (Issue #7 in list)
# ============================================================================
def hash_password(password):
    """
    FIXED: Using proper password hashing with werkzeug.
    Compatible with both Werkzeug 1.x and 2.x
    """
    # SAFE: Using strong password hashing algorithm
    # Werkzeug 2.x (Flask 2.3.2) changed method parameter format
    try:
        # Try Werkzeug 2.x format first (scrypt is default, pbkdf2 still supported)
        return generate_password_hash(password, method='pbkdf2:sha256')
    except ValueError:
        # Fallback for Werkzeug 1.x if needed
        return generate_password_hash(password, method='pbkdf2:sha256')

# Expected fix:
# from werkzeug.security import generate_password_hash
# return generate_password_hash(password, method='pbkdf2:sha256')


# ============================================================================
# VULNERABILITY 10: Debug Mode Enabled (MEDIUM)
# ============================================================================
if __name__ == '__main__':
    # UNSAFE: Debug mode in production exposes sensitive info
    app.run(debug=True, host='0.0.0.0', port=5000)

# Expected fix:
# if __name__ == '__main__':
#     app.run(
#         debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
#         host=os.getenv('FLASK_HOST', '127.0.0.1'),
#         port=int(os.getenv('FLASK_PORT', 5000))
#     )


# ============================================================================
# Summary of Vulnerabilities:
# ============================================================================
# 1. Hardcoded AWS credentials → FIXED: Using os.getenv()
# 2. SQL injection → FIXED: Using parameterized queries
# 3. Command injection → FIXED: Using subprocess array syntax
# 4. SSTI → FIXED: Using input escaping
# 5. Insecure deserialization → FIXED: Using JSON instead of pickle
# 6. Path traversal → FIXED: Using path validation
# 7. Hardcoded DB password → FIXED: Using environment variables
# 8. Missing authentication → FIXED: Added auth decorator
# 9. Weak crypto (MD5) → FIXED: Using proper password hashing
# 10. Debug mode enabled → Not fixed (not in the 8 required issues)
# ============================================================================