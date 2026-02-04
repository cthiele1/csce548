"""
Training Goal Model - Data Access Layer
Handles all CRUD operations for the training_goals table
"""

from database import DatabaseConnection
from datetime import date


class TrainingGoal:
    """Training Goal model class"""
    
    def __init__(self, goal_id=None, runner_id=None, goal_type=None,
                 target_value=None, current_value=0, target_date=None,
                 status='Active', description=None, created_at=None, 
                 updated_at=None):
        self.goal_id = goal_id
        self.runner_id = runner_id
        self.goal_type = goal_type
        self.target_value = target_value
        self.current_value = current_value
        self.target_date = target_date
        self.status = status
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        return f"Goal({self.goal_id}, {self.goal_type}, {self.current_value}/{self.target_value}, {self.status})"
    
    @staticmethod
    def create(runner_id, goal_type, target_value, target_date=None, 
               description=None):
        """Create a new training goal (CREATE)"""
        query = """
            INSERT INTO training_goals (runner_id, goal_type, target_value, 
                                       target_date, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (runner_id, goal_type, target_value, target_date, description)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            goal_id = cursor.lastrowid
            print(f"✓ Training goal created successfully with ID: {goal_id}")
            return goal_id
    
    @staticmethod
    def get_by_id(goal_id):
        """Retrieve a goal by ID (READ)"""
        query = "SELECT * FROM training_goals WHERE goal_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (goal_id,))
            result = cursor.fetchone()
            
            if result:
                return TrainingGoal(**result)
            return None
    
    @staticmethod
    def get_all():
        """Retrieve all goals (READ)"""
        query = "SELECT * FROM training_goals ORDER BY status, target_date"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [TrainingGoal(**row) for row in results]
    
    @staticmethod
    def get_by_runner(runner_id, active_only=False):
        """Get all goals for a specific runner (READ)"""
        if active_only:
            query = """
                SELECT * FROM training_goals 
                WHERE runner_id = %s AND status = 'Active'
                ORDER BY target_date
            """
        else:
            query = """
                SELECT * FROM training_goals 
                WHERE runner_id = %s 
                ORDER BY status, target_date
            """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            results = cursor.fetchall()
            return [TrainingGoal(**row) for row in results]
    
    @staticmethod
    def update(goal_id, **kwargs):
        """Update a goal (UPDATE)"""
        valid_fields = ['goal_type', 'target_value', 'current_value', 
                       'target_date', 'status', 'description']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        query = f"UPDATE training_goals SET {set_clause} WHERE goal_id = %s"
        values = tuple(updates.values()) + (goal_id,)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Goal {goal_id} updated successfully")
                return True
            else:
                print(f"✗ Goal {goal_id} not found")
                return False
    
    @staticmethod
    def update_progress(goal_id, current_value):
        """Update the current progress of a goal (UPDATE)"""
        query = """
            UPDATE training_goals 
            SET current_value = %s,
                status = CASE 
                    WHEN current_value >= target_value THEN 'Completed'
                    ELSE status
                END
            WHERE goal_id = %s
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (current_value, goal_id))
            if cursor.rowcount > 0:
                print(f"✓ Goal {goal_id} progress updated to {current_value}")
                return True
            else:
                print(f"✗ Goal {goal_id} not found")
                return False
    
    @staticmethod
    def complete_goal(goal_id):
        """Mark a goal as completed (UPDATE)"""
        query = "UPDATE training_goals SET status = 'Completed' WHERE goal_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (goal_id,))
            if cursor.rowcount > 0:
                print(f"✓ Goal {goal_id} marked as completed")
                return True
            else:
                print(f"✗ Goal {goal_id} not found")
                return False
    
    @staticmethod
    def abandon_goal(goal_id):
        """Mark a goal as abandoned (UPDATE)"""
        query = "UPDATE training_goals SET status = 'Abandoned' WHERE goal_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (goal_id,))
            if cursor.rowcount > 0:
                print(f"✓ Goal {goal_id} marked as abandoned")
                return True
            else:
                print(f"✗ Goal {goal_id} not found")
                return False
    
    @staticmethod
    def delete(goal_id):
        """Delete a goal (DELETE)"""
        query = "DELETE FROM training_goals WHERE goal_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (goal_id,))
            if cursor.rowcount > 0:
                print(f"✓ Goal {goal_id} deleted successfully")
                return True
            else:
                print(f"✗ Goal {goal_id} not found")
                return False
