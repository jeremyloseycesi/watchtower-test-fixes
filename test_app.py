"""
Simple Flask application with security fixes applied.
"""

import os
import sqlite3
import subprocess

# Use environment variables for secrets (security fix for hardcoded credentials)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', '')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')


def get_user(user_id):
    """
    Get user from database using parameterized query.
    Security fix: Using parameterized query instead of f-string to prevent SQL injection.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Fixed: Using parameterized query with ? placeholder
    # OLD (vulnerable): cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result


def run_command(filename):
    """
    Run a command safely without shell injection.
    Security fix: Using shell=False and list arguments to prevent command injection.
    """
    # Fixed: Using shell=False and passing command as list
    # OLD (vulnerable): subprocess.run(f"cat {filename}", shell=True)
    result = subprocess.run(['cat', filename], shell=False, capture_output=True, text=True)
    return result.stdout


def create_app():
    """Create and configure the Flask application"""
    try:
        from flask import Flask
        app = Flask(__name__)
        app.config['SECRET_KEY'] = SECRET_KEY
        
        @app.route('/')
        def index():
            return "Hello, World!"
        
        return app
    except ImportError:
        # Flask not installed, return None
        return None


# For backwards compatibility
app = create_app()

if __name__ == '__main__':
    if app:
        app.run(debug=False)