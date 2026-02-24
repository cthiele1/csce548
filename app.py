"""
app.py - Service Layer: Flask REST API
Exposes all business layer methods as HTTP endpoints.

HOSTING ON RAILWAY:
  1. Push this project to a GitHub repo.
  2. Go to https://railway.app and create a new project from your GitHub repo.
  3. Railway will auto-detect Python. It will look for a Procfile or requirements.txt.
  4. In Railway Dashboard > Variables, add these environment variables:
       DB_HOST     = your MySQL host (use Railway MySQL plugin if hosted there)
       DB_PORT     = 3306
       DB_NAME     = running_tracker
       DB_USER     = your db username
       DB_PASSWORD = your db password
       PORT        = 5000  (Railway sets this automatically)
  5. Railway will build and deploy automatically on every git push.
  6. Your API base URL will be: https://<your-app>.up.railway.app

RUNNING LOCALLY:
  pip install flask mysql-connector-python
  python app.py
"""

import os
from flask import Flask, request, jsonify
from business import business_layer as bl

app = Flask(__name__)


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def to_response(result):
    """Converts a business layer result dict to a Flask JSON response."""
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# ─────────────────────────────────────────────
# RUNNER ENDPOINTS
# ─────────────────────────────────────────────

@app.route("/runners", methods=["GET"])
def get_runners():
    """GET /runners - Retrieve all runners."""
    return to_response(bl.fetch_all_runners())


@app.route("/runners/<int:runner_id>", methods=["GET"])
def get_runner(runner_id):
    """GET /runners/<id> - Retrieve a specific runner."""
    return to_response(bl.fetch_runner(runner_id))


@app.route("/runners", methods=["POST"])
def create_runner():
    """POST /runners - Add a new runner. Body: JSON with runner fields."""
    data = request.get_json()
    result = bl.add_runner(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        date_of_birth=data.get("date_of_birth"),
        gender=data.get("gender"),
        weight_lbs=data.get("weight_lbs"),
        height_inches=data.get("height_inches")
    )
    return to_response(result)


@app.route("/runners/<int:runner_id>", methods=["PUT"])
def update_runner(runner_id):
    """PUT /runners/<id> - Update an existing runner."""
    data = request.get_json()
    result = bl.modify_runner(
        runner_id=runner_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        weight_lbs=data.get("weight_lbs"),
        height_inches=data.get("height_inches")
    )
    return to_response(result)


@app.route("/runners/<int:runner_id>", methods=["DELETE"])
def delete_runner(runner_id):
    """DELETE /runners/<id> - Remove a runner."""
    return to_response(bl.remove_runner(runner_id))


# ─────────────────────────────────────────────
# RUN ENDPOINTS
# ─────────────────────────────────────────────

@app.route("/runs", methods=["GET"])
def get_runs():
    """GET /runs - Retrieve all runs. Optional ?runner_id=X to filter by runner."""
    runner_id = request.args.get("runner_id", type=int)
    if runner_id:
        return to_response(bl.fetch_runs_for_runner(runner_id))
    return to_response(bl.fetch_all_runs())


@app.route("/runs/<int:run_id>", methods=["GET"])
def get_run(run_id):
    """GET /runs/<id> - Retrieve a specific run."""
    return to_response(bl.fetch_run(run_id))


@app.route("/runs", methods=["POST"])
def create_run():
    """POST /runs - Log a new run."""
    data = request.get_json()
    result = bl.log_run(
        runner_id=data.get("runner_id"),
        run_date=data.get("run_date"),
        distance_miles=data.get("distance_miles"),
        duration_minutes=data.get("duration_minutes"),
        run_type=data.get("run_type"),
        route_id=data.get("route_id"),
        shoe_id=data.get("shoe_id"),
        pace_min_per_mile=data.get("pace_min_per_mile"),
        average_heart_rate=data.get("average_heart_rate"),
        calories_burned=data.get("calories_burned"),
        weather=data.get("weather"),
        temperature_f=data.get("temperature_f"),
        notes=data.get("notes")
    )
    return to_response(result)


@app.route("/runs/<int:run_id>", methods=["PUT"])
def update_run(run_id):
    """PUT /runs/<id> - Update a run."""
    data = request.get_json()
    result = bl.modify_run(
        run_id=run_id,
        distance_miles=data.get("distance_miles"),
        duration_minutes=data.get("duration_minutes"),
        pace_min_per_mile=data.get("pace_min_per_mile"),
        average_heart_rate=data.get("average_heart_rate"),
        calories_burned=data.get("calories_burned"),
        notes=data.get("notes")
    )
    return to_response(result)


