"""
Database utilities with security vulnerabilities.

⚠️ WARNING: Intentionally vulnerable code!
"""

import sqlite3
import os

# FIXED: Load sensitive credentials from environment variables
# Provide defaults for testing/development (should be overridden in production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
API_KEY = os.getenv("API_KEY", "default-api-key-for-testing")
JWT_SECRET = os.getenv("JWT_SECRET", "default-jwt-secret-for-testing")

# Expected fix:
# DATABASE_URL = os.getenv("DATABASE_URL")
# API_KEY = os.getenv("API_KEY")
# JWT_SECRET = os.getenv("JWT_SECRET")


def execute_raw_query(query, user_input):
    """
    VULNERABILITY: String concatenation in SQL queries.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # UNSAFE: Direct string interpolation
    full_query = query.replace("USER_INPUT", user_input)
    cursor.execute(full_query)
    
    results = cursor.fetchall()
    conn.close()
    return results

# Expected fix:
# def execute_query(query, params):
#     conn = sqlite3.connect('app.db')
#     cursor = conn.cursor()
#     cursor.execute(query, params)
#     results = cursor.fetchall()
#     conn.close()
#     return results


def backup_database(backup_path):
    """
    VULNERABILITY: Command injection via os.system.
    """
    import os
    
    # UNSAFE: User input in os.system
    os.system(f"mysqldump -u root -p'password' mydb > {backup_path}")

# Expected fix:
# import subprocess
# subprocess.run(
#     ["mysqldump", "-u", "root", f"--password={db_password}", "mydb"],
#     stdout=open(backup_path, 'w'),
#     shell=False
# )


class UserManager:
    """User management with security flaws."""
    
    def __init__(self):
        # VULNERABILITY: Hardcoded admin credentials
        self.admin_username = "admin"
        self.admin_password = "admin123"  # NEVER do this!
    
    def authenticate(self, username, password):
        """
        VULNERABILITY: Timing attack possible.
        """
        # UNSAFE: String comparison (timing attack)
        if username == self.admin_username and password == self.admin_password:
            return True
        return False
    
    # Expected fix:
    # import secrets
    # def authenticate(self, username, password):
    #     stored_password = get_password_from_db(username)
    #     return secrets.compare_digest(
    #         stored_password.encode(),
    #         password.encode()
    #     )