"""
Running Tracker - Console Application
Main console interface for interacting with the running tracker database
"""

import sys
from datetime import date, datetime, timedelta
from models import Runner, Run, Route, RunningShoe, TrainingGoal


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_menu(title, options):
    """Print a menu with options"""
    print(f"\n{title}")
    print("-" * 40)
    for key, value in options.items():
        print(f"  {key}. {value}")
    print()


def display_runners(runners):
    """Display a list of runners"""
    if not runners:
        print("No runners found.")
        return
    
    print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Runs':<10}")
    print("-" * 75)
    
    for runner in runners:
        stats = Runner.get_statistics(runner.runner_id)
        total_runs = stats['total_runs'] if stats else 0
        name = f"{runner.first_name} {runner.last_name}"
        print(f"{runner.runner_id:<5} {name:<25} {runner.email:<30} {total_runs:<10}")


def display_runs(runs):
    """Display a list of runs"""
    if not runs:
        print("No runs found.")
        return
    
    print(f"\n{'ID':<5} {'Date':<12} {'Distance':<10} {'Time':<8} {'Pace':<8} {'Type':<12}")
    print("-" * 70)
    
    for run in runs:
        distance = f"{run.distance_miles:.2f} mi"
        duration = f"{run.duration_minutes} min"
        pace = f"{run.pace_min_per_mile:.2f}" if run.pace_min_per_mile else "N/A"
        print(f"{run.run_id:<5} {str(run.run_date):<12} {distance:<10} {duration:<8} {pace:<8} {run.run_type:<12}")


def display_routes(routes):
    """Display a list of routes"""
    if not routes:
        print("No routes found.")
        return
    
    print(f"\n{'ID':<5} {'Name':<25} {'Distance':<12} {'Elevation':<12} {'Surface':<12}")
    print("-" * 75)
    
    for route in routes:
        distance = f"{route.distance_miles:.2f} mi"
        elevation = f"{route.elevation_gain_ft} ft"
        print(f"{route.route_id:<5} {route.route_name:<25} {distance:<12} {elevation:<12} {route.surface_type:<12}")


def display_shoes(shoes):
    """Display a list of shoes"""
    if not shoes:
        print("No shoes found.")
        return
    
    print(f"\n{'ID':<5} {'Brand':<15} {'Model':<20} {'Miles':<10} {'Status':<10}")
    print("-" * 65)
    
    for shoe in shoes:
        miles = f"{shoe.total_miles:.2f}"
        status = "Retired" if shoe.retired else "Active"
        print(f"{shoe.shoe_id:<5} {shoe.brand:<15} {shoe.model:<20} {miles:<10} {status:<10}")


def display_goals(goals):
    """Display a list of training goals"""
    if not goals:
        print("No goals found.")
        return
    
    print(f"\n{'ID':<5} {'Type':<15} {'Progress':<20} {'Target Date':<12} {'Status':<10}")
    print("-" * 70)
    
    for goal in goals:
        progress = f"{goal.current_value:.1f}/{goal.target_value:.1f}"
        target = str(goal.target_date) if goal.target_date else "N/A"
        print(f"{goal.goal_id:<5} {goal.goal_type:<15} {progress:<20} {target:<12} {goal.status:<10}")


