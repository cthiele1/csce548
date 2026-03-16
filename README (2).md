# Running Tracker — CSCE 548

A full n-tier web application for tracking runs, routes, shoes, and training goals. Built with a MySQL database, Python/Flask REST API, and a browser-based frontend. All layers run locally.

---

## Architecture

```
index.html              ← Client Layer (Browser)
        ↓  HTTP/REST
app.py                  ← Service Layer (Flask API, localhost:5000)
        ↓
business_layer.py       ← Business Layer (validation & rules)
        ↓
data_layer.py           ← Data Layer (SQL queries)
        ↓
MySQL                   ← running_tracker database
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Run the Flask API |
| pip | Latest | Install Python packages |
| MySQL | 8.0+ | Database server |
| Any browser | Modern | Run the frontend |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/cthiele1/csce548.git
cd csce548
```

### 2. Install Python dependencies

```powershell
pip install flask flask-cors mysql-connector-python
```

### 3. Set up the database

Start MySQL and run your Project 1 SQL script to create the `running_tracker` database and all tables.

### 4. Set environment variables (PowerShell)

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_NAME="running_tracker"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
```

### 5. Start the API server

```powershell
python app.py
```

The API starts at `http://localhost:5000`

### 6. Open the frontend

Double-click `index.html` in File Explorer, or run:

```powershell
start index.html
```

### 7. Verify it works

- Green dot in the top-right of the app = API is reachable
- All 5 tables (Runners, Runs, Routes, Shoes, Goals) load data automatically

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/runners` | Get all runners |
| GET | `/runners/<id>` | Get one runner |
| POST | `/runners` | Create runner |
| PUT | `/runners/<id>` | Update runner |
| DELETE | `/runners/<id>` | Delete runner |
| GET | `/runs` | Get all runs |
| GET | `/runs?runner_id=X` | Get runs by runner |
| GET | `/runs/<id>` | Get one run |
| POST | `/runs` | Log a run |
| PUT | `/runs/<id>` | Update run |
| DELETE | `/runs/<id>` | Delete run |
| GET | `/routes` | Get all routes |
| GET | `/routes/<id>` | Get one route |
| POST | `/routes` | Create route |
| PUT | `/routes/<id>` | Update route |
| DELETE | `/routes/<id>` | Delete route |
| GET | `/shoes` | Get all shoes |
| GET | `/shoes/<id>` | Get one shoe |
| POST | `/shoes` | Add shoe |
| PUT | `/shoes/<id>` | Update shoe |
| DELETE | `/shoes/<id>` | Delete shoe |
| GET | `/goals` | Get all goals |
| GET | `/goals?runner_id=X` | Get goals by runner |
| GET | `/goals/<id>` | Get one goal |
| POST | `/goals` | Create goal |
| PUT | `/goals/<id>` | Update goal |
| DELETE | `/goals/<id>` | Delete goal |
| GET | `/health` | Health check |

---

## Project Structure

```
csce548/
├── app.py                  # Flask REST API (service layer)
├── client.py               # Console test client
├── index.html              # Web frontend (client layer)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── deployment.md           # Full deployment instructions
├── data/
│   ├── db_connection.py    # MySQL connection
│   └── data_layer.py       # CRUD SQL operations
└── business/
    └── business_layer.py   # Business rules & validation
```

---

## Database Tables

| Table | Description |
|-------|-------------|
| `runners` | Runner profiles — name, email, weight, height |
| `runs` | Individual run records — distance, duration, pace, type |
| `routes` | Saved routes — distance, elevation, surface type |
| `running_shoes` | Shoe tracking with mileage and retirement status |
| `training_goals` | Goals with target values and progress tracking |

---

## Business Rules

- Email validation required on all runner records
- Run pace is auto-calculated by MySQL (generated column) — do not submit manually
- Heart rate above 220 bpm is rejected
- Shoes with 300+ miles trigger a replacement warning
- Goals cannot have a past target date
- Goals auto-complete when current value reaches target value
