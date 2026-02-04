# Running Tracker - Quick Start Guide

## 🏃‍♂️ Get Running in 5 Minutes!

### Step 1: Setup MySQL Database (2 minutes)

```bash
# Navigate to the project directory
cd running-tracker

# Create the database and schema
mysql -u root -p < 01_create_database.sql
# Enter your MySQL password when prompted

# Load the test data (60 runs + more!)
mysql -u root -p < 02_insert_test_data.sql
# Enter your MySQL password when prompted
```

### Step 2: Configure Python (1 minute)

```bash
# Copy the config template
cp config.template.py config.py

# Edit config.py and change YOUR_PASSWORD_HERE to your actual MySQL password
# You can use any text editor:
nano config.py
# or
vim config.py
# or open it in VS Code/your preferred editor

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Test Everything Works (1 minute)

```bash
# Run the automated tests
python test_crud.py

# You should see:
# ✓ Runner CRUD test completed successfully!
# ✓ Run CRUD test completed successfully!
# ✓ Statistics test completed successfully!
# ALL TESTS COMPLETED SUCCESSFULLY! ✓
```

### Step 4: Run the Application (1 minute)

```bash
python main.py
```

You'll see the main menu:
```
============================================================
  Running Tracker - Console Application
============================================================

Welcome to Running Tracker!
Track your runs, routes, shoes, and training goals.

Main Menu
----------------------------------------
  1. Runner Management
  2. Run Management
  3. Route Management
  4. Shoe Management
  5. Training Goal Management
  0. Exit
```

---

## 📸 Taking Screenshots for Assignment

### Screenshot 1: Database Diagram
1. Open MySQL Workbench
2. Connect to your database
3. Database → Reverse Engineer
4. Select `running_tracker` database
5. Screenshot the diagram showing all 5 tables

### Screenshot 2: 50+ Rows Verification
```bash
mysql -u root -p running_tracker

# In MySQL prompt:
SELECT COUNT(*) as total_runs FROM runs;

# Should show: 60
# Take screenshot!
```

### Screenshot 3: Console Application
```bash
python main.py

# Take screenshot of the main menu
```

### Screenshot 4: Data Retrieval
```bash
# From main menu:
1  # Runner Management
1  # View all runners

# Shows list of runners with statistics
# Take screenshot!

# Or try:
2  # Run Management
1  # View all runs
# Take screenshot of run data!
```

---

## 🎯 Quick Demo Commands

### See All Your Data
```bash
# Connect to MySQL
mysql -u root -p running_tracker

# View everything at once
source 03_verification_queries.sql
```

### Try These in the Application

**View Runner Stats:**
- Main Menu → 1 (Runner Management)
- Option 2 (View runner details)
- Enter runner ID: 1
- See total miles, average pace, etc.

**View Recent Runs:**
- Main Menu → 2 (Run Management)
- Option 6 (View recent runs)
- See last 20 runs across all runners

**Add a New Run:**
- Main Menu → 2 (Run Management)
- Option 3 (Add new run)
- Follow the prompts!

---

## 🐛 Troubleshooting

**"Access denied for user"**
- Check your password in `config.py`
- Make sure MySQL server is running

**"No module named 'mysql'"**
- Run: `pip install -r requirements.txt`

**"Table doesn't exist"**
- Make sure you ran: `mysql -u root -p < 01_create_database.sql`

**No data showing**
- Make sure you ran: `mysql -u root -p < 02_insert_test_data.sql`

---

## ✅ Assignment Checklist

- [ ] Database created (5 tables)
- [ ] Test data loaded (60+ runs)
- [ ] Screenshot: Database diagram
- [ ] Screenshot: Row count showing 60
- [ ] Screenshot: Console main menu
- [ ] Screenshot: Data retrieval
- [ ] Code pushed to GitHub
- [ ] README.md in repository

---

## 🚀 GitHub Setup

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Running Tracker database project"

# Add your GitHub remote (create repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/running-tracker.git

# Push to GitHub
git push -u origin main
```

**Note:** The `.gitignore` file will prevent your `config.py` (with password) from being committed!

---

## 📊 What's Included

- **5 Database Tables:** runners, running_shoes, routes, runs, training_goals
- **95 Total Rows:** Well over the 50 minimum!
- **All CRUD Operations:** Create, Read, Update, Delete for every table
- **Console Application:** Easy-to-use menu interface
- **Advanced Features:** Statistics, calculated fields, views, search
- **Professional Code:** MVC pattern, error handling, validation

---

## 🎓 What You've Built

This is a production-quality application that demonstrates:
- Relational database design
- Foreign key relationships
- Data normalization
- Object-oriented programming
- Data access layer pattern
- User interface design
- SQL query optimization
- Error handling and validation

**Great work!** This project shows real-world database application development skills. 🌟

---

Need help? Check:
- `README.md` for detailed setup
- `PROJECT_DOCS.md` for assignment requirements
- `03_verification_queries.sql` for sample queries