def runner_menu():
    """Runner management menu"""
    while True:
        print_menu("Runner Management", {
            '1': 'View all runners',
            '2': 'View runner details',
            '3': 'Add new runner',
            '4': 'Update runner',
            '5': 'Delete runner',
            '6': 'Search runners',
            '0': 'Back to main menu'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print_header("All Runners")
            runners = Runner.get_all()
            display_runners(runners)
        
        elif choice == '2':
            runner_id = int(input("Enter runner ID: "))
            runner = Runner.get_by_id(runner_id)
            if runner:
                print(f"\nRunner Details:")
                print(f"  Name: {runner.first_name} {runner.last_name}")
                print(f"  Email: {runner.email}")
                print(f"  DOB: {runner.date_of_birth}")
                print(f"  Gender: {runner.gender}")
                print(f"  Weight: {runner.weight_lbs} lbs")
                print(f"  Height: {runner.height_inches} inches")
                
                stats = Runner.get_statistics(runner_id)
                if stats:
                    print(f"\nRunning Statistics:")
                    print(f"  Total Runs: {stats['total_runs']}")
                    print(f"  Total Miles: {stats['total_miles']:.2f}")
                    print(f"  Average Pace: {stats['average_pace']:.2f} min/mile")
                    print(f"  Best Pace: {stats['best_pace']:.2f} min/mile")
                    print(f"  Longest Run: {stats['longest_run']:.2f} miles")
            else:
                print("Runner not found.")
        
        elif choice == '3':
            print("\nAdd New Runner")
            first_name = input("First name: ")
            last_name = input("Last name: ")
            email = input("Email: ")
            dob = input("Date of birth (YYYY-MM-DD) or press Enter to skip: ")
            gender = input("Gender (M/F/Other) [Other]: ") or 'Other'
            weight = input("Weight (lbs) or press Enter to skip: ")
            height = input("Height (inches) or press Enter to skip: ")
            
            Runner.create(
                first_name, last_name, email,
                date_of_birth=dob if dob else None,
                gender=gender,
                weight_lbs=float(weight) if weight else None,
                height_inches=int(height) if height else None
            )
        
        elif choice == '4':
            runner_id = int(input("Enter runner ID to update: "))
            print("Enter new values (press Enter to skip):")
            first_name = input("First name: ")
            last_name = input("Last name: ")
            email = input("Email: ")
            weight = input("Weight (lbs): ")
            
            updates = {}
            if first_name: updates['first_name'] = first_name
            if last_name: updates['last_name'] = last_name
            if email: updates['email'] = email
            if weight: updates['weight_lbs'] = float(weight)
            
            Runner.update(runner_id, **updates)
        
        elif choice == '5':
            runner_id = int(input("Enter runner ID to delete: "))
            confirm = input(f"Are you sure you want to delete runner {runner_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                Runner.delete(runner_id)
        
        elif choice == '6':
            name = input("Enter name to search: ")
            runners = Runner.search_by_name(name)
            display_runners(runners)
        
        elif choice == '0':
            break


def run_menu():
    """Run management menu"""
    while True:
        print_menu("Run Management", {
            '1': 'View all runs',
            '2': 'View runs by runner',
            '3': 'Add new run',
            '4': 'Update run',
            '5': 'Delete run',
            '6': 'View recent runs',
            '0': 'Back to main menu'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print_header("All Runs")
            runs = Run.get_all(limit=50)
            display_runs(runs)
        
        elif choice == '2':
            runner_id = int(input("Enter runner ID: "))
            runs = Run.get_by_runner(runner_id)
            print_header(f"Runs for Runner {runner_id}")
            display_runs(runs)
            
            # Show summary statistics
            stats = Run.get_summary_stats(runner_id)
            if stats and stats['total_runs'] > 0:
                print(f"\nSummary Statistics:")
                print(f"  Total Runs: {stats['total_runs']}")
                print(f"  Total Distance: {stats['total_distance']:.2f} miles")
                print(f"  Average Distance: {stats['avg_distance']:.2f} miles")
                print(f"  Average Pace: {stats['avg_pace']:.2f} min/mile")
                print(f"  Best Pace: {stats['best_pace']:.2f} min/mile")
                print(f"  Longest Run: {stats['longest_run']:.2f} miles")
        
        elif choice == '3':
            print("\nAdd New Run")
            runner_id = int(input("Runner ID: "))
            run_date = input("Run date (YYYY-MM-DD): ")
            distance = float(input("Distance (miles): "))
            duration = int(input("Duration (minutes): "))
            route_id = input("Route ID (or press Enter to skip): ")
            shoe_id = input("Shoe ID (or press Enter to skip): ")
            run_type = input("Run type [Easy/Tempo/Interval/Long/Race/Recovery]: ") or 'Easy'
            weather = input("Weather: ")
            temp = input("Temperature (F): ")
            notes = input("Notes: ")
            
            Run.create(
                runner_id, run_date, distance, duration,
                route_id=int(route_id) if route_id else None,
                shoe_id=int(shoe_id) if shoe_id else None,
                run_type=run_type,
                weather=weather if weather else None,
                temperature_f=int(temp) if temp else None,
                notes=notes if notes else None
            )
        
        elif choice == '4':
            run_id = int(input("Enter run ID to update: "))
            print("Enter new values (press Enter to skip):")
            distance = input("Distance (miles): ")
            duration = input("Duration (minutes): ")
            notes = input("Notes: ")
            
            updates = {}
            if distance: updates['distance_miles'] = float(distance)
            if duration: updates['duration_minutes'] = int(duration)
            if notes: updates['notes'] = notes
            
            Run.update(run_id, **updates)
        
        elif choice == '5':
            run_id = int(input("Enter run ID to delete: "))
            confirm = input(f"Are you sure you want to delete run {run_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                Run.delete(run_id)
        
        elif choice == '6':
            print_header("Recent Runs")
            recent = Run.get_recent_runs(limit=20)
            if recent:
                print(f"\n{'Runner':<20} {'Date':<12} {'Distance':<10} {'Pace':<8} {'Route':<20}")
                print("-" * 80)
                for run in recent:
                    pace = f"{run['pace_min_per_mile']:.2f}" if run['pace_min_per_mile'] else "N/A"
                    route = run['route_name'] if run['route_name'] else "No route"
                    print(f"{run['runner_name']:<20} {str(run['run_date']):<12} {run['distance_miles']:.2f} mi   {pace:<8} {route:<20}")
            else:
                print("No recent runs found.")
        
        elif choice == '0':
            break


def route_menu():
    """Route management menu"""
    while True:
        print_menu("Route Management", {
            '1': 'View all routes',
            '2': 'View routes by runner',
            '3': 'Add new route',
            '4': 'Update route',
            '5': 'Delete route',
            '0': 'Back to main menu'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print_header("All Routes")
            routes = Route.get_all()
            display_routes(routes)
        
        elif choice == '2':
            runner_id = int(input("Enter runner ID: "))
            routes = Route.get_by_runner(runner_id)
            print_header(f"Routes for Runner {runner_id}")
            display_routes(routes)
        
        elif choice == '3':
            print("\nAdd New Route")
            runner_id = int(input("Runner ID: "))
            route_name = input("Route name: ")
            distance = float(input("Distance (miles): "))
            elevation = int(input("Elevation gain (feet): ") or 0)
            surface = input("Surface type [Road/Trail/Track/Treadmill/Mixed]: ") or 'Road'
            description = input("Description: ")
            start_location = input("Start location: ")
            
            Route.create(
                runner_id, route_name, distance, elevation,
                surface_type=surface,
                description=description if description else None,
                start_location=start_location if start_location else None
            )
        
        elif choice == '4':
            route_id = int(input("Enter route ID to update: "))
            print("Enter new values (press Enter to skip):")
            route_name = input("Route name: ")
            distance = input("Distance (miles): ")
            description = input("Description: ")
            
            updates = {}
            if route_name: updates['route_name'] = route_name
            if distance: updates['distance_miles'] = float(distance)
            if description: updates['description'] = description
            
            Route.update(route_id, **updates)
        
        elif choice == '5':
            route_id = int(input("Enter route ID to delete: "))
            confirm = input(f"Are you sure you want to delete route {route_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                Route.delete(route_id)
        
        elif choice == '0':
            break


def shoe_menu():
    """Shoe management menu"""
    while True:
        print_menu("Shoe Management", {
            '1': 'View all shoes',
            '2': 'View shoes by runner',
            '3': 'Add new shoe',
            '4': 'Retire shoe',
            '5': 'Delete shoe',
            '6': 'Check shoes needing replacement',
            '0': 'Back to main menu'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print_header("All Running Shoes")
            shoes = RunningShoe.get_all()
            display_shoes(shoes)
        
        elif choice == '2':
            runner_id = int(input("Enter runner ID: "))
            active = input("Active shoes only? (yes/no): ").lower() == 'yes'
            shoes = RunningShoe.get_by_runner(runner_id, active_only=active)
            print_header(f"Shoes for Runner {runner_id}")
            display_shoes(shoes)
        
        elif choice == '3':
            print("\nAdd New Shoe")
            runner_id = int(input("Runner ID: "))
            brand = input("Brand: ")
            model = input("Model: ")
            purchase_date = input("Purchase date (YYYY-MM-DD): ")
            notes = input("Notes: ")
            
            RunningShoe.create(
                runner_id, brand, model, purchase_date,
                notes=notes if notes else None
            )
        
        elif choice == '4':
            shoe_id = int(input("Enter shoe ID to retire: "))
            RunningShoe.retire_shoe(shoe_id)
        
        elif choice == '5':
            shoe_id = int(input("Enter shoe ID to delete: "))
            confirm = input(f"Are you sure you want to delete shoe {shoe_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                RunningShoe.delete(shoe_id)
        
        elif choice == '6':
            runner_id = int(input("Enter runner ID: "))
            threshold = int(input("Mileage threshold [400]: ") or 400)
            shoes = RunningShoe.get_shoes_needing_replacement(runner_id, threshold)
            print_header(f"Shoes with {threshold}+ Miles")
            display_shoes(shoes)
        
        elif choice == '0':
            break


def goal_menu():
    """Training goal management menu"""
    while True:
        print_menu("Training Goal Management", {
            '1': 'View all goals',
            '2': 'View goals by runner',
            '3': 'Add new goal',
            '4': 'Update goal progress',
            '5': 'Complete goal',
            '6': 'Delete goal',
            '0': 'Back to main menu'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print_header("All Training Goals")
            goals = TrainingGoal.get_all()
            display_goals(goals)
        
        elif choice == '2':
            runner_id = int(input("Enter runner ID: "))
            active = input("Active goals only? (yes/no): ").lower() == 'yes'
            goals = TrainingGoal.get_by_runner(runner_id, active_only=active)
            print_header(f"Goals for Runner {runner_id}")
            display_goals(goals)
        
        elif choice == '3':
            print("\nAdd New Training Goal")
            runner_id = int(input("Runner ID: "))
            goal_type = input("Goal type [Distance/Time/Pace/Race/Weight/Weekly_Mileage]: ")
            target_value = float(input("Target value: "))
            target_date = input("Target date (YYYY-MM-DD) or press Enter to skip: ")
            description = input("Description: ")
            
            TrainingGoal.create(
                runner_id, goal_type, target_value,
                target_date=target_date if target_date else None,
                description=description if description else None
            )
        
        elif choice == '4':
            goal_id = int(input("Enter goal ID: "))
            current_value = float(input("Current progress value: "))
            TrainingGoal.update_progress(goal_id, current_value)
        
        elif choice == '5':
            goal_id = int(input("Enter goal ID to complete: "))
            TrainingGoal.complete_goal(goal_id)
        
        elif choice == '6':
            goal_id = int(input("Enter goal ID to delete: "))
            confirm = input(f"Are you sure you want to delete goal {goal_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                TrainingGoal.delete(goal_id)
        
        elif choice == '0':
            break


def main():
    """Main application menu"""
    print_header("Running Tracker - Console Application")
    print("\nWelcome to Running Tracker!")
    print("Track your runs, routes, shoes, and training goals.")
    
    while True:
        print_menu("Main Menu", {
            '1': 'Runner Management',
            '2': 'Run Management',
            '3': 'Route Management',
            '4': 'Shoe Management',
            '5': 'Training Goal Management',
            '0': 'Exit'
        })
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            runner_menu()
        elif choice == '2':
            run_menu()
        elif choice == '3':
            route_menu()
        elif choice == '4':
            shoe_menu()
        elif choice == '5':
            goal_menu()
        elif choice == '0':
            print("\nThank you for using Running Tracker!")
            print("Keep running! 🏃‍♂️💨")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting Running Tracker. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
