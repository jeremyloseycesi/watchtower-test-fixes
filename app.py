#!/usr/bin/env python3
"""
Intentionally vulnerable Flask application for testing Watchtower.

⚠️ WARNING: Contains multiple security vulnerabilities!
DO NOT USE IN PRODUCTION!
"""

import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded AWS Credentials (HIGH severity)
# Should be: AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# VULNERABILITY 2: Hardcoded Database Password (HIGH severity)
DATABASE_PASSWORD = "super_secret_password_123"


# VULNERABILITY 3: SQL Injection (HIGH severity)
@app.route('/user/<user_id>')
def get_user(user_id):
    """Vulnerable to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # UNSAFE: User input directly in query
    # An attacker could pass: 1 OR 1=1; DROP TABLE users;--
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return {"user": result}


# VULNERABILITY 4: Command Injection (HIGH severity)
@app.route('/list-files')
def list_files():
    """Vulnerable to command injection"""
    directory = request.args.get('dir', '.')
    
    # UNSAFE: User input in shell command
    # An attacker could pass: .; rm -rf /
    result = subprocess.run(
        f"ls -la {directory}",
        shell=True,
        capture_output=True,
        text=True
    )
    
    return {"output": result.stdout}


# VULNERABILITY 5: Path Traversal (MEDIUM severity)
@app.route('/read-file')
def read_file():
    """Vulnerable to path traversal"""
    filename = request.args.get('file', 'default.txt')
    
    # UNSAFE: No path validation
    # An attacker could pass: ../../../../etc/passwd
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


# VULNERABILITY 6: Unsafe YAML Loading (HIGH severity)
@app.route('/parse-config', methods=['POST'])
def parse_config():
    """Vulnerable to arbitrary code execution via YAML"""
    import yaml
    
    config_data = request.get_data()
    
    # UNSAFE: yaml.load allows arbitrary Python code execution
    # Should use: yaml.safe_load(config_data)
    config = yaml.load(config_data)
    
    return {"config": str(config)}


# VULNERABILITY 7: Debug Mode in Production
if __name__ == '__main__':
    # UNSAFE: Debug mode exposes sensitive information
    app.run(debug=True, host='0.0.0.0', port=5000)
