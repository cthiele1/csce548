"""
business_layer.py - Business Layer
Sits between the service layer and data layer. Enforces business rules,
validates inputs, and exposes clean methods to the service layer.
All business logic (e.g., shoe mileage warnings, goal progress) lives here.
"""

import data.data_layer as dal
from datetime import date


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _error(msg):
    """Returns a standardized error dict."""
    return {"success": False, "error": msg}


def _ok(data=None):
    """Returns a standardized success dict."""
    return {"success": True, "data": data}


# ─────────────────────────────────────────────
# RUNNERS BUSINESS
# ─────────────────────────────────────────────

def add_runner(first_name, last_name, email, date_of_birth, gender,
               weight_lbs=None, height_inches=None):
    """
    Business rule: first name, last name, and email are required.
    Business rule: email must contain '@'.
    Business rule: weight and height must be positive if provided.
    """
    if not first_name or not last_name:
        return _error("First name and last name are required.")
    if not email or "@" not in email:
        return _error("A valid email address is required.")
    if weight_lbs is not None and weight_lbs <= 0:
        return _error("Weight must be a positive number.")
    if height_inches is not None and height_inches <= 0:
        return _error("Height must be a positive number.")

    new_id = dal.create_runner(first_name, last_name, email, date_of_birth,
                               gender, weight_lbs, height_inches)
    return _ok({"runner_id": new_id})


def fetch_runner(runner_id):
    """Retrieves a single runner. Returns error if not found."""
    runner = dal.get_runner_by_id(runner_id)
    if not runner:
        return _error(f"Runner with ID {runner_id} not found.")
    return _ok(runner)


def fetch_all_runners():
    """Returns all runners."""
    runners = dal.get_all_runners()
    return _ok(runners)


def modify_runner(runner_id, first_name, last_name, email, weight_lbs=None, height_inches=None):
    """
    Business rule: runner must exist before updating.
    Business rule: email must be valid.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    if not email or "@" not in email:
        return _error("A valid email address is required.")

    affected = dal.update_runner(runner_id, first_name, last_name, email, weight_lbs, height_inches)
    return _ok({"rows_affected": affected})


def remove_runner(runner_id):
    """
    Business rule: runner must exist before deleting.
    Note: Deleting a runner will cascade to their runs, shoes, routes, and goals.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    affected = dal.delete_runner(runner_id)
    return _ok({"rows_affected": affected})


# ─────────────────────────────────────────────
# RUNS BUSINESS
# ─────────────────────────────────────────────

def log_run(runner_id, run_date, distance_miles, duration_minutes, run_type,
            route_id=None, shoe_id=None, pace_min_per_mile=None,
            average_heart_rate=None, calories_burned=None,
            weather=None, temperature_f=None, notes=None):
    """
    Business rule: runner must exist.
    Business rule: distance and duration must be positive.
    Business rule: auto-calculate pace if not provided.
    Business rule: warn if heart rate exceeds 220 bpm.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    if distance_miles <= 0:
        return _error("Distance must be greater than zero.")
    if duration_minutes <= 0:
        return _error("Duration must be greater than zero.")
    if average_heart_rate and average_heart_rate > 220:
        return _error("Heart rate exceeds physiological maximum of 220 bpm.")

    # Auto-calculate pace if not provided
    if pace_min_per_mile is None:
        pace_min_per_mile = round(duration_minutes / distance_miles, 2)

    new_id = dal.create_run(runner_id, route_id, shoe_id, run_date, distance_miles,
                            duration_minutes, pace_min_per_mile, average_heart_rate,
                            calories_burned, weather, temperature_f, run_type, notes)
    return _ok({"run_id": new_id})


def fetch_run(run_id):
    run = dal.get_run_by_id(run_id)
    if not run:
        return _error(f"Run with ID {run_id} not found.")
    return _ok(run)


def fetch_all_runs():
    return _ok(dal.get_all_runs())


def fetch_runs_for_runner(runner_id):
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    return _ok(dal.get_runs_by_runner(runner_id))


def modify_run(run_id, distance_miles, duration_minutes, pace_min_per_mile=None,
               average_heart_rate=None, calories_burned=None, notes=None):
    if not dal.get_run_by_id(run_id):
        return _error(f"Run with ID {run_id} not found.")
    if distance_miles <= 0 or duration_minutes <= 0:
        return _error("Distance and duration must be positive.")
    if pace_min_per_mile is None:
        pace_min_per_mile = round(duration_minutes / distance_miles, 2)

    affected = dal.update_run(run_id, distance_miles, duration_minutes, pace_min_per_mile,
                              average_heart_rate, calories_burned, notes)
    return _ok({"rows_affected": affected})


def remove_run(run_id):
    if not dal.get_run_by_id(run_id):
        return _error(f"Run with ID {run_id} not found.")
    affected = dal.delete_run(run_id)
    return _ok({"rows_affected": affected})


# ─────────────────────────────────────────────
# ROUTES BUSINESS
# ─────────────────────────────────────────────

def add_route(runner_id, route_name, distance_miles, elevation_gain_ft=0,
              surface_type=None, description=None, start_location=None):
    """
    Business rule: route name and distance are required.
    Business rule: runner must exist.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    if not route_name:
        return _error("Route name is required.")
    if distance_miles <= 0:
        return _error("Distance must be greater than zero.")

    new_id = dal.create_route(runner_id, route_name, distance_miles, elevation_gain_ft,
                              surface_type, description, start_location)
    return _ok({"route_id": new_id})


