# Running Tracker Database Project

A comprehensive running tracker application with MySQL database backend and Python console interface. Track your runs, routes, shoes, training goals, and analyze your performance over time.

## Project Overview

This project demonstrates a complete database application with:
- **5 normalized database tables** with proper relationships
- **60+ rows of test data** across all tables
- **Full CRUD operations** for all entities
- **Console-based user interface** for easy interaction
- **Advanced features** like statistics, views, and data validation

## Database Schema

### Tables

1. **runners** - Store runner profiles
   - Fields: runner_id, first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches
   - Primary Key: runner_id

2. **running_shoes** - Track running shoe inventory and mileage
   - Fields: shoe_id, runner_id, brand, model, purchase_date, total_miles, retired, notes
   - Primary Key: shoe_id
   - Foreign Key: runner_id → runners(runner_id)

3. **routes** - Store favorite running routes
   - Fields: route_id, runner_id, route_name, distance_miles, elevation_gain_ft, surface_type, description, start_location
   - Primary Key: route_id
   - Foreign Key: runner_id → runners(runner_id)

4. **runs** - Main table storing individual run records
   - Fields: run_id, runner_id, route_id, shoe_id, run_date, distance_miles, duration_minutes, pace_min_per_mile (calculated), average_heart_rate, calories_burned, weather, temperature_f, run_type, notes
   - Primary Key: run_id
   - Foreign Keys: runner_id → runners(runner_id), route_id → routes(route_id), shoe_id → running_shoes(shoe_id)
   - Computed Column: pace_min_per_mile (duration/distance)

5. **training_goals** - Track training goals and progress
   - Fields: goal_id, runner_id, goal_type, target_value, current_value, target_date, status, description
   - Primary Key: goal_id
   - Foreign Key: runner_id → runners(runner_id)

### Views

- **runner_statistics** - Aggregated running statistics per runner
- **recent_runs** - Most recent 20 runs across all runners with joined data

## Project Structure

```
running-tracker/
├── 01_create_database.sql      # Database schema creation script
├── 02_insert_test_data.sql     # Test data insertion (60+ rows)
├── config.py                   # Database configuration
├── database.py                 # Database connection utilities
├── models/                     # Data Access Layer
│   ├── __init__.py
│   ├── runner.py              # Runner CRUD operations
│   ├── run.py                 # Run CRUD operations
│   ├── route.py               # Route CRUD operations
│   ├── shoe.py                # Shoe CRUD operations
│   └── goal.py                # Training Goal CRUD operations
├── main.py                     # Console application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

- MySQL Server 8.0+ or MariaDB 10.5+
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone or download this project**
   ```bash
   cd running-tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection**
   - Edit `config.py`
   - Update the MySQL password and connection details:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'YOUR_MYSQL_PASSWORD',  # Change this!
       'database': 'running_tracker',
       'raise_on_warnings': True
   }
   ```

4. **Create the database and schema**
   ```bash
   mysql -u root -p < 01_create_database.sql
   ```

5. **Load test data**
   ```bash
   mysql -u root -p < 02_insert_test_data.sql
   ```

6. **Verify data loaded successfully**
   ```bash
   mysql -u root -p running_tracker -e "SELECT COUNT(*) FROM runs;"
   ```
   Should show 60 rows.

7. **Run the application**
   ```bash
   python main.py
   ```

## CRUD Operations

All models implement complete CRUD (Create, Read, Update, Delete) operations:

### Runner Model (`models/runner.py`)
- `create()` - Add new runner
- `get_by_id()` - Retrieve runner by ID
- `get_all()` - Get all runners
- `search_by_name()` - Search runners by name
- `update()` - Update runner information
- `delete()` - Delete runner
- `get_statistics()` - Get running statistics

### Run Model (`models/run.py`)
- `create()` - Log new run
- `get_by_id()` - Retrieve run by ID
- `get_all()` - Get all runs
- `get_by_runner()` - Get runs for specific runner
- `get_by_date_range()` - Get runs in date range
- `update()` - Update run details
- `delete()` - Delete run
- `get_recent_runs()` - Get recent runs view
- `get_summary_stats()` - Get summary statistics

### Route Model (`models/route.py`)
- `create()` - Add new route
- `get_by_id()` - Retrieve route by ID
- `get_all()` - Get all routes
- `get_by_runner()` - Get routes for specific runner
- `search_by_name()` - Search routes by name
- `update()` - Update route details
- `delete()` - Delete route

### Running Shoe Model (`models/shoe.py`)
- `create()` - Add new shoe
- `get_by_id()` - Retrieve shoe by ID
- `get_all()` - Get all shoes
- `get_by_runner()` - Get shoes for specific runner
- `update()` - Update shoe details
- `retire_shoe()` - Mark shoe as retired
- `delete()` - Delete shoe
- `get_shoes_needing_replacement()` - Find high-mileage shoes

### Training Goal Model (`models/goal.py`)
- `create()` - Create new goal
- `get_by_id()` - Retrieve goal by ID
- `get_all()` - Get all goals
- `get_by_runner()` - Get goals for specific runner
- `update()` - Update goal details
- `update_progress()` - Update progress value
- `complete_goal()` - Mark goal as completed
- `abandon_goal()` - Mark goal as abandoned
- `delete()` - Delete goal

## Using the Console Application

The application provides an intuitive menu-driven interface:

```
Main Menu
----------------------------------------
  1. Runner Management
  2. Run Management
  3. Route Management
  4. Shoe Management
  5. Training Goal Management
  0. Exit
```

### Example Workflows

**Viewing Your Running Statistics:**
1. Select "1" (Runner Management)
2. Select "2" (View runner details)
3. Enter your runner ID
4. View total runs, miles, pace statistics

**Logging a New Run:**
1. Select "2" (Run Management)
2. Select "3" (Add new run)
3. Enter run details (date, distance, time, etc.)
4. System automatically calculates pace

**Tracking Shoe Mileage:**
1. Select "4" (Shoe Management)
2. Select "6" (Check shoes needing replacement)
3. View shoes over mileage threshold

## Test Data

The database includes realistic test data:
- **5 runners** with different profiles
- **10 pairs of running shoes** across different brands
- **12 running routes** with varied terrain
- **60 run records** from January-February 2025
- **8 training goals** with different objectives

## Database Features

### Indexes
- Email lookup on runners
- Runner-date composite index on runs
- Route and shoe lookups optimized

### Constraints
- Foreign key relationships with CASCADE delete
- Email uniqueness on runners
- NOT NULL constraints on critical fields

### Generated Columns
- Pace automatically calculated from distance/duration

### Views
- Pre-aggregated statistics for performance
- Recent runs with joined data for reports

## Screenshots Required for Assignment

1. **Database Diagram** - Use MySQL Workbench to generate ERD
2. **Row Count Verification** - Run `SELECT COUNT(*) FROM runs;` (should show 60+)
3. **Console Application Running** - Screenshot of main menu
4. **Data Retrieval** - Screenshot showing runner statistics or run list

## Extension Ideas

- Add web interface using Flask
- Implement data visualization with matplotlib
- Add GPS/GPX file import
- Create mobile app interface
- Add weather API integration
- Implement training plan generator

## Technologies Used

- **Database**: MySQL 8.0
- **Language**: Python 3.8+
- **Database Connector**: mysql-connector-python
- **Architecture**: MVC pattern with Data Access Layer

## License

This is an educational project created for database course requirements.

## Author

Created for CS Database Course - Running Tracker Project
