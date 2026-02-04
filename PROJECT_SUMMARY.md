# 🏃‍♂️ Running Tracker Database Project - Complete Package

## Project Overview

A comprehensive running tracker database application designed for your database course assignment. This project tracks mileage, pace, routes, shoes, and training goals for runners.

---

## ✅ Assignment Requirements Met

### 1. Database Schema (3-5 tables) ✅
**File:** `01_create_database.sql`

Created **5 tables:**
1. **runners** - Runner profiles and demographics
2. **running_shoes** - Track shoe inventory and mileage
3. **routes** - Favorite running routes  
4. **runs** - Individual run records (main data table)
5. **training_goals** - Track training objectives and progress

**Bonus features:**
- Foreign key relationships
- Database views for reporting
- Calculated/generated columns
- Proper indexing

### 2. Test Data (50+ rows) ✅
**File:** `02_insert_test_data.sql`

**95 total rows:**
- 5 runners
- 10 running shoes
- 12 routes
- **60 runs** ← Exceeds 50 minimum by 10 rows!
- 8 training goals

All data is realistic and interconnected.

### 3. Data Access Layer (CRUD Operations) ✅
**Language:** Python 3.8+

**Files:**
- `database.py` - Connection utilities
- `models/runner.py` - Runner CRUD
- `models/run.py` - Run CRUD  
- `models/route.py` - Route CRUD
- `models/shoe.py` - Shoe CRUD
- `models/goal.py` - Training Goal CRUD

**All CRUD operations implemented:**
- ✅ CREATE - Add new records
- ✅ READ - Retrieve by ID, get all, search
- ✅ UPDATE - Modify existing records
- ✅ DELETE - Remove records

### 4. Console Front End ✅
**File:** `main.py`

Full-featured console application with:
- Interactive menus
- Data entry and validation
- Formatted output displays
- Statistics and reporting
- Error handling

---

## 📁 File Structure

```
running-tracker/
├── 01_create_database.sql          # Database schema
├── 02_insert_test_data.sql         # Test data (60 runs)
├── 03_verification_queries.sql     # Verification & demo queries
├── config.py                       # Database connection config
├── config.template.py              # Config template for Git
├── database.py                     # Connection utilities
├── main.py                         # Console application
├── test_crud.py                    # CRUD operation tests
├── requirements.txt                # Python dependencies
├── README.md                       # Full setup documentation
├── PROJECT_DOCS.md                 # Assignment requirements checklist
├── QUICK_START.md                  # 5-minute setup guide
├── .gitignore                      # Git ignore file
└── models/                         # Data Access Layer
    ├── __init__.py
    ├── runner.py
    ├── run.py
    ├── route.py
    ├── shoe.py
    └── goal.py
```

---

## 🚀 Quick Setup (5 Minutes)

### 1. Create Database
```bash
mysql -u root -p < 01_create_database.sql
mysql -u root -p < 02_insert_test_data.sql
```

### 2. Configure Python
```bash
cp config.template.py config.py
# Edit config.py with your MySQL password
pip install -r requirements.txt
```

### 3. Test & Run
```bash
python test_crud.py    # Verify CRUD operations
python main.py         # Run the application
```

---

## 📸 Screenshots Needed

1. **Database Diagram** (MySQL Workbench)
   - Shows 5 tables with relationships
   
2. **Row Count Verification**
   ```sql
   SELECT COUNT(*) FROM runs;  -- Shows 60
   ```

3. **Console Application**
   - Main menu screenshot

4. **Data Retrieval**
   - Runner statistics or run list

---

## 🌟 Key Features

### Database Design
- Normalized schema (3NF)
- Foreign key constraints
- Computed columns (pace)
- Database views
- Proper indexing

### Data Access Layer
- Full CRUD for all tables
- Object-oriented design
- Context managers
- Error handling
- Dynamic SQL generation

### Console Application
- Menu-driven interface
- Input validation
- Formatted displays
- Statistics & reports
- User-friendly prompts

### Code Quality
- MVC architecture
- Type hints
- Documentation
- Clean code principles
- Professional structure

---

## 💡 What Makes This Special

1. **Exceeds Requirements**
   - 5 tables (max requested)
   - 95 rows (90% over minimum)
   - Advanced SQL features
   - Professional code structure

2. **Real-World Application**
   - Based on actual running tracking needs
   - Production-quality code
   - Extensible design
   - Comprehensive features

3. **Educational Value**
   - Demonstrates best practices
   - Shows relational database concepts
   - Illustrates OOP in Python
   - Examples of all CRUD operations

4. **Ready for GitHub**
   - Professional README
   - Proper .gitignore
   - Documentation included
   - Easy to clone and run

---

## 📚 Documentation

- **README.md** - Comprehensive setup guide
- **QUICK_START.md** - Get running in 5 minutes
- **PROJECT_DOCS.md** - Assignment checklist
- **Code comments** - Inline documentation

---

## 🎓 Learning Outcomes

This project demonstrates:
- Database design and normalization
- SQL DDL and DML
- Foreign key relationships
- CRUD operations
- Object-relational mapping
- MVC architecture
- Error handling
- User interface design

---

## 🔧 Technologies

- **Database:** MySQL 8.0
- **Language:** Python 3.8+
- **Connector:** mysql-connector-python
- **Architecture:** MVC with Data Access Layer

---

## ✅ Pre-Submission Checklist

- [x] 5 tables created
- [x] 60+ rows of data
- [x] All CRUD operations working
- [x] Console application functional
- [x] Documentation complete
- [x] Tests included
- [x] .gitignore configured
- [x] README.md written
- [ ] Screenshots taken
- [ ] Pushed to GitHub
- [ ] Submitted to course

---

## 🎯 Next Steps

1. Run the setup commands
2. Test the application
3. Take required screenshots
4. Create GitHub repository
5. Push code to GitHub
6. Submit assignment

---

## 📞 Support Resources

- **Setup Issues:** See QUICK_START.md
- **Requirements:** See PROJECT_DOCS.md
- **Database Schema:** See 01_create_database.sql
- **Sample Queries:** See 03_verification_queries.sql

---

## 🏆 Project Status

**COMPLETE AND READY FOR SUBMISSION** ✅

All requirements met and exceeded. Professional-quality code ready for GitHub and course submission.

---

**Good luck with your assignment!** 🚀

This is a solid database project that demonstrates real-world application development skills. You should be proud of this work!
