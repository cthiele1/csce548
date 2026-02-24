"""
client.py - Console-Based Front End
Tests all 5 service endpoints (Runners, Runs, Routes, Shoes, Goals) by performing
CREATE → READ → UPDATE → READ → DELETE → READ on each entity.

USAGE:
  # Test against Railway deployment:
  BASE_URL=https://your-app.up.railway.app python client.py

  # Test against local server:
  python client.py
"""

import os
import sys
import json
import requests
from datetime import date, timedelta

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

PASS = "✓"
FAIL = "✗"


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def step(num, description):
    print(f"\n{num}. {description}")


def check(response, label=""):
    body = response.json()
    if response.status_code == 200 and body.get("success"):
        print(f"  {PASS} {label or 'OK'}")
        print(f"     Response: {json.dumps(body.get('data'), indent=4, default=str)}")
        return body.get("data")
    else:
        print(f"  {FAIL} FAILED: {body.get('error', 'Unknown error')}")
        return None


# ─────────────────────────────────────────────
# RUNNER CRUD TEST
# ─────────────────────────────────────────────

def test_runners():
    header("Testing Runner CRUD Operations")
    runner_id = None

    step(1, "CREATE - Adding new runner...")
    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Test",
        "last_name": "Runner",
        "email": "test.runner@example.com",
        "date_of_birth": "1990-06-15",
        "gender": "M",
        "weight_lbs": 160,
        "height_inches": 70
    })
    data = check(r, "Runner created")
    if data:
        runner_id = data["runner_id"]

    step(2, f"READ - Retrieving runner ID {runner_id}...")
    r = requests.get(f"{BASE_URL}/runners/{runner_id}")
    check(r, "Runner retrieved")

    step(3, "UPDATE - Updating runner weight to 155 lbs...")
    r = requests.put(f"{BASE_URL}/runners/{runner_id}", json={
        "first_name": "Test",
        "last_name": "Runner",
        "email": "test.runner@example.com",
        "weight_lbs": 155,
        "height_inches": 70
    })
    check(r, "Runner updated")

    step(4, "READ ALL - Getting all runners...")
    r = requests.get(f"{BASE_URL}/runners")
    data = check(r, "All runners retrieved")
    if data:
        print(f"     Total runners: {len(data)}")

    step(5, f"DELETE - Removing runner ID {runner_id}...")
    r = requests.delete(f"{BASE_URL}/runners/{runner_id}")
    check(r, "Runner deleted")

    step(6, f"READ (verify delete) - Runner {runner_id} should not be found...")
    r = requests.get(f"{BASE_URL}/runners/{runner_id}")
    body = r.json()
    if not body.get("success"):
        print(f"  {PASS} Correctly returned not found: {body.get('error')}")
    else:
        print(f"  {FAIL} Runner still exists after delete!")

    print("\n  Runner CRUD test complete!")
    return runner_id


# ─────────────────────────────────────────────
# RUN CRUD TEST
# ─────────────────────────────────────────────

def test_runs(runner_id):
    header("Testing Run CRUD Operations")
    run_id = None

    # First create a temporary runner to own this run
    step(0, "Setup - Creating a temporary runner for run tests...")
    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Temp",
        "last_name": "Runner",
        "email": "temp@example.com",
        "date_of_birth": "1985-01-01",
        "gender": "F"
    })
    data = check(r, "Temp runner created")
    temp_runner_id = data["runner_id"] if data else None

    step(1, "CREATE - Logging a new run...")
    r = requests.post(f"{BASE_URL}/runs", json={
        "runner_id": temp_runner_id,
        "run_date": str(date.today()),
        "distance_miles": 5.0,
        "duration_minutes": 45,
        "run_type": "Easy",
        "weather": "Sunny",
        "temperature_f": 68,
        "notes": "Test run via client"
    })
    data = check(r, "Run logged")
    if data:
        run_id = data["run_id"]

    step(2, f"READ - Retrieving run ID {run_id}...")
    r = requests.get(f"{BASE_URL}/runs/{run_id}")
    check(r, "Run retrieved")

    step(3, "UPDATE - Updating run distance and duration...")
    r = requests.put(f"{BASE_URL}/runs/{run_id}", json={
        "distance_miles": 5.2,
        "duration_minutes": 47,
        "notes": "Updated via client test"
    })
    check(r, "Run updated")

    step(4, f"READ - Runner {temp_runner_id}'s runs...")
    r = requests.get(f"{BASE_URL}/runs?runner_id={temp_runner_id}")
    data = check(r, "Runner's runs retrieved")

    step(5, f"DELETE - Removing run ID {run_id}...")
    r = requests.delete(f"{BASE_URL}/runs/{run_id}")
    check(r, "Run deleted")

    # Cleanup temp runner
    requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
    print("\n  Run CRUD test complete!")


# ─────────────────────────────────────────────
# ROUTE CRUD TEST
# ─────────────────────────────────────────────

