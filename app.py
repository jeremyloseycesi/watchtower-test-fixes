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
from flask import Flask, request, render_template_string
from markupsafe import escape
from werkzeug.security import generate_password_hash
from functools import wraps

app = Flask(__name__)

# ============================================================================
# VULNERABILITY 1: Hardcoded AWS Credentials (CRITICAL) - FIXED
# ============================================================================
# FIXED: Load from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


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
    
    # FIXED: Parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"user": {"id": result[0], "name": result[1], "email": result[2]}}
    return {"error": "User not found"}


# ============================================================================
# VULNERABILITY 3: Command Injection (CRITICAL) - FIXED
# ============================================================================
@app.route('/ping')
def ping_host():
    """
    FIXED: Using array syntax without shell=True to prevent command injection.
    """
    host = request.args.get('host', 'localhost')
    
    # FIXED: Using array syntax with shell=False
    result = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True
    )
    
    return {"output": result.stdout}


# ============================================================================
# VULNERABILITY 4: Server-Side Template Injection (CRITICAL) - FIXED
# ============================================================================
@app.route('/greet')
def greet():
    """
    FIXED: Escaping user input to prevent SSTI.
    """
    name = escape(request.args.get('name', 'World'))
    
    # FIXED: Using escaped input, not rendering as template
    return f"<h1>Hello {name}!</h1>"


# ============================================================================
# VULNERABILITY 5: Insecure Deserialization (CRITICAL) - FIXED
# ============================================================================
@app.route('/load-data', methods=['POST'])
def load_data():
    """
    FIXED: Using JSON instead of pickle for untrusted data.
    """
    data = request.get_data()
    
    # FIXED: Using JSON instead of pickle
    try:
        obj = json.loads(data.decode())
        return {"data": str(obj)}
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# VULNERABILITY 6: Path Traversal (HIGH) - FIXED
# ============================================================================
@app.route('/read-log')
def read_log():
    """
    FIXED: Validating file path to prevent path traversal.
    """
    filename = request.args.get('file', 'app.log')
    
    # FIXED: Path validation to prevent directory traversal
    try:
        logs_dir = Path("logs").resolve()
        file_path = (logs_dir / filename).resolve()
        
        # Ensure the resolved path is within logs directory
        if not str(file_path).startswith(str(logs_dir)):
            return {"error": "Invalid file path"}, 403
            
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# VULNERABILITY 7: Hardcoded Database Password (CRITICAL) - FIXED
# ============================================================================
def get_database_connection():
    """
    FIXED: Using environment variables for database credentials.
    """
    # FIXED: Load credentials from environment
    db_path = os.getenv("DB_PATH", "users.db")
    return sqlite3.connect(db_path)
    # In a real app with PostgreSQL, this would be:
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


# ============================================================================
# VULNERABILITY 8: Missing Authentication (HIGH) - FIXED
# ============================================================================
def require_admin(f):
    """
    Authentication decorator for admin endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        
        # Simple token check - in production, use proper JWT/session validation
        admin_token = os.getenv('ADMIN_TOKEN')
        if not auth_token or auth_token != f"Bearer {admin_token}":
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@require_admin
def delete_user(user_id):
    """
    FIXED: Added authentication check and parameterized query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # FIXED: Also using parameterized query here
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "deleted": user_id}


# ============================================================================
# VULNERABILITY 9: Weak Cryptography (HIGH) - FIXED
# ============================================================================
def hash_password(password):
    """
    FIXED: Using proper password hashing with werkzeug.
    """
    # FIXED: Using secure password hashing
    return generate_password_hash(password, method='pbkdf2:sha256')


# ============================================================================
# VULNERABILITY 10: Debug Mode Enabled (MEDIUM) - FIXED
# ============================================================================
if __name__ == '__main__':
    # FIXED: Environment-based configuration
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )


# ============================================================================
# Summary of Vulnerabilities - ALL FIXED:
# ============================================================================
# 1. Hardcoded AWS credentials → FIXED with os.getenv()
# 2. SQL injection → FIXED with parameterized queries
# 3. Command injection → FIXED with subprocess array syntax
# 4. SSTI → FIXED with input escaping
# 5. Insecure deserialization → FIXED with JSON instead of pickle
# 6. Path traversal → FIXED with path validation
# 7. Hardcoded DB password → FIXED with environment variables
# 8. Missing authentication → FIXED with auth decorator
# 9. Weak crypto (MD5) → FIXED with proper password hashing
# 10. Debug mode enabled → FIXED with environment-based config
# ============================================================================