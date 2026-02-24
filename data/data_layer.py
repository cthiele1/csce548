"""
data_layer.py - Data Layer: CRUD Operations
Contains raw database operations for all 5 tables:
  - runners, running_shoes, routes, runs, training_goals
All methods open/close their own connection for simplicity.
"""

import time
import mysql.connector
from data.db_connection import get_connection


# helper: close cursor/conn safely
def _close(cursor, conn):
    try:
        if cursor:
            cursor.close()
    except Exception:
        pass
    try:
        if conn:
            conn.close()
    except Exception:
        pass


# ─────────────────────────────────────────────
# RUNNERS
# ─────────────────────────────────────────────

def create_runner(first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches,
                  retries=3, backoff=0.2):
    """
    Attempt to insert a runner. Retries on transient lock wait timeouts (errno 1205).
    Returns new runner_id.
    """
    attempt = 0
    while True:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO runners (first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches))
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except mysql.connector.Error as e:
            conn.rollback()
            # transient lock wait timeout
            if getattr(e, "errno", None) == 1205 and attempt < (retries - 1):
                attempt += 1
                time.sleep(backoff * attempt)
                _close(cursor, conn)
                continue
            raise
        finally:
            _close(cursor, conn)


def get_runner_by_id(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM runners WHERE runner_id = %s", (runner_id,))
        row = cursor.fetchone()
        return row
    finally:
        _close(cursor, conn)


def get_all_runners():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM runners ORDER BY last_name")
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def update_runner(runner_id, first_name, last_name, email, weight_lbs, height_inches):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """UPDATE runners SET first_name=%s, last_name=%s, email=%s, weight_lbs=%s, height_inches=%s
                 WHERE runner_id=%s"""
        cursor.execute(sql, (first_name, last_name, email, weight_lbs, height_inches, runner_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def delete_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM runners WHERE runner_id = %s", (runner_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


# ─────────────────────────────────────────────
# RUNS
# ─────────────────────────────────────────────

def create_run(runner_id, route_id, shoe_id, run_date, distance_miles, duration_minutes,
               pace_min_per_mile, average_heart_rate, calories_burned, weather,
               temperature_f, run_type, notes):
    """
    pace_min_per_mile is a generated column in the DB — do NOT include it in INSERT.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO runs (runner_id, route_id, shoe_id, run_date, distance_miles,
                 duration_minutes, average_heart_rate, calories_burned,
                 weather, temperature_f, run_type, notes)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (runner_id, route_id, shoe_id, run_date, distance_miles,
                             duration_minutes, average_heart_rate,
                             calories_burned, weather, temperature_f, run_type, notes))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def get_run_by_id(run_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM runs WHERE run_id = %s", (run_id,))
        row = cursor.fetchone()
        return row
    finally:
        _close(cursor, conn)


def get_all_runs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM runs ORDER BY run_date DESC")
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def get_runs_by_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM runs WHERE runner_id = %s ORDER BY run_date DESC", (runner_id,))
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def update_run(run_id, distance_miles, duration_minutes, pace_min_per_mile,
               average_heart_rate, calories_burned, notes):
    """
    pace_min_per_mile is a generated column - omit it from UPDATE
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """UPDATE runs SET distance_miles=%s, duration_minutes=%s,
                 average_heart_rate=%s, calories_burned=%s, notes=%s WHERE run_id=%s"""
        cursor.execute(sql, (distance_miles, duration_minutes,
                             average_heart_rate, calories_burned, notes, run_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def delete_run(run_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM runs WHERE run_id = %s", (run_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

def create_route(runner_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location):
    """
    Defensive truncation of surface_type to 255 chars to avoid 'Data truncated' errors
    from overly-long input strings.
    """
    if surface_type is not None:
        try:
            surface_type = surface_type.strip()
        except Exception:
            # non-string input: coerce to string
            surface_type = str(surface_type)
        if len(surface_type) > 255:
            surface_type = surface_type[:255]

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO routes (runner_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (runner_id, route_name, distance_miles, elevation_gain_ft,
                             surface_type, description, start_location))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def get_route_by_id(route_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
        row = cursor.fetchone()
        return row
    finally:
        _close(cursor, conn)


def get_all_routes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM routes ORDER BY route_name")
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def update_route(route_id, route_name, distance_miles, elevation_gain_ft,
                 surface_type, description, start_location):
    if surface_type is not None:
        try:
            surface_type = surface_type.strip()
        except Exception:
            surface_type = str(surface_type)
        if len(surface_type) > 255:
            surface_type = surface_type[:255]

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """UPDATE routes SET route_name=%s, distance_miles=%s, elevation_gain_ft=%s,
                 surface_type=%s, description=%s, start_location=%s WHERE route_id=%s"""
        cursor.execute(sql, (route_name, distance_miles, elevation_gain_ft,
                             surface_type, description, start_location, route_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def delete_route(route_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM routes WHERE route_id = %s", (route_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


# ─────────────────────────────────────────────
# RUNNING SHOES
# ─────────────────────────────────────────────

def create_shoe(runner_id, brand, model, purchase_date, total_miles, retired, notes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO running_shoes (runner_id, brand, model, purchase_date, total_miles, retired, notes)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (runner_id, brand, model, purchase_date, total_miles, retired, notes))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def get_shoe_by_id(shoe_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM running_shoes WHERE shoe_id = %s", (shoe_id,))
        row = cursor.fetchone()
        return row
    finally:
        _close(cursor, conn)


def get_all_shoes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM running_shoes ORDER BY brand")
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def update_shoe(shoe_id, brand, model, total_miles, retired, notes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """UPDATE running_shoes SET brand=%s, model=%s, total_miles=%s, retired=%s, notes=%s
                 WHERE shoe_id=%s"""
        cursor.execute(sql, (brand, model, total_miles, retired, notes, shoe_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def delete_shoe(shoe_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM running_shoes WHERE shoe_id = %s", (shoe_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


# ─────────────────────────────────────────────
# TRAINING GOALS
# ─────────────────────────────────────────────

def create_goal(runner_id, goal_type, target_value, current_value, target_date, status, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO training_goals (runner_id, goal_type, target_value, current_value,
                 target_date, status, description)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (runner_id, goal_type, target_value, current_value,
                             target_date, status, description))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def get_goal_by_id(goal_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM training_goals WHERE goal_id = %s", (goal_id,))
        row = cursor.fetchone()
        return row
    finally:
        _close(cursor, conn)


def get_all_goals():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM training_goals ORDER BY target_date")
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def get_goals_by_runner(runner_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM training_goals WHERE runner_id = %s ORDER BY target_date", (runner_id,))
        rows = cursor.fetchall()
        return rows
    finally:
        _close(cursor, conn)


def update_goal(goal_id, target_value, current_value, target_date, status, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """UPDATE training_goals SET target_value=%s, current_value=%s, target_date=%s,
                 status=%s, description=%s WHERE goal_id=%s"""
        cursor.execute(sql, (target_value, current_value, target_date, status, description, goal_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)


def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM training_goals WHERE goal_id = %s", (goal_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        _close(cursor, conn)