def test_routes():
    header("Testing Route CRUD Operations")

    # Need a runner first
    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Route",
        "last_name": "Tester",
        "email": "route.tester@example.com",
        "date_of_birth": "1992-03-20",
        "gender": "M"
    })
    data = check(r, "Temp runner created")
    temp_runner_id = data["runner_id"] if data else None

    step(1, "CREATE - Adding a new route...")
    r = requests.post(f"{BASE_URL}/routes", json={
        "runner_id": temp_runner_id,
        "route_name": "Test Loop",
        "distance_miles": 3.1,
        "elevation_gain_ft": 120,
        "surface_type": "paved",
        "description": "A quick test loop",
        "start_location": "City Park"
    })
    data = check(r, "Route created")
    route_id = data["route_id"] if data else None

    step(2, f"READ - Retrieving route ID {route_id}...")
    r = requests.get(f"{BASE_URL}/routes/{route_id}")
    check(r, "Route retrieved")

    step(3, "UPDATE - Updating route distance...")
    r = requests.put(f"{BASE_URL}/routes/{route_id}", json={
        "route_name": "Test Loop (Updated)",
        "distance_miles": 3.2,
        "elevation_gain_ft": 125,
        "surface_type": "paved"
    })
    check(r, "Route updated")

    step(4, f"DELETE - Removing route ID {route_id}...")
    r = requests.delete(f"{BASE_URL}/routes/{route_id}")
    check(r, "Route deleted")

    requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
    print("\n  Route CRUD test complete!")


# ─────────────────────────────────────────────
# SHOE CRUD TEST
# ─────────────────────────────────────────────

def test_shoes():
    header("Testing Shoe CRUD Operations")

    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Shoe",
        "last_name": "Tester",
        "email": "shoe.tester@example.com",
        "date_of_birth": "1988-11-05",
        "gender": "F"
    })
    data = check(r, "Temp runner created")
    temp_runner_id = data["runner_id"] if data else None

    step(1, "CREATE - Adding a new shoe...")
    r = requests.post(f"{BASE_URL}/shoes", json={
        "runner_id": temp_runner_id,
        "brand": "Nike",
        "model": "Pegasus 40",
        "purchase_date": str(date.today()),
        "total_miles": 0.0,
        "retired": False,
        "notes": "Test shoe"
    })
    data = check(r, "Shoe created")
    shoe_id = data["shoe_id"] if data else None

    step(2, f"READ - Retrieving shoe ID {shoe_id}...")
    r = requests.get(f"{BASE_URL}/shoes/{shoe_id}")
    check(r, "Shoe retrieved")

    step(3, "UPDATE - Adding 50 miles to shoe...")
    r = requests.put(f"{BASE_URL}/shoes/{shoe_id}", json={
        "brand": "Nike",
        "model": "Pegasus 40",
        "total_miles": 50.0,
        "retired": False,
        "notes": "Updated mileage"
    })
    check(r, "Shoe updated")

    step(4, f"DELETE - Removing shoe ID {shoe_id}...")
    r = requests.delete(f"{BASE_URL}/shoes/{shoe_id}")
    check(r, "Shoe deleted")

    requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
    print("\n  Shoe CRUD test complete!")


# ─────────────────────────────────────────────
# GOAL CRUD TEST
# ─────────────────────────────────────────────

def test_goals():
    header("Testing Training Goal CRUD Operations")

    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Goal",
        "last_name": "Tester",
        "email": "goal.tester@example.com",
        "date_of_birth": "1995-07-14",
        "gender": "M"
    })
    data = check(r, "Temp runner created")
    temp_runner_id = data["runner_id"] if data else None

    future_date = str(date.today() + timedelta(days=90))

    step(1, "CREATE - Adding a new training goal...")
    r = requests.post(f"{BASE_URL}/goals", json={
        "runner_id": temp_runner_id,
        "goal_type": "distance",
        "target_value": 100.0,
        "current_value": 0.0,
        "target_date": future_date,
        "status": "active",
        "description": "Run 100 miles this quarter"
    })
    data = check(r, "Goal created")
    goal_id = data["goal_id"] if data else None

    step(2, f"READ - Retrieving goal ID {goal_id} (with progress %)...")
    r = requests.get(f"{BASE_URL}/goals/{goal_id}")
    check(r, "Goal retrieved")

    step(3, "UPDATE - Updating current progress to 40 miles...")
    r = requests.put(f"{BASE_URL}/goals/{goal_id}", json={
        "target_value": 100.0,
        "current_value": 40.0,
        "target_date": future_date,
        "status": "active",
        "description": "Making good progress!"
    })
    check(r, "Goal updated")

    step(4, f"DELETE - Removing goal ID {goal_id}...")
    r = requests.delete(f"{BASE_URL}/goals/{goal_id}")
    check(r, "Goal deleted")

    requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
    print("\n  Goal CRUD test complete!")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  RUNNING TRACKER - SERVICE LAYER TEST CLIENT")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    # Health check first
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        if r.status_code == 200:
            print(f"\n{PASS} Service is online!")
        else:
            print(f"\n{FAIL} Service returned status {r.status_code}")
            sys.exit(1)
    except requests.ConnectionError:
        print(f"\n{FAIL} Could not connect to {BASE_URL}")
        print("  Make sure the Flask app is running.")
        sys.exit(1)

    test_runners()
    test_runs(None)
    test_routes()
    test_shoes()
    test_goals()

    print("\n" + "=" * 60)
    print("  ALL CRUD TESTS COMPLETE!")
    print("=" * 60)
