"""
Runner Model - Data Access Layer
Handles all CRUD operations for the runners table
"""

from database import DatabaseConnection
from datetime import date


class Runner:
    """Runner model class"""
    
    def __init__(self, runner_id=None, first_name=None, last_name=None, 
                 email=None, date_of_birth=None, gender=None, 
                 weight_lbs=None, height_inches=None, created_at=None):
        self.runner_id = runner_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.weight_lbs = weight_lbs
        self.height_inches = height_inches
        self.created_at = created_at
    
    def __str__(self):
        return f"Runner({self.runner_id}, {self.first_name} {self.last_name}, {self.email})"
    
    @staticmethod
    def create(first_name, last_name, email, date_of_birth=None, 
               gender='Other', weight_lbs=None, height_inches=None):
        """Create a new runner (CREATE)"""
        query = """
            INSERT INTO runners (first_name, last_name, email, date_of_birth, 
                               gender, weight_lbs, height_inches)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, email, date_of_birth, 
                 gender, weight_lbs, height_inches)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            runner_id = cursor.lastrowid
            print(f"✓ Runner created successfully with ID: {runner_id}")
            return runner_id
    
    @staticmethod
    def get_by_id(runner_id):
        """Retrieve a runner by ID (READ)"""
        query = "SELECT * FROM runners WHERE runner_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            result = cursor.fetchone()
            
            if result:
                return Runner(**result)
            return None
    
    @staticmethod
    def get_all():
        """Retrieve all runners (READ)"""
        query = "SELECT * FROM runners ORDER BY last_name, first_name"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [Runner(**row) for row in results]
    
    @staticmethod
    def search_by_name(name):
        """Search runners by name (READ)"""
        query = """
            SELECT * FROM runners 
            WHERE first_name LIKE %s OR last_name LIKE %s
            ORDER BY last_name, first_name
        """
        search_term = f"%{name}%"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (search_term, search_term))
            results = cursor.fetchall()
            return [Runner(**row) for row in results]
    
    @staticmethod
    def update(runner_id, **kwargs):
        """Update a runner's information (UPDATE)"""
        # Build dynamic update query based on provided fields
        valid_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 
                       'gender', 'weight_lbs', 'height_inches']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        query = f"UPDATE runners SET {set_clause} WHERE runner_id = %s"
        values = tuple(updates.values()) + (runner_id,)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Runner {runner_id} updated successfully")
                return True
            else:
                print(f"✗ Runner {runner_id} not found")
                return False
    
    @staticmethod
    def delete(runner_id):
        """Delete a runner (DELETE)"""
        query = "DELETE FROM runners WHERE runner_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            if cursor.rowcount > 0:
                print(f"✓ Runner {runner_id} deleted successfully")
                return True
            else:
                print(f"✗ Runner {runner_id} not found")
                return False
    
    @staticmethod
    def get_statistics(runner_id):
        """Get running statistics for a runner"""
        query = "SELECT * FROM runner_statistics WHERE runner_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            return cursor.fetchone()
