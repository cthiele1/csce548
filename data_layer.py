"""
data_layer.py - Data Layer: CRUD Operations
Contains raw database operations for all 5 tables:
  - runners, running_shoes, routes, runs, training_goals
All methods open/close their own connection for simplicity.
"""

from data.db_connection import get_connection


# ─────────────────────────────────────────────
# RUNNERS
# ─────────────────────────────────────────────

def create_runner(first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO runners (first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def get_runner_by_id(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM runners WHERE runner_id = %s", (runner_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_runners():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM runners ORDER BY last_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_runner(runner_id, first_name, last_name, email, weight_lbs, height_inches):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE runners SET first_name=%s, last_name=%s, email=%s, weight_lbs=%s, height_inches=%s
             WHERE runner_id=%s"""
    cursor.execute(sql, (first_name, last_name, email, weight_lbs, height_inches, runner_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runners WHERE runner_id = %s", (runner_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


# ─────────────────────────────────────────────
# RUNS
# ─────────────────────────────────────────────

def create_run(runner_id, route_id, shoe_id, run_date, distance_miles, duration_minutes,
               pace_min_per_mile, average_heart_rate, calories_burned, weather,
               temperature_f, run_type, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO runs (runner_id, route_id, shoe_id, run_date, distance_miles,
             duration_minutes, pace_min_per_mile, average_heart_rate, calories_burned,
             weather, temperature_f, run_type, notes)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (runner_id, route_id, shoe_id, run_date, distance_miles,
                         duration_minutes, pace_min_per_mile, average_heart_rate,
                         calories_burned, weather, temperature_f, run_type, notes))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def get_run_by_id(run_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM runs WHERE run_id = %s", (run_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_runs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM runs ORDER BY run_date DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_runs_by_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM runs WHERE runner_id = %s ORDER BY run_date DESC", (runner_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_run(run_id, distance_miles, duration_minutes, pace_min_per_mile,
               average_heart_rate, calories_burned, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE runs SET distance_miles=%s, duration_minutes=%s, pace_min_per_mile=%s,
             average_heart_rate=%s, calories_burned=%s, notes=%s WHERE run_id=%s"""
    cursor.execute(sql, (distance_miles, duration_minutes, pace_min_per_mile,
                         average_heart_rate, calories_burned, notes, run_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_run(run_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runs WHERE run_id = %s", (run_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

def create_route(runner_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO routes (runner_id, route_name, distance_miles, elevation_gain_ft,
             surface_type, description, start_location)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (runner_id, route_name, distance_miles, elevation_gain_ft,
                         surface_type, description, start_location))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def get_route_by_id(route_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_routes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routes ORDER BY route_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_route(route_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE routes SET route_name=%s, distance_miles=%s, elevation_gain_ft=%s,
             surface_type=%s, description=%s, start_location=%s WHERE route_id=%s"""
    cursor.execute(sql, (route_name, distance_miles, elevation_gain_ft,
                         surface_type, description, start_location, route_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_route(route_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routes WHERE route_id = %s", (route_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


# ─────────────────────────────────────────────
# RUNNING SHOES
# ─────────────────────────────────────────────

def create_shoe(runner_id, brand, model, purchase_date, total_miles, retired, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO running_shoes (runner_id, brand, model, purchase_date, total_miles, retired, notes)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (runner_id, brand, model, purchase_date, total_miles, retired, notes))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def get_shoe_by_id(shoe_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM running_shoes WHERE shoe_id = %s", (shoe_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_shoes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM running_shoes ORDER BY brand")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_shoe(shoe_id, brand, model, total_miles, retired, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE running_shoes SET brand=%s, model=%s, total_miles=%s, retired=%s, notes=%s
             WHERE shoe_id=%s"""
    cursor.execute(sql, (brand, model, total_miles, retired, notes, shoe_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_shoe(shoe_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM running_shoes WHERE shoe_id = %s", (shoe_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


# ─────────────────────────────────────────────
# TRAINING GOALS
# ─────────────────────────────────────────────

def create_goal(runner_id, goal_type, target_value, current_value, target_date, status, description):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO training_goals (runner_id, goal_type, target_value, current_value,
             target_date, status, description)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (runner_id, goal_type, target_value, current_value,
                         target_date, status, description))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def get_goal_by_id(goal_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM training_goals WHERE goal_id = %s", (goal_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_goals():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM training_goals ORDER BY target_date")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_goals_by_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM training_goals WHERE runner_id = %s ORDER BY target_date", (runner_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_goal(goal_id, target_value, current_value, target_date, status, description):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE training_goals SET target_value=%s, current_value=%s, target_date=%s,
             status=%s, description=%s WHERE goal_id=%s"""
    cursor.execute(sql, (target_value, current_value, target_date, status, description, goal_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM training_goals WHERE goal_id = %s", (goal_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
