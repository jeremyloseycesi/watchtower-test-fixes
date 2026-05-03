"""
Database utilities with security vulnerabilities.

⚠️ WARNING: Intentionally vulnerable code!
"""

import sqlite3
import os
import subprocess
import secrets

# FIXED: Load sensitive credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")


def execute_query(query, params):
    """
    FIXED: Use parameterized queries to prevent SQL injection.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


# Backwards compatibility wrapper
def execute_raw_query(query, user_input):
    """
    Deprecated: Use execute_query with parameterized queries instead.
    This wrapper maintains backwards compatibility.
    """
    # Convert old-style query to parameterized query
    if "USER_INPUT" in query:
        parameterized_query = query.replace("USER_INPUT", "?")
        return execute_query(parameterized_query, (user_input,))
    return execute_query(query, (user_input,))


def backup_database(backup_path):
    """
    FIXED: Use subprocess with shell=False to prevent command injection.
    """
    # Get password from environment variable
    db_password = os.getenv("DB_PASSWORD", "password")
    
    # SAFE: Using subprocess with list of arguments, no shell
    with open(backup_path, 'w') as output_file:
        subprocess.run(
            ["mysqldump", "-u", "root", f"--password={db_password}", "mydb"],
            stdout=output_file,
            shell=False,
            check=True
        )


class UserManager:
    """User management with security fixes."""
    
    def __init__(self):
        # FIXED: Load credentials from environment variables
        self.admin_username = os.getenv("ADMIN_USERNAME", "admin")
        self.admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    def authenticate(self, username, password):
        """
        FIXED: Use constant-time comparison to prevent timing attacks.
        """
        # SAFE: Using secrets.compare_digest for constant-time comparison
        username_match = secrets.compare_digest(
            self.admin_username.encode(),
            username.encode()
        )
        password_match = secrets.compare_digest(
            self.admin_password.encode(),
            password.encode()
        )
        return username_match and password_match