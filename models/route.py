"""
Route Model - Data Access Layer
Handles all CRUD operations for the routes table
"""

from database import DatabaseConnection


class Route:
    """Route model class"""
    
    def __init__(self, route_id=None, runner_id=None, route_name=None,
                 distance_miles=None, elevation_gain_ft=None, surface_type='Road',
                 description=None, start_location=None, created_at=None):
        self.route_id = route_id
        self.runner_id = runner_id
        self.route_name = route_name
        self.distance_miles = distance_miles
        self.elevation_gain_ft = elevation_gain_ft
        self.surface_type = surface_type
        self.description = description
        self.start_location = start_location
        self.created_at = created_at
    
    def __str__(self):
        return f"Route({self.route_id}, {self.route_name}, {self.distance_miles} mi)"
    
    @staticmethod
    def create(runner_id, route_name, distance_miles, elevation_gain_ft=0,
               surface_type='Road', description=None, start_location=None):
        """Create a new route (CREATE)"""
        query = """
            INSERT INTO routes (runner_id, route_name, distance_miles, 
                              elevation_gain_ft, surface_type, description, 
                              start_location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (runner_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            route_id = cursor.lastrowid
            print(f"✓ Route created successfully with ID: {route_id}")
            return route_id
    
    @staticmethod
    def get_by_id(route_id):
        """Retrieve a route by ID (READ)"""
        query = "SELECT * FROM routes WHERE route_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (route_id,))
            result = cursor.fetchone()
            
            if result:
                return Route(**result)
            return None
    
    @staticmethod
    def get_all():
        """Retrieve all routes (READ)"""
        query = "SELECT * FROM routes ORDER BY route_name"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [Route(**row) for row in results]
    
    @staticmethod
    def get_by_runner(runner_id):
        """Get all routes for a specific runner (READ)"""
        query = """
            SELECT * FROM routes 
            WHERE runner_id = %s 
            ORDER BY route_name
        """
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (runner_id,))
            results = cursor.fetchall()
            return [Route(**row) for row in results]
    
    @staticmethod
    def search_by_name(name):
        """Search routes by name (READ)"""
        query = """
            SELECT * FROM routes 
            WHERE route_name LIKE %s
            ORDER BY route_name
        """
        search_term = f"%{name}%"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (search_term,))
            results = cursor.fetchall()
            return [Route(**row) for row in results]
    
    @staticmethod
    def update(route_id, **kwargs):
        """Update a route (UPDATE)"""
        valid_fields = ['route_name', 'distance_miles', 'elevation_gain_ft',
                       'surface_type', 'description', 'start_location']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        query = f"UPDATE routes SET {set_clause} WHERE route_id = %s"
        values = tuple(updates.values()) + (route_id,)
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Route {route_id} updated successfully")
                return True
            else:
                print(f"✗ Route {route_id} not found")
                return False
    
    @staticmethod
    def delete(route_id):
        """Delete a route (DELETE)"""
        query = "DELETE FROM routes WHERE route_id = %s"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, (route_id,))
            if cursor.rowcount > 0:
                print(f"✓ Route {route_id} deleted successfully")
                return True
            else:
                print(f"✗ Route {route_id} not found")
                return False
