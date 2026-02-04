"""
Database connection utility for Running Tracker
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.cursor
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


def get_connection():
    """Get a database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
