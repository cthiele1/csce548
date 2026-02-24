
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from business import business_layer as bl

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the browser frontend


# ─────────────────────────────────────────────
# GLOBAL ERROR HANDLER
# ─────────────────────────────────────────────

@app.errorhandler(Exception)
def handle_all_exceptions(e):
    """
    Convert all exceptions (HTTP and non-HTTP) to JSON responses so the client never
    receives HTML error pages. Keeps the message minimal for non-HTTP exceptions.
    """
    if isinstance(e, HTTPException):
        return jsonify({"success": False, "error": e.description}), e.code
    app.logger.exception("Unhandled exception")
    return jsonify({"success": False, "error": "Internal server error"}), 500


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def to_response(result):
    """
    Converts a business layer result dict to a Flask JSON response.
    Expected result shape: {"success": bool, "data": ..., "error": ...}
    """
    if result is None:
        return jsonify({"success": False, "error": "Internal error"}), 500

    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 400


def _sanitize_surface(surface_type):
    """Normalize and defensively truncate surface_type to one of the DB enum values."""
    if surface_type is None:
        return None
    s = str(surface_type).strip()
    if not s:
        return None
    s_lower = s.lower()
    mapping = {
        "paved": "Road",
        "road": "Road",
        "trail": "Trail",
        "mixed": "Mixed",
        "track": "Track",
        "treadmill": "Treadmill",
        "gravel": "Mixed",
        "dirt": "Trail",
    }
    if s_lower in mapping:
        normalized = mapping[s_lower]
    else:
        normalized = s.title()
    if len(normalized) > 255:
        normalized = normalized[:255]
    return normalized


def _normalize_run_type(rt):
    """Normalize run_type to the DB enum values or return None if missing."""
    if rt is None:
        return None
    s = str(rt).strip().lower()
    mapping = {
        "easy": "Easy",
        "tempo": "Tempo",
        "interval": "Interval",
        "long": "Long",
        "race": "Race",
        "recovery": "Recovery"
    }
    return mapping.get(s)


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
    data = request.get_json(silent=True) or {}
    try:
        result = bl.add_runner(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            weight_lbs=data.get("weight_lbs"),
            height_inches=data.get("height_inches")
        )
    except Exception as e:
        app.logger.exception("Error in create_runner")
        return jsonify({"success": False, "error": f"{type(e).__name__}: {str(e)}"}), 500

    if result.get("success"):
        return jsonify(result), 201
    return to_response(result)


@app.route("/runners/<int:runner_id>", methods=["PUT"])
def update_runner(runner_id):
    """PUT /runners/<id> - Update an existing runner."""
    data = request.get_json(silent=True) or {}
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
    data = request.get_json(silent=True) or {}
    data.pop("pace_min_per_mile", None)

    if not data.get("runner_id") or data.get("distance_miles") is None or data.get("duration_minutes") is None:
        return jsonify({"success": False, "error": "Missing required fields: runner_id, distance_miles, duration_minutes"}), 400

    try:
        distance = float(data.get("distance_miles"))
        duration = float(data.get("duration_minutes"))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid numeric values for distance_miles or duration_minutes"}), 400

    if distance <= 0:
        return jsonify({"success": False, "error": "distance_miles must be greater than 0"}), 400
    if duration <= 0:
        return jsonify({"success": False, "error": "duration_minutes must be greater than 0"}), 400

    run_type = _normalize_run_type(data.get("run_type"))
    if data.get("run_type") and run_type is None:
        return jsonify({"success": False, "error": f"Invalid run_type: {data.get('run_type')}"}), 400

    try:
        new_id = bl.log_run(
            runner_id=data.get("runner_id"),
            run_date=data.get("run_date"),
            distance_miles=distance,
            duration_minutes=int(duration),
            run_type=run_type,
            route_id=data.get("route_id"),
            shoe_id=data.get("shoe_id"),
            average_heart_rate=data.get("average_heart_rate"),
            calories_burned=data.get("calories_burned"),
            weather=data.get("weather"),
            temperature_f=data.get("temperature_f"),
            notes=data.get("notes")
        )
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception:
        app.logger.exception("Error logging run")
        return jsonify({"success": False, "error": "Internal server error"}), 500

    if isinstance(new_id, dict) and new_id.get("success"):
        return jsonify(new_id), 201
    return to_response(new_id)


@app.route("/runs/<int:run_id>", methods=["PUT"])
def update_run(run_id):
    """PUT /runs/<id> - Update a run."""
    data = request.get_json(silent=True) or {}
    data.pop("pace_min_per_mile", None)

    if data.get("distance_miles") is not None:
        try:
            distance = float(data.get("distance_miles"))
            if distance <= 0:
                return jsonify({"success": False, "error": "distance_miles must be greater than 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Invalid numeric value for distance_miles"}), 400

    if data.get("duration_minutes") is not None:
        try:
            duration = float(data.get("duration_minutes"))
            if duration <= 0:
                return jsonify({"success": False, "error": "duration_minutes must be greater than 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Invalid numeric value for duration_minutes"}), 400

    if "run_type" in data:
        run_type = _normalize_run_type(data.get("run_type"))
        if data.get("run_type") and run_type is None:
            return jsonify({"success": False, "error": f"Invalid run_type: {data.get('run_type')}"}), 400
        data["run_type"] = run_type

    result = bl.modify_run(
        run_id=run_id,
        distance_miles=data.get("distance_miles"),
        duration_minutes=data.get("duration_minutes"),
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
    data = request.get_json(silent=True) or {}
    surface = _sanitize_surface(data.get("surface_type"))
    result = bl.add_route(
        runner_id=data.get("runner_id"),
        route_name=data.get("route_name"),
        distance_miles=data.get("distance_miles"),
        elevation_gain_ft=data.get("elevation_gain_ft", 0),
        surface_type=surface,
        description=data.get("description"),
        start_location=data.get("start_location")
    )
    if result.get("success"):
        return jsonify(result), 201
    return to_response(result)


@app.route("/routes/<int:route_id>", methods=["PUT"])
def update_route(route_id):
    data = request.get_json(silent=True) or {}
    surface = _sanitize_surface(data.get("surface_type"))
    result = bl.modify_route(
        route_id=route_id,
        route_name=data.get("route_name"),
        distance_miles=data.get("distance_miles"),
        elevation_gain_ft=data.get("elevation_gain_ft", 0),
        surface_type=surface,
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
    data = request.get_json(silent=True) or {}
    result = bl.add_shoe(
        runner_id=data.get("runner_id"),
        brand=data.get("brand"),
        model=data.get("model"),
        purchase_date=data.get("purchase_date"),
        total_miles=data.get("total_miles", 0.0),
        retired=data.get("retired", False),
        notes=data.get("notes")
    )
    if result.get("success"):
        return jsonify(result), 201
    return to_response(result)


@app.route("/shoes/<int:shoe_id>", methods=["PUT"])
def update_shoe(shoe_id):
    data = request.get_json(silent=True) or {}
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
    data = request.get_json(silent=True) or {}
    result = bl.add_goal(
        runner_id=data.get("runner_id"),
        goal_type=data.get("goal_type"),
        target_value=data.get("target_value"),
        target_date=data.get("target_date"),
        current_value=data.get("current_value", 0.0),
        status=data.get("status", "active"),
        description=data.get("description")
    )
    if result.get("success"):
        return jsonify(result), 201
    return to_response(result)


@app.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    data = request.get_json(silent=True) or {}
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