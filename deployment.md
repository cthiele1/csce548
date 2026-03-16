# Running Tracker — Deployment Document
### CSCE 548 — Project 4 | Connor Thiele
### GitHub: https://github.com/cthiele1/csce548

---

## 1. Project Overview

The Running Tracker is a full n-tier web application demonstrating layered software architecture. It consists of four layers communicating from top to bottom:

```
index.html              ← Client Layer (Browser)
        ↓  HTTP/REST
app.py                  ← Service Layer (Flask API, localhost:5000)
        ↓
business_layer.py       ← Business Layer (validation & business rules)
        ↓
data_layer.py           ← Data Layer (SQL operations)
        ↓
MySQL                   ← running_tracker database
```

The application tracks five entities: Runners, Runs, Routes, Running Shoes, and Training Goals. All layers run locally on the developer's machine.

---

## 2. Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Runs the Flask API |
| pip | Latest | Installs Python packages |
| MySQL | 8.0+ | Database server |
| MySQL Workbench | Any | Visual DB access (optional) |
| Git | Any | Clone the repository |
| Web Browser | Chrome / Firefox / Edge | Runs the frontend |

---

## 3. Getting the Code

**Option A — Clone with Git:**

```bash
git clone https://github.com/cthiele1/csce548.git
cd csce548
```

**Option B — Download ZIP:**

1. Go to https://github.com/cthiele1/csce548
2. Click the green **Code** button → **Download ZIP**
3. Extract the ZIP to a folder of your choice
4. Open PowerShell in that folder

---

## 4. Database Setup

### 4.1 Start MySQL

Make sure MySQL Server is running. On Windows, open **Services** and start **MySQL80**.

### 4.2 Create the database and tables

Open MySQL Workbench or the MySQL command line and run:

```sql
CREATE DATABASE IF NOT EXISTS running_tracker;
USE running_tracker;
```

Then execute the Project 1 SQL script to create all five tables: `runners`, `runs`, `routes`, `running_shoes`, `training_goals`.

### 4.3 Verify tables exist

```sql
USE running_tracker;
SHOW TABLES;
```

Expected output:

```
+---------------------------+
| Tables_in_running_tracker |
+---------------------------+
| runners                   |
| running_shoes             |
| routes                    |
| runs                      |
| training_goals            |
+---------------------------+
```

---

## 5. Back End Setup (Service Layer)

### 5.1 Install Python dependencies

Open PowerShell in the project folder:

```powershell
pip install flask flask-cors mysql-connector-python
```

### 5.2 Set environment variables

In PowerShell, set these for the current session:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_NAME="running_tracker"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password_here"
```

> Replace `your_password_here` with your actual MySQL root password.

### 5.3 Start the Flask server

```powershell
python app.py
```

Expected output:

```
* Running on http://0.0.0.0:5000
* Debug mode: off
```

### 5.4 Verify the API is running

Open a browser and navigate to:

```
http://localhost:5000/health
```

Expected response:

```json
{"service": "Running Tracker API", "status": "ok"}
```

---

## 6. Front End Setup (Client Layer)

The frontend is a single HTML file — no build step, no install required.

### 6.1 Open the frontend

Open a **second** PowerShell window and run:

```powershell
start index.html
```

Or simply **double-click `index.html`** in File Explorer.

### 6.2 Verify it connects

- The **API URL** field in the top-right header should show `http://localhost:5000`
- A **green dot** next to the URL confirms the API is reachable
- A gray or red dot means the Flask server is not running — check Step 5
- All 5 table pages (Runners, Runs, Routes, Shoes, Goals) should load data automatically

---

## 7. Using the Application

### 7.1 Reading data (GET all / GET one)

- Click any table in the left sidebar to view all records
- **Runs** and **Goals** have a **By Runner** tab to filter records by Runner ID
- Stats (total count, miles, hours, etc.) display above each table

### 7.2 Inserting records (POST)

1. Click the **+ Add** button at the top of any page
2. Fill in the required fields (marked with `*`)
3. Click **Save** — a green confirmation message appears
4. The table refreshes automatically showing the new record

### 7.3 Updating records (PUT)

1. Click the **Edit** button on any row
2. The form opens pre-filled with that record's current values
3. Make changes and click **Save**
4. A green confirmation appears and the table refreshes

### 7.4 Verifying changes in MySQL

After inserting or updating, confirm in MySQL Workbench or command line:

```sql
USE running_tracker;
SELECT * FROM runners ORDER BY runner_id DESC LIMIT 5;
```

---

## 8. Project File Structure

| File / Folder | Purpose |
|---------------|---------|
| `app.py` | Flask REST API — service layer, all endpoints |
| `index.html` | Browser frontend — insert, update, and read UI |
| `client.py` | Console test client — automated CRUD tests |
| `requirements.txt` | Python package list |
| `README.md` | GitHub readme |
| `deployment.md` | This document |
| `data/db_connection.py` | MySQL connection using environment variables |
| `data/data_layer.py` | All SQL CRUD operations for all 5 tables |
| `business/business_layer.py` | Business rules and input validation |

---

## 9. API Endpoints

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
| GET | `/health` | API health check |

---

## 10. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Red/gray dot in frontend | Flask not running | Run `python app.py` in PowerShell |
| CORS error in browser console | `flask-cors` not installed | `pip install flask-cors` and restart Flask |
| 500 error on POST /runners | Duplicate email in database | Use a unique email address |
| 500 error on POST /runs | `pace_min_per_mile` is a generated column | Do not pass pace — it is auto-calculated by MySQL |
| DB connection error | Wrong credentials or MySQL not started | Check `$env:DB_*` variables and MySQL service status |
| Tables show no data | Database is empty | Re-run the Project 1 SQL seed script |
| `export` not recognized | Running on Windows | Use `$env:VAR="value"` instead of `export VAR=value` |

---

## 11. How to Confirm Setup Succeeded

- [ ] `http://localhost:5000/health` returns `{"status": "ok"}`
- [ ] Green dot is visible in the top-right of `index.html`
- [ ] All 5 table pages load data without errors
- [ ] Clicking **+ Add Runner** and submitting creates a new row in the table and in MySQL
- [ ] Clicking **Edit** on any row pre-fills the form with that record's data
- [ ] Saving an edit updates the record and the table refreshes
- [ ] Running `python client.py` shows all CRUD tests passing with ✓ checkmarks
