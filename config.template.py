"""
Database configuration template for Running Tracker
Copy this to config.py and update with your credentials
"""

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'connor',   # Updated
    'database': 'running_tracker',
    'raise_on_warnings': True
}


# After copying this file to config.py:
# 1. Update the password field with your MySQL password
# 2. Adjust host/user if using different credentials
# 3. Do NOT commit config.py to git (it's in .gitignore)
