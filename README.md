# CSCE 548 - Project 2: Running Tracker API

A three-layer architecture built with Python and Flask, connecting to the
MySQL `running_tracker` database from Project 1.

## Architecture

```
client.py  (Console Front End)
    ↓  HTTP requests
app.py  (Service Layer - Flask REST API)
    ↓  function calls
business/business_layer.py  (Business Layer - validation & rules)
    ↓  function calls
data/data_layer.py  (Data Layer - SQL queries)
    ↓  MySQL connection
running_tracker database
```

## Project Structure

```
project2/
├── app.py                    # Flask service layer (REST API)
├── client.py                 # Console front-end test client
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment config
├── data/
│   ├── db_connection.py      # Database connection (reads env vars)
│   └── data_layer.py         # All CRUD SQL operations
└── business/
    └── business_layer.py     # Business rules + validation
```

## API Endpoints

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | /runners           | Get all runners          |
| GET    | /runners/<id>      | Get one runner           |
| POST   | /runners           | Add a runner             |
| PUT    | /runners/<id>      | Update a runner          |
| DELETE | /runners/<id>      | Delete a runner          |
| GET    | /runs              | Get all runs             |
| GET    | /runs?runner_id=X  | Get runs for a runner    |
| GET    | /runs/<id>         | Get one run              |
| POST   | /runs              | Log a run                |
| PUT    | /runs/<id>         | Update a run             |
| DELETE | /runs/<id>         | Delete a run             |
| GET    | /routes            | Get all routes           |
| GET    | /routes/<id>       | Get one route            |
| POST   | /routes            | Add a route              |
| PUT    | /routes/<id>       | Update a route           |
| DELETE | /routes/<id>       | Delete a route           |
| GET    | /shoes             | Get all shoes            |
| GET    | /shoes/<id>        | Get one shoe             |
| POST   | /shoes             | Add a shoe               |
| PUT    | /shoes/<id>        | Update a shoe            |
| DELETE | /shoes/<id>        | Delete a shoe            |
| GET    | /goals             | Get all goals            |
| GET    | /goals?runner_id=X | Get goals for a runner   |
| GET    | /goals/<id>        | Get one goal             |
| POST   | /goals             | Add a goal               |
| PUT    | /goals/<id>        | Update a goal            |
| DELETE | /goals/<id>        | Delete a goal            |
| GET    | /health            | Health check             |

## Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (or create a .env file)
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=running_tracker
export DB_USER=root
export DB_PASSWORD=yourpassword

# 3. Start the Flask server
python app.py

# 4. In a new terminal, run the test client
python client.py
```

## Deploying to Railway

1. **Push to GitHub**: Commit all files and push to your GitHub repo.

2. **Create Railway Project**:
   - Go to https://railway.app and sign in
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `csce548` repository

3. **Add MySQL Database** (if not already hosted elsewhere):
   - In your Railway project, click "New" → "Database" → "MySQL"
   - Railway will provision a MySQL instance automatically

4. **Set Environment Variables**:
   - In Railway Dashboard → your service → "Variables"
   - Add the following:
     ```
     DB_HOST     = <from Railway MySQL plugin - use MYSQLHOST variable>
     DB_PORT     = 3306
     DB_NAME     = running_tracker
     DB_USER     = <from Railway MySQL plugin - use MYSQLUSER>
     DB_PASSWORD = <from Railway MySQL plugin - use MYSQLPASSWORD>
     ```
   - Tip: Railway's MySQL plugin auto-exposes `$MYSQLHOST`, `$MYSQLUSER`,
     `$MYSQLPASSWORD`, `$MYSQLPORT`, `$MYSQLDATABASE` — you can reference
     these directly in the Variables tab.

5. **Deploy**:
   - Railway will detect the `Procfile` and run `python app.py`
   - Your app will be live at `https://<your-app-name>.up.railway.app`

6. **Test the deployment**:
   ```bash
   BASE_URL=https://your-app.up.railway.app python client.py
   ```

## Business Rules Enforced

- Runners require a valid email address with '@'
- Run distance and duration must be positive numbers
- Pace is auto-calculated if not provided (`duration / distance`)
- Heart rate above 220 bpm is rejected
- Shoes with 300+ miles trigger a replacement warning
- Training goals cannot have a past target date
- Goals are auto-marked "completed" when current_value >= target_value
- Goal progress percentage is calculated on retrieval