@app.route("/runs/<int:run_id>", methods=["DELETE"])
def delete_run(run_id):
    """DELETE /runs/<id> - Remove a run."""
    return to_response(bl.remove_run(run_id))


# ─────────────────────────────────────────────
# ROUTE ENDPOINTS
# ─────────────────────────────────────────────

@app.route("/routes", methods=["GET"])
def get_routes():
    """GET /routes - Retrieve all routes."""
    return to_response(bl.fetch_all_routes())


@app.route("/routes/<int:route_id>", methods=["GET"])
def get_route(route_id):
    return to_response(bl.fetch_route(route_id))


@app.route("/routes", methods=["POST"])
def create_route():
    data = request.get_json()
    result = bl.add_route(
        runner_id=data.get("runner_id"),
        route_name=data.get("route_name"),
        distance_miles=data.get("distance_miles"),
        elevation_gain_ft=data.get("elevation_gain_ft", 0),
        surface_type=data.get("surface_type"),
        description=data.get("description"),
        start_location=data.get("start_location")
    )
    return to_response(result)


@app.route("/routes/<int:route_id>", methods=["PUT"])
def update_route(route_id):
    data = request.get_json()
    result = bl.modify_route(
        route_id=route_id,
        route_name=data.get("route_name"),
        distance_miles=data.get("distance_miles"),
        elevation_gain_ft=data.get("elevation_gain_ft", 0),
        surface_type=data.get("surface_type"),
        description=data.get("description"),
        start_location=data.get("start_location")
    )
    return to_response(result)


@app.route("/routes/<int:route_id>", methods=["DELETE"])
def delete_route(route_id):
    return to_response(bl.remove_route(route_id))


# ─────────────────────────────────────────────
# SHOE ENDPOINTS
# ─────────────────────────────────────────────

@app.route("/shoes", methods=["GET"])
def get_shoes():
    """GET /shoes - Retrieve all shoes."""
    return to_response(bl.fetch_all_shoes())


@app.route("/shoes/<int:shoe_id>", methods=["GET"])
def get_shoe(shoe_id):
    return to_response(bl.fetch_shoe(shoe_id))


@app.route("/shoes", methods=["POST"])
def create_shoe():
    data = request.get_json()
    result = bl.add_shoe(
        runner_id=data.get("runner_id"),
        brand=data.get("brand"),
        model=data.get("model"),
        purchase_date=data.get("purchase_date"),
        total_miles=data.get("total_miles", 0.0),
        retired=data.get("retired", False),
        notes=data.get("notes")
    )
    return to_response(result)


@app.route("/shoes/<int:shoe_id>", methods=["PUT"])
def update_shoe(shoe_id):
    data = request.get_json()
    result = bl.modify_shoe(
        shoe_id=shoe_id,
        brand=data.get("brand"),
        model=data.get("model"),
        total_miles=data.get("total_miles"),
        retired=data.get("retired"),
        notes=data.get("notes")
    )
    return to_response(result)


@app.route("/shoes/<int:shoe_id>", methods=["DELETE"])
def delete_shoe(shoe_id):
    return to_response(bl.remove_shoe(shoe_id))


# ─────────────────────────────────────────────
# TRAINING GOAL ENDPOINTS
# ─────────────────────────────────────────────

@app.route("/goals", methods=["GET"])
def get_goals():
    """GET /goals - Retrieve all goals. Optional ?runner_id=X to filter."""
    runner_id = request.args.get("runner_id", type=int)
    if runner_id:
        return to_response(bl.fetch_goals_for_runner(runner_id))
    return to_response(bl.fetch_all_goals())


@app.route("/goals/<int:goal_id>", methods=["GET"])
def get_goal(goal_id):
    return to_response(bl.fetch_goal(goal_id))


@app.route("/goals", methods=["POST"])
def create_goal():
    data = request.get_json()
    result = bl.add_goal(
        runner_id=data.get("runner_id"),
        goal_type=data.get("goal_type"),
        target_value=data.get("target_value"),
        target_date=data.get("target_date"),
        current_value=data.get("current_value", 0.0),
        status=data.get("status", "active"),
        description=data.get("description")
    )
    return to_response(result)


@app.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    data = request.get_json()
    result = bl.modify_goal(
        goal_id=goal_id,
        target_value=data.get("target_value"),
        current_value=data.get("current_value"),
        target_date=data.get("target_date"),
        status=data.get("status"),
        description=data.get("description")
    )
    return to_response(result)


@app.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    return to_response(bl.remove_goal(goal_id))


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """GET /health - Simple health check endpoint."""
    return jsonify({"status": "ok", "service": "Running Tracker API"}), 200


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