def fetch_route(route_id):
    route = dal.get_route_by_id(route_id)
    if not route:
        return _error(f"Route with ID {route_id} not found.")
    return _ok(route)


def fetch_all_routes():
    return _ok(dal.get_all_routes())


def modify_route(route_id, route_name, distance_miles, elevation_gain_ft=0,
                 surface_type=None, description=None, start_location=None):
    if not dal.get_route_by_id(route_id):
        return _error(f"Route with ID {route_id} not found.")
    if not route_name or distance_miles <= 0:
        return _error("Route name and positive distance are required.")

    affected = dal.update_route(route_id, route_name, distance_miles, elevation_gain_ft,
                                surface_type, description, start_location)
    return _ok({"rows_affected": affected})


def remove_route(route_id):
    if not dal.get_route_by_id(route_id):
        return _error(f"Route with ID {route_id} not found.")
    affected = dal.delete_route(route_id)
    return _ok({"rows_affected": affected})


# ─────────────────────────────────────────────
# RUNNING SHOES BUSINESS
# ─────────────────────────────────────────────

SHOE_MILEAGE_WARNING = 300  # miles before shoes should be replaced

def add_shoe(runner_id, brand, model, purchase_date, total_miles=0.0, retired=False, notes=None):
    """
    Business rule: brand and model are required.
    Business rule: runner must exist.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    if not brand or not model:
        return _error("Brand and model are required.")

    new_id = dal.create_shoe(runner_id, brand, model, purchase_date, total_miles, retired, notes)
    result = {"shoe_id": new_id}
    if total_miles >= SHOE_MILEAGE_WARNING:
        result["warning"] = f"These shoes already have {total_miles} miles. Consider retiring them soon."
    return _ok(result)


def fetch_shoe(shoe_id):
    shoe = dal.get_shoe_by_id(shoe_id)
    if not shoe:
        return _error(f"Shoe with ID {shoe_id} not found.")
    return _ok(shoe)


def fetch_all_shoes():
    return _ok(dal.get_all_shoes())


def modify_shoe(shoe_id, brand, model, total_miles, retired, notes=None):
    if not dal.get_shoe_by_id(shoe_id):
        return _error(f"Shoe with ID {shoe_id} not found.")

    affected = dal.update_shoe(shoe_id, brand, model, total_miles, retired, notes)
    result = {"rows_affected": affected}
    if total_miles >= SHOE_MILEAGE_WARNING and not retired:
        result["warning"] = f"Shoe has {total_miles} miles. Consider retiring it."
    return _ok(result)


def remove_shoe(shoe_id):
    if not dal.get_shoe_by_id(shoe_id):
        return _error(f"Shoe with ID {shoe_id} not found.")
    affected = dal.delete_shoe(shoe_id)
    return _ok({"rows_affected": affected})


# ─────────────────────────────────────────────
# TRAINING GOALS BUSINESS
# ─────────────────────────────────────────────

def add_goal(runner_id, goal_type, target_value, target_date,
             current_value=0.0, status="active", description=None):
    """
    Business rule: runner must exist.
    Business rule: target date cannot be in the past.
    Business rule: target value must be positive.
    """
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    if target_value <= 0:
        return _error("Target value must be positive.")

    # Parse target_date if it's a string
    if isinstance(target_date, str):
        try:
            td = date.fromisoformat(target_date)
        except ValueError:
            return _error("Invalid target date format. Use YYYY-MM-DD.")
    else:
        td = target_date

    if td < date.today():
        return _error("Target date cannot be in the past.")

    new_id = dal.create_goal(runner_id, goal_type, target_value, current_value,
                             target_date, status, description)
    return _ok({"goal_id": new_id})


def fetch_goal(goal_id):
    goal = dal.get_goal_by_id(goal_id)
    if not goal:
        return _error(f"Goal with ID {goal_id} not found.")
    # Business rule: compute progress percentage
    if goal.get("target_value") and goal["target_value"] > 0:
        goal["progress_pct"] = round((goal["current_value"] / goal["target_value"]) * 100, 1)
    return _ok(goal)


def fetch_all_goals():
    return _ok(dal.get_all_goals())


def fetch_goals_for_runner(runner_id):
    if not dal.get_runner_by_id(runner_id):
        return _error(f"Runner with ID {runner_id} not found.")
    return _ok(dal.get_goals_by_runner(runner_id))


def modify_goal(goal_id, target_value, current_value, target_date, status, description=None):
    if not dal.get_goal_by_id(goal_id):
        return _error(f"Goal with ID {goal_id} not found.")

    # Business rule: if current_value >= target_value, auto-complete the goal
    if current_value >= target_value and status != "completed":
        status = "completed"

    affected = dal.update_goal(goal_id, target_value, current_value, target_date, status, description)
    return _ok({"rows_affected": affected, "status": status})


def remove_goal(goal_id):
    if not dal.get_goal_by_id(goal_id):
        return _error(f"Goal with ID {goal_id} not found.")
    affected = dal.delete_goal(goal_id)
    return _ok({"rows_affected": affected})
