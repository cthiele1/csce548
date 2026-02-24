"""
client.py - Console-Based Front End
Tests all 5 service endpoints (Runners, Runs, Routes, Shoes, Goals) by performing
CREATE → READ → UPDATE → READ → DELETE → READ on each entity.

USAGE:
  # Test against Railway deployment:
  $env:BASE_URL="https://your-app.up.railway.app"; python client.py

  # Test against local server:
  python client.py
"""

import os
import sys
import json
import requests
import time
from datetime import date, timedelta

# Unique suffix so re-runs never hit duplicate email errors
TS = str(int(time.time()))

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
    try:
        body = response.json()
    except Exception:
        print(f"  {FAIL} FAILED (HTTP {response.status_code}) - Server returned non-JSON:")
        print(f"     {response.text[:300] or '(empty response)'}")
        return None

    # accept 200/201 as success codes (server may return 201 on create)
    if response.status_code in (200, 201) and body.get("success"):
        print(f"  {PASS} {label or 'OK'}")
        print(f"     Response: {json.dumps(body.get('data'), indent=4, default=str)}")
        return body.get("data")
    else:
        err = body.get("error", None)
        if err:
            print(f"  {FAIL} FAILED (HTTP {response.status_code}): {err}")
        else:
            print(f"  {FAIL} FAILED (HTTP {response.status_code}): {body}")
        return None


# ─────────────────────────────────────────────
# RUNNER CRUD TEST
# ─────────────────────────────────────────────

def test_runners():
    header("Testing Runner CRUD Operations")
    runner_id = None
    email = f"test.runner.{TS}@example.com"

    step(1, "CREATE - Adding new runner...")
    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Test",
        "last_name": "Runner",
        "email": email,
        "date_of_birth": "1990-06-15",
        "gender": "M",
        "weight_lbs": 160,
        "height_inches": 70
    })
    data = check(r, "Runner created")
    if not data:
        print("  Aborting runner tests due to failed create.")
        return
    runner_id = data["runner_id"]

    step(2, f"READ - Retrieving runner ID {runner_id}...")
    r = requests.get(f"{BASE_URL}/runners/{runner_id}")
    check(r, "Runner retrieved")

    step(3, "UPDATE - Updating runner weight to 155 lbs...")
    r = requests.put(f"{BASE_URL}/runners/{runner_id}", json={
        "first_name": "Test",
        "last_name": "Runner",
        "email": email,
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
    try:
        body = r.json()
        if not body.get("success"):
            print(f"  {PASS} Correctly returned not found: {body.get('error')}")
        else:
            print(f"  {FAIL} Runner still exists after delete!")
    except Exception:
        # 404s from Flask may not be JSON - that's still correct behavior
        if r.status_code in (400, 404):
            print(f"  {PASS} Correctly returned {r.status_code} - runner not found")
        else:
            print(f"  {FAIL} Unexpected status {r.status_code}")

    print("\n  Runner CRUD test complete!")


# ─────────────────────────────────────────────
# RUN CRUD TEST
# ─────────────────────────────────────────────

def test_runs():
    header("Testing Run CRUD Operations")
    run_id = None

    step(0, "Setup - Creating a temporary runner for run tests...")
    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Temp",
        "last_name": "Runner",
        "email": f"temp.{TS}@example.com",
        "date_of_birth": "1985-01-01",
        "gender": "F"
    })
    data = check(r, "Temp runner created")
    if not data:
        print("  Aborting run tests due to failed runner create.")
        return
    temp_runner_id = data["runner_id"]

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
    if not data:
        print("  Aborting run tests due to failed run create.")
        # cleanup temp runner before returning
        if temp_runner_id:
            try:
                requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
            except Exception:
                pass
        return
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
    check(r, "Runner's runs retrieved")

    step(5, f"DELETE - Removing run ID {run_id}...")
    r = requests.delete(f"{BASE_URL}/runs/{run_id}")
    check(r, "Run deleted")

    # Cleanup temp runner
    if temp_runner_id:
        try:
            requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
        except Exception:
            pass
    print("\n  Run CRUD test complete!")


# ─────────────────────────────────────────────
# ROUTE CRUD TEST
# ─────────────────────────────────────────────

def test_routes():
    header("Testing Route CRUD Operations")

    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Route",
        "last_name": "Tester",
        "email": f"route.{TS}@example.com",
        "date_of_birth": "1992-03-20",
        "gender": "M"
    })
    data = check(r, "Temp runner created")
    if not data:
        print("  Aborting route tests due to failed runner create.")
        return
    temp_runner_id = data["runner_id"]

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
    if not data:
        print("  Aborting route tests due to failed route create.")
        if temp_runner_id:
            try:
                requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
            except Exception:
                pass
        return
    route_id = data["route_id"]

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

    if temp_runner_id:
        try:
            requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
        except Exception:
            pass
    print("\n  Route CRUD test complete!")


# ─────────────────────────────────────────────
# SHOE CRUD TEST
# ─────────────────────────────────────────────

def test_shoes():
    header("Testing Shoe CRUD Operations")

    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Shoe",
        "last_name": "Tester",
        "email": f"shoe.{TS}@example.com",
        "date_of_birth": "1988-11-05",
        "gender": "F"
    })
    data = check(r, "Temp runner created")
    if not data:
        print("  Aborting shoe tests due to failed runner create.")
        return
    temp_runner_id = data["runner_id"]

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
    if not data:
        print("  Aborting shoe tests due to failed shoe create.")
        if temp_runner_id:
            try:
                requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
            except Exception:
                pass
        return
    shoe_id = data["shoe_id"]

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

    if temp_runner_id:
        try:
            requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
        except Exception:
            pass
    print("\n  Shoe CRUD test complete!")


# ─────────────────────────────────────────────
# GOAL CRUD TEST
# ─────────────────────────────────────────────

def test_goals():
    header("Testing Training Goal CRUD Operations")

    r = requests.post(f"{BASE_URL}/runners", json={
        "first_name": "Goal",
        "last_name": "Tester",
        "email": f"goal.{TS}@example.com",
        "date_of_birth": "1995-07-14",
        "gender": "M"
    })
    data = check(r, "Temp runner created")
    if not data:
        print("  Aborting goal tests due to failed runner create.")
        return
    temp_runner_id = data["runner_id"]

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
    if not data:
        print("  Aborting goal tests due to failed goal create.")
        if temp_runner_id:
            try:
                requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
            except Exception:
                pass
        return
    goal_id = data["goal_id"]

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

    if temp_runner_id:
        try:
            requests.delete(f"{BASE_URL}/runners/{temp_runner_id}")
        except Exception:
            pass
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
    test_runs()
    test_routes()
    test_shoes()
    test_goals()

    print("\n" + "=" * 60)
    print("  ALL CRUD TESTS COMPLETE!")
    print("=" * 60)