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
import pickle
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ============================================================================
# VULNERABILITY 1: Hardcoded AWS Credentials (CRITICAL)
# ============================================================================
# These should be environment variables!
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"

# Expected fix:
# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


# ============================================================================
# VULNERABILITY 2: SQL Injection (CRITICAL)
# ============================================================================
@app.route('/user/<user_id>')
def get_user(user_id):
    """
    VULNERABLE: Direct string concatenation in SQL query.
    An attacker can inject: 1 OR 1=1; DROP TABLE users;--
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # UNSAFE: User input directly in query string
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"user": {"id": result[0], "name": result[1], "email": result[2]}}
    return {"error": "User not found"}

# Expected fix:
# query = "SELECT * FROM users WHERE id = ?"
# cursor.execute(query, (user_id,))


# ============================================================================
# VULNERABILITY 3: Command Injection (CRITICAL)
# ============================================================================
@app.route('/ping')
def ping_host():
    """
    VULNERABLE: User input passed to shell command.
    An attacker can inject: 8.8.8.8; rm -rf /
    """
    host = request.args.get('host', 'localhost')
    
    # UNSAFE: Using shell=True with user input
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
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
# VULNERABILITY 4: Server-Side Template Injection (CRITICAL)
# ============================================================================
@app.route('/greet')
def greet():
    """
    VULNERABLE: User input directly in template.
    An attacker can inject: {{config.__class__.__init__.__globals__['os'].popen('ls').read()}}
    """
    name = request.args.get('name', 'World')
    
    # UNSAFE: Rendering user input as template
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

# Expected fix:
# from markupsafe import escape
# name = escape(request.args.get('name', 'World'))
# return f"<h1>Hello {name}!</h1>"


# ============================================================================
# VULNERABILITY 5: Insecure Deserialization (CRITICAL)
# ============================================================================
@app.route('/load-data', methods=['POST'])
def load_data():
    """
    VULNERABLE: Unpickling untrusted data.
    An attacker can execute arbitrary code via malicious pickle payload.
    """
    data = request.get_data()
    
    # UNSAFE: pickle.loads on untrusted data
    try:
        obj = pickle.loads(data)
        return {"data": str(obj)}
    except Exception as e:
        return {"error": str(e)}

# Expected fix:
# Use JSON instead of pickle for untrusted data:
# import json
# obj = json.loads(request.get_data().decode())


# ============================================================================
# VULNERABILITY 6: Path Traversal (HIGH)
# ============================================================================
@app.route('/read-log')
def read_log():
    """
    VULNERABLE: No path validation.
    An attacker can read: ../../../../etc/passwd
    """
    filename = request.args.get('file', 'app.log')
    
    # UNSAFE: No validation of file path
    try:
        with open(f"logs/{filename}", 'r') as f:
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
# VULNERABILITY 7: Hardcoded Database Password (CRITICAL)
# ============================================================================
def get_database_connection():
    """
    VULNERABLE: Database credentials hardcoded.
    """
    # UNSAFE: Hardcoded credentials
    return sqlite3.connect('users.db')
    # In a real app, this would be:
    # conn = psycopg2.connect(
    #     host="prod-db.company.com",
    #     database="users",
    #     user="admin",
    #     password="SuperSecret123!"  # HARDCODED!
    # )

# Expected fix:
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================================
# VULNERABILITY 8: Missing Authentication (HIGH)
# ============================================================================
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    """
    VULNERABLE: No authentication check!
    Anyone can delete any user.
    """
    # UNSAFE: No auth check
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
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
# VULNERABILITY 9: Weak Cryptography (HIGH)
# ============================================================================
def hash_password(password):
    """
    VULNERABLE: Using MD5 for passwords!
    """
    import hashlib
    
    # UNSAFE: MD5 is broken and fast (susceptible to rainbow tables)
    return hashlib.md5(password.encode()).hexdigest()

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
# 1. Hardcoded AWS credentials → Need os.getenv()
# 2. SQL injection → Need parameterized queries
# 3. Command injection → Need subprocess array syntax
# 4. SSTI → Need input escaping
# 5. Insecure deserialization → Need JSON instead of pickle
# 6. Path traversal → Need path validation
# 7. Hardcoded DB password → Need environment variables
# 8. Missing authentication → Need auth decorator
# 9. Weak crypto (MD5) → Need proper password hashing
# 10. Debug mode enabled → Need environment-based config
# ============================================================================