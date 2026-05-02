"""
Configuration file with hardcoded secrets.

⚠️ WARNING: Multiple security vulnerabilities!
"""

# VULNERABILITY 8: Hardcoded Database Credentials
DATABASE_CONFIG = {
    'host': 'production-db.example.com',
    'port': 5432,
    'user': 'admin',
    'password': 'P@ssw0rd123',  # UNSAFE: Hardcoded password
    'database': 'users_prod'
}

# VULNERABILITY 9: Hardcoded API Keys
API_KEYS = {
    'stripe_secret': 'sk_test_FakeStripeKeyForTesting1234567890',
    'stripe_public': 'pk_test_FakeStripeKeyForTesting1234567890',
    'sendgrid': 'SG.FakeSendGridKey.FakeForTestingOnly',
    'twilio_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'twilio_token': 'fake_twilio_token_for_testing_12345'
}

# VULNERABILITY 10: Hardcoded JWT Secret
JWT_SECRET = 'my-super-secret-key-123'

# VULNERABILITY 11: Weak Encryption Key
ENCRYPTION_KEY = b'12345'  # UNSAFE: Weak key

# VULNERABILITY 12: Hardcoded GitHub Token
GITHUB_TOKEN = 'ghp_1234567890abcdefghijklmnopqrstuvwx'

# Proper configuration should look like:
# DATABASE_CONFIG = {
#     'host': os.getenv('DB_HOST'),
#     'port': int(os.getenv('DB_PORT', 5432)),
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'database': os.getenv('DB_NAME')
# }
