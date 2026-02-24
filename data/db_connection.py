"""
db_connection.py - Data Layer: Database Connection
Provides a reusable MySQL connection using environment variables.
Environment variables are set in Railway's dashboard under Variables.
"""

import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Connection parameters are read from environment variables set in Railway.
    """
    try:
        connection = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT", 3306)),
    database=os.environ.get("DB_NAME", "running_tracker"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "connor")
)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise
