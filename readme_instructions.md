# Rossmann Store Sales - Business Analytics Project

##  Project Overview

This project performs comprehensive business analytics on Rossmann drugstore sales data using Python, MySQL, and data visualization libraries. The analysis includes data extraction, preprocessing, database design, and advanced analytics with visualizations.

---

## 🛠️ Prerequisites

### Software Requirements
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **MySQL Server 8.0+** - [Download](https://dev.mysql.com/downloads/mysql/)
3. **MySQL Workbench** (optional, for database management) - [Download](https://dev.mysql.com/downloads/workbench/)

### Python Libraries
All required libraries are listed in `requirements.txt`

---

## 📦 Installation Steps

### Step 1: Install Python Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- numpy (numerical operations)
- mysql-connector-python (MySQL connectivity)
- matplotlib (data visualization)
- seaborn (statistical visualization)

### Step 2: Setup MySQL Database

1. Install MySQL Server on your machine
2. Start MySQL service
3. Note your MySQL username and password (you'll need these)

Default credentials are usually:
- **Username**: `root`
- **Password**: (the password you set during MySQL installation)

### Step 3: Configure Database Connection

Edit the following files and update MySQL credentials:

**In `03_mysql_database_setup.py`:**
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Your MySQL username
    'password': 'yourpassword'  # Your MySQL password
}
```

**In `04_data_analysis_visualization.py`:**
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': 'yourpassword',  # Your MySQL password
    'database': 'rossmann_analytics'
}
```

---

##  Running the Project

### Execute Scripts in Order

The project consists of 4 sequential scripts that must be run in order:

#### Script 1: Data Extraction & Exploration
```bash
python 01_data_extraction_exploration.py
```
**What it does:**
- Loads the raw CSV files (train2.csv, store.csv)
- Performs initial data quality assessment
- Identifies missing values and data issues
- Generates exploration report

**Output:**
- `data_exploration_report.txt`

---

#### Script 2: Data Preprocessing
```bash
python 02_data_preprocessing.py
```
**What it does:**
- Cleans data (removes closed stores, handles nulls)
- Creates derived columns (SalesPerCustomer, weekend flags, etc.)
- Builds date dimension table
- Prepares dimension and fact tables

**Output:**
- `processed_dim_store.csv`
- `processed_dim_date.csv`
- `processed_fact_sales.csv`
- `preprocessing_summary.txt`

---

#### Script 3: MySQL Database Setup
```bash
python 03_mysql_database_setup.py
```
**What it does:**
- Creates MySQL database (`rossmann_analytics`)
- Defines star schema (dimension and fact tables)
- Creates relationships and indexes
- Loads all preprocessed data into MySQL

**Output:**
- MySQL database with 3 tables (dim_store, dim_date, fact_sales)
- `database_setup_info.txt`

** Important:** Make sure MySQL is running before executing this script!

---

#### Script 4: Data Analysis & Visualization
```bash
python 04_data_analysis_visualization.py
```
**What it does:**
- Connects to MySQL database
- Performs comprehensive analytics:
  - Descriptive statistics
  - Store type analysis
  - Promotional effectiveness
  - Temporal trends
  - Competition impact
  - Top performer identification
  - Correlation analysis
- Generates visualizations and insights report

**Output:**
- `analysis_store_type.png`
- `analysis_promotional_effectiveness.png`
- `analysis_monthly_trend.png`
- `analysis_day_of_week.png`
- `analysis_competition.png`
- `analysis_top_stores.png`
- `analysis_correlation.png`
- `insights_report.txt`

---

##  Project Structure

```
rossmann-analytics/
│
├── train2.csv                              # Raw training data
├── store.csv                               # Raw store metadata
│
├── 01_data_extraction_exploration.py       # Script 1: Data loading & exploration
├── 02_data_preprocessing.py                # Script 2: Data cleaning & transformation
├── 03_mysql_database_setup.py              # Script 3: Database creation & loading
├── 04_data_analysis_visualization.py       # Script 4: Analysis & visualization
│
├── requirements.txt                        # Python dependencies
├── README.md                               # This file
│
├── processed_dim_store.csv                 # Processed dimension table
├── processed_dim_date.csv                  # Processed dimension table
├── processed_fact_sales.csv                # Processed fact table
│
├── data_exploration_report.txt             # Exploration findings
├── preprocessing_summary.txt               # Preprocessing summary
├── database_setup_info.txt                 # Database info
├── insights_report.txt                     # Final insights report
│
└── analysis_*.png                          # Visualization outputs
```

---

##  Database Schema

### Star Schema Design

**Dimension Tables:**
1. **dim_store** - Store characteristics and metadata
   - Primary Key: StoreID
   - Contains: StoreType, Assortment, Competition info, Promo2 info

2. **dim_date** - Date dimension with temporal attributes
   - Primary Key: DateID
   - Contains: Year, Month, Quarter, Day, Weekend flags, etc.

**Fact Table:**
3. **fact_sales** - Sales transactions (grain: one record per store per day)
   - Primary Key: SalesID (auto-increment)
   - Foreign Keys: StoreID → dim_store, DateID → dim_date
   - Contains: Sales, Customers, Promo flags, derived metrics

---

##  Analysis Outputs

The project generates 7 key visualizations:

1. **Store Type Analysis** - Performance comparison across store types
2. **Promotional Effectiveness** - Impact of promotions on sales
3. **Monthly Trends** - Time series analysis of sales patterns
4. **Day of Week Analysis** - Weekly sales patterns
5. **Competition Impact** - How competition proximity affects sales
6. **Top Performers** - Identification of best-performing stores
7. **Correlation Matrix** - Relationships between variables

Plus a comprehensive **Insights Report** with:
- Key findings
- Statistical summaries
- Strategic recommendations
- Actionable business insights

---

## 🔧 Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
pip install [missing-module-name]
```

**2. "Access denied for user" (MySQL)**
- Check username/password in DB_CONFIG
- Ensure MySQL server is running
- Verify user has CREATE DATABASE privileges

**3. "File not found: train2.csv"**
- Ensure CSV files are in the same directory as scripts
- Check file names match exactly

**4. Script runs but no output**
- Check for error messages in console
- Verify all previous scripts completed successfully
- Check file permissions

**5. MySQL connection timeout**
- Start MySQL service: `sudo service mysql start` (Linux/Mac)
- Or use MySQL Workbench to start the server

---

##  Support

For issues or questions about this project:
1. Check the error message carefully
2. Verify all prerequisites are installed
3. Ensure scripts are run in order (1→2→3→4)
4. Check MySQL is running before script 3

---

##  Project Report Components

For your final submission, include:

1. **Project Proposal** (already created)
2. **Infrastructure Diagram** - Show data flow:
   ```
   CSV Files → Python (Pandas) → MySQL → Python (Analysis) → Visualizations
   ```
3. **Insights Report** - Generated by script 4
4. **Visualizations** - All 7 PNG files
5. **Code Documentation** - All 4 Python scripts

---

##  Checklist for Successful Execution

- [ ] Python 3.8+ installed
- [ ] MySQL Server installed and running
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV files (train2.csv, store.csv) in project directory
- [ ] MySQL credentials updated in scripts 3 and 4
- [ ] Script 1 executed successfully
- [ ] Script 2 executed successfully
- [ ] Script 3 executed successfully (database created)
- [ ] Script 4 executed successfully (visualizations generated)
- [ ] All output files created
- [ ] Insights report reviewed

---

##  Learning Outcomes

By completing this project, you will have demonstrated:

✅ Data extraction and loading with Python  
✅ Data preprocessing and transformation  
✅ Handling missing values and data quality issues  
✅ Creating derived columns and features  
✅ Database design (star schema)  
✅ SQL database creation and data loading  
✅ Joining multiple tables  
✅ Descriptive statistics and aggregations  
✅ Time series and trend analysis  
✅ Data visualization with Matplotlib/Seaborn  
✅ Business insights generation  
✅ Professional reporting  

---

**Good luck with your Business Analytics project! 🚀**
