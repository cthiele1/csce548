"""
Run Model - Data Access Layer
Handles all CRUD operations for the runs table
"""

from database import DatabaseConnection
from datetime import date, datetime


class Run:
    """Run model class"""
    
    def __init__(self, run_id=None, runner_id=None, route_id=None, shoe_id=None,
                 run_date=None, distance_miles=None, duration_minutes=None,
                 pace_min_per_mile=None, average_heart_rate=None, 
                 calories_burned=None, weather=None, temperature_f=None,
                 run_type='Easy', notes=None, created_at=None):
        self.run_id = run_id
        self.runner_id = runner_id
        self.route_id = route_id
        self.shoe_id = shoe_id
        self.run_date = run_date
        self.distance_miles = distance_miles
        self.duration_minutes = duration_minutes
        self.pace_min_per_mile = pace_min_per_mile
        self.average_heart_rate = average_heart_rate
        self.calories_burned = calories_burned
        self.weather = weather
        self.temperature_f = temperature_f
        self.run_type = run_type
        self.notes = notes
        self.created_at = created_at
    
    def __str__(self):
        return f"Run({self.run_id}, {self.run_date}, {self.distance_miles} mi, {self.pace_min_per_mile} min/mi)"
    
    @staticmethod
    def create(runner_id, run_date, distance_miles, duration_minutes,
               route_id=None, shoe_id=None, average_heart_rate=None,
               calories_burned=None, weather=None, temperature_f=None,
               run_type='Easy', notes=None):
        """Create a new run (CREATE)"""
        query = """
            INSERT INTO runs (runner_id, route_id, shoe_id, run_date, 
                            distance_miles, duration_minutes, average_heart_rate,
                            calories_burned, weather, temperature_f, run_type, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (runner_id, route_id, shoe_id, run_date, distance_miles,
                 duration_minutes, average_heart_rate, calories_burned,
                 weather, temperature_f, run_type, notes)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            run_id = cursor.lastrowid
            
            # Update shoe mileage if shoe_id is provided
            if shoe_id:
                update_query = """
                    UPDATE running_shoes 
                    SET total_miles = total_miles + %s 
                    WHERE shoe_id = %s
                """
                cursor.execute(update_query, (distance_miles, shoe_id))
            
            print(f"✓ Run created successfully with ID: {run_id}")
            return run_id
    
    @staticmethod
    def get_by_id(run_id):
        """Retrieve a run by ID (READ)"""
        query = "SELECT * FROM runs WHERE run_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (run_id,))
            result = cursor.fetchone()
            
            if result:
                return Run(**result)
            return None
    
    @staticmethod
    def get_all(limit=100):
        """Retrieve all runs (READ)"""
        query = "SELECT * FROM runs ORDER BY run_date DESC, created_at DESC LIMIT %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            return [Run(**row) for row in results]
    
    @staticmethod
    def get_by_runner(runner_id, limit=100):
        """Get all runs for a specific runner (READ)"""
        query = """
            SELECT * FROM runs 
            WHERE runner_id = %s 
            ORDER BY run_date DESC, created_at DESC
            LIMIT %s
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id, limit))
            results = cursor.fetchall()
            return [Run(**row) for row in results]
    
    @staticmethod
    def get_by_date_range(runner_id, start_date, end_date):
        """Get runs within a date range (READ)"""
        query = """
            SELECT * FROM runs 
            WHERE runner_id = %s AND run_date BETWEEN %s AND %s
            ORDER BY run_date DESC
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id, start_date, end_date))
            results = cursor.fetchall()
            return [Run(**row) for row in results]
    
    @staticmethod
    def update(run_id, **kwargs):
        """Update a run (UPDATE)"""
        valid_fields = ['route_id', 'shoe_id', 'run_date', 'distance_miles',
                       'duration_minutes', 'average_heart_rate', 'calories_burned',
                       'weather', 'temperature_f', 'run_type', 'notes']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        query = f"UPDATE runs SET {set_clause} WHERE run_id = %s"
        values = tuple(updates.values()) + (run_id,)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Run {run_id} updated successfully")
                return True
            else:
                print(f"✗ Run {run_id} not found")
                return False
    
    @staticmethod
    def delete(run_id):
        """Delete a run (DELETE)"""
        query = "DELETE FROM runs WHERE run_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (run_id,))
            if cursor.rowcount > 0:
                print(f"✓ Run {run_id} deleted successfully")
                return True
            else:
                print(f"✗ Run {run_id} not found")
                return False
    
    @staticmethod
    def get_recent_runs(limit=20):
        """Get recent runs across all runners"""
        query = "SELECT * FROM recent_runs LIMIT %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (limit,))
            return cursor.fetchall()
    
    @staticmethod
    def get_summary_stats(runner_id):
        """Get summary statistics for a runner's runs"""
        query = """
            SELECT 
                COUNT(*) as total_runs,
                SUM(distance_miles) as total_distance,
                AVG(distance_miles) as avg_distance,
                AVG(pace_min_per_mile) as avg_pace,
                MIN(pace_min_per_mile) as best_pace,
                MAX(distance_miles) as longest_run
            FROM runs
            WHERE runner_id = %s
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            return cursor.fetchone()
