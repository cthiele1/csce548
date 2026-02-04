"""
Running Shoe Model - Data Access Layer
Handles all CRUD operations for the running_shoes table
"""

from database import DatabaseConnection
from datetime import date


class RunningShoe:
    """Running Shoe model class"""
    
    def __init__(self, shoe_id=None, runner_id=None, brand=None, model=None,
                 purchase_date=None, total_miles=0, retired=False, 
                 notes=None, created_at=None):
        self.shoe_id = shoe_id
        self.runner_id = runner_id
        self.brand = brand
        self.model = model
        self.purchase_date = purchase_date
        self.total_miles = total_miles
        self.retired = retired
        self.notes = notes
        self.created_at = created_at
    
    def __str__(self):
        status = "Retired" if self.retired else "Active"
        return f"Shoe({self.shoe_id}, {self.brand} {self.model}, {self.total_miles} mi, {status})"
    
    @staticmethod
    def create(runner_id, brand, model, purchase_date, notes=None):
        """Create a new shoe (CREATE)"""
        query = """
            INSERT INTO running_shoes (runner_id, brand, model, purchase_date, notes)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (runner_id, brand, model, purchase_date, notes)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            shoe_id = cursor.lastrowid
            print(f"✓ Shoe created successfully with ID: {shoe_id}")
            return shoe_id
    
    @staticmethod
    def get_by_id(shoe_id):
        """Retrieve a shoe by ID (READ)"""
        query = "SELECT * FROM running_shoes WHERE shoe_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (shoe_id,))
            result = cursor.fetchone()
            
            if result:
                return RunningShoe(**result)
            return None
    
    @staticmethod
    def get_all():
        """Retrieve all shoes (READ)"""
        query = "SELECT * FROM running_shoes ORDER BY purchase_date DESC"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [RunningShoe(**row) for row in results]
    
    @staticmethod
    def get_by_runner(runner_id, active_only=False):
        """Get all shoes for a specific runner (READ)"""
        if active_only:
            query = """
                SELECT * FROM running_shoes 
                WHERE runner_id = %s AND retired = FALSE
                ORDER BY purchase_date DESC
            """
        else:
            query = """
                SELECT * FROM running_shoes 
                WHERE runner_id = %s 
                ORDER BY retired, purchase_date DESC
            """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            results = cursor.fetchall()
            return [RunningShoe(**row) for row in results]
    
    @staticmethod
    def update(shoe_id, **kwargs):
        """Update a shoe (UPDATE)"""
        valid_fields = ['brand', 'model', 'purchase_date', 'total_miles', 
                       'retired', 'notes']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        query = f"UPDATE running_shoes SET {set_clause} WHERE shoe_id = %s"
        values = tuple(updates.values()) + (shoe_id,)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Shoe {shoe_id} updated successfully")
                return True
            else:
                print(f"✗ Shoe {shoe_id} not found")
                return False
    
    @staticmethod
    def retire_shoe(shoe_id):
        """Retire a shoe (UPDATE)"""
        query = "UPDATE running_shoes SET retired = TRUE WHERE shoe_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (shoe_id,))
            if cursor.rowcount > 0:
                print(f"✓ Shoe {shoe_id} retired successfully")
                return True
            else:
                print(f"✗ Shoe {shoe_id} not found")
                return False
    
    @staticmethod
    def delete(shoe_id):
        """Delete a shoe (DELETE)"""
        query = "DELETE FROM running_shoes WHERE shoe_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (shoe_id,))
            if cursor.rowcount > 0:
                print(f"✓ Shoe {shoe_id} deleted successfully")
                return True
            else:
                print(f"✗ Shoe {shoe_id} not found")
                return False
    
    @staticmethod
    def get_shoes_needing_replacement(runner_id, mileage_threshold=400):
        """Get shoes that may need replacement (READ)"""
        query = """
            SELECT * FROM running_shoes 
            WHERE runner_id = %s 
            AND retired = FALSE 
            AND total_miles >= %s
            ORDER BY total_miles DESC
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id, mileage_threshold))
            results = cursor.fetchall()
            return [RunningShoe(**row) for row in results]
