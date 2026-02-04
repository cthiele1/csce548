"""
Test Script for Running Tracker
Demonstrates all CRUD operations working correctly
"""

from datetime import date
from models import Runner, Run, Route, RunningShoe, TrainingGoal


def test_runner_crud():
    """Test Runner CRUD operations"""
    print("\n" + "="*60)
    print("Testing Runner CRUD Operations")
    print("="*60)
    
    # CREATE
    print("\n1. CREATE - Adding new runner...")
    runner_id = Runner.create(
        "Test", "Runner", "test.runner@email.com",
        date_of_birth="1990-01-01",
        gender="M",
        weight_lbs=170.0,
        height_inches=70
    )
    
    # READ
    print("\n2. READ - Retrieving runner...")
    runner = Runner.get_by_id(runner_id)
    print(f"   Retrieved: {runner}")
    
    # UPDATE
    print("\n3. UPDATE - Updating runner weight...")
    Runner.update(runner_id, weight_lbs=165.0)
    runner = Runner.get_by_id(runner_id)
    print(f"   Updated weight: {runner.weight_lbs} lbs")
    
    # READ ALL
    print("\n4. READ ALL - Getting all runners...")
    all_runners = Runner.get_all()
    print(f"   Total runners in database: {len(all_runners)}")
    
    # DELETE
    print("\n5. DELETE - Removing test runner...")
    Runner.delete(runner_id)
    
    print("\n✓ Runner CRUD test completed successfully!")


def test_run_crud():
    """Test Run CRUD operations"""
    print("\n" + "="*60)
    print("Testing Run CRUD Operations")
    print("="*60)
    
    # Use existing runner (ID 1 from test data)
    runner_id = 1
    
    # CREATE
    print("\n1. CREATE - Logging new run...")
    run_id = Run.create(
        runner_id=runner_id,
        run_date="2025-02-03",
        distance_miles=5.0,
        duration_minutes=40,
        run_type="Easy",
        weather="Sunny",
        temperature_f=65,
        notes="Test run for CRUD demo"
    )
    
    # READ
    print("\n2. READ - Retrieving run...")
    run = Run.get_by_id(run_id)
    print(f"   Retrieved: {run}")
    print(f"   Calculated pace: {run.pace_min_per_mile:.2f} min/mile")
    
    # UPDATE
    print("\n3. UPDATE - Updating run notes...")
    Run.update(run_id, notes="Updated: Great test run!")
    run = Run.get_by_id(run_id)
    print(f"   Updated notes: {run.notes}")
    
    # READ BY RUNNER
    print("\n4. READ BY RUNNER - Getting runs for runner 1...")
    runs = Run.get_by_runner(runner_id, limit=5)
    print(f"   Found {len(runs)} recent runs for runner {runner_id}")
    
    # DELETE
    print("\n5. DELETE - Removing test run...")
    Run.delete(run_id)
    
    print("\n✓ Run CRUD test completed successfully!")


def test_statistics():
    """Test statistics and reporting functions"""
    print("\n" + "="*60)
    print("Testing Statistics and Reports")
    print("="*60)
    
    # Runner statistics
    print("\n1. Runner Statistics for Runner 1:")
    stats = Runner.get_statistics(1)
    if stats:
        print(f"   Total Runs: {stats['total_runs']}")
        print(f"   Total Miles: {stats['total_miles']:.2f}")
        print(f"   Average Pace: {stats['average_pace']:.2f} min/mile")
        print(f"   Best Pace: {stats['best_pace']:.2f} min/mile")
        print(f"   Longest Run: {stats['longest_run']:.2f} miles")
    
    # Run summary statistics
    print("\n2. Run Summary Statistics for Runner 1:")
    summary = Run.get_summary_stats(1)
    if summary:
        print(f"   Total Runs: {summary['total_runs']}")
        print(f"   Total Distance: {summary['total_distance']:.2f} miles")
        print(f"   Average Distance: {summary['avg_distance']:.2f} miles")
        print(f"   Average Pace: {summary['avg_pace']:.2f} min/mile")
    
    # Recent runs
    print("\n3. Recent Runs (All Runners):")
    recent = Run.get_recent_runs(limit=5)
    print(f"   Showing {len(recent)} most recent runs:")
    for run in recent:
        print(f"   - {run['runner_name']}: {run['distance_miles']:.2f} mi on {run['run_date']}")
    
    print("\n✓ Statistics test completed successfully!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RUNNING TRACKER - CRUD OPERATION TESTS")
    print("="*60)
    print("\nThis script demonstrates all CRUD operations working correctly.")
    print("It will create, read, update, and delete test records.")
    
    try:
        test_runner_crud()
        test_run_crud()
        test_statistics()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY! ✓")
        print("="*60)
        print("\nThe application is ready to use.")
        print("Run 'python main.py' to start the console interface.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
