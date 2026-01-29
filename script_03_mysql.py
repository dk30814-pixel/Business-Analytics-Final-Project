"""
Script 3: MySQL Database Setup and Data Loading
================================================
This script creates the MySQL database, defines the star schema,
creates tables with relationships, and loads the preprocessed data.

Author: [Your Name]
Date: [Current Date]
Course: Business Analytics Project

PREREQUISITES:
- MySQL Server installed and running
- MySQL Connector for Python installed: pip install mysql-connector-python
- Preprocessed CSV files from script 02
"""

import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# IMPORTANT: Update these with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Change to your MySQL username
    'password': 'Bz!03062003'  # Change to your MySQL password
}

DATABASE_NAME = 'rossmann_analytics'

print("="*80)
print("ROSSMANN STORE SALES - MySQL DATABASE SETUP")
print("="*80)
print("\n")

# ============================================================================
# 1. CONNECT TO MySQL AND CREATE DATABASE
# ============================================================================

print("[1/6] Connecting to MySQL server...")

try:
    # Connect to MySQL server
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    print("✓ Connected to MySQL server successfully!")
    
    # Create database
    print(f"\n[2/6] Creating database '{DATABASE_NAME}'...")
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
    cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
    print(f"✓ Database '{DATABASE_NAME}' created successfully!")
    
    # Use the database
    cursor.execute(f"USE {DATABASE_NAME}")
    
except Error as e:
    print(f"✗ Error connecting to MySQL: {e}")
    print("\nPlease check:")
    print("  1. MySQL server is running")
    print("  2. Username and password are correct in DB_CONFIG")
    print("  3. mysql-connector-python is installed: pip install mysql-connector-python")
    exit()

print("\n")

# ============================================================================
# 2. CREATE DIMENSION TABLES
# ============================================================================

print("[3/6] Creating dimension tables...")

# Create dim_store table
create_dim_store = """
CREATE TABLE dim_store (
    StoreID INT PRIMARY KEY,
    StoreType VARCHAR(10),
    Assortment VARCHAR(10),
    CompetitionDistance FLOAT,
    CompetitionOpenSinceMonth INT,
    CompetitionOpenSinceYear INT,
    Promo2 INT,
    Promo2SinceWeek INT,
    Promo2SinceYear INT,
    PromoInterval VARCHAR(50),
    CompetitionCategory VARCHAR(50),
    HasCompetition INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

cursor.execute(create_dim_store)
print("✓ Created table: dim_store")

# Create dim_date table
create_dim_date = """
CREATE TABLE dim_date (
    DateID INT PRIMARY KEY,
    Date DATE NOT NULL,
    Year INT,
    Month INT,
    Day INT,
    Quarter INT,
    WeekOfYear INT,
    DayOfWeek INT,
    DayName VARCHAR(20),
    MonthName VARCHAR(20),
    IsWeekend INT,
    IsMonthStart INT,
    IsMonthEnd INT,
    IsQuarterStart INT,
    IsQuarterEnd INT,
    IsYearStart INT,
    IsYearEnd INT,
    UNIQUE KEY unique_date (Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

cursor.execute(create_dim_date)
print("✓ Created table: dim_date")

print("\n")

# ============================================================================
# 3. CREATE FACT TABLE
# ============================================================================

print("[4/6] Creating fact table...")

create_fact_sales = """
CREATE TABLE fact_sales (
    SalesID INT AUTO_INCREMENT PRIMARY KEY,
    StoreID INT NOT NULL,
    DateID INT NOT NULL,
    Date DATE NOT NULL,
    DayOfWeek INT,
    Sales DECIMAL(10,2),
    Customers INT,
    Promo INT,
    StateHoliday VARCHAR(10),
    SchoolHoliday INT,
    SalesPerCustomer DECIMAL(10,2),
    Year INT,
    Month INT,
    Quarter INT,
    IsWeekend INT,
    FOREIGN KEY (StoreID) REFERENCES dim_store(StoreID),
    FOREIGN KEY (DateID) REFERENCES dim_date(DateID),
    INDEX idx_store (StoreID),
    INDEX idx_date (DateID),
    INDEX idx_year_month (Year, Month),
    INDEX idx_date_col (Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

cursor.execute(create_fact_sales)
print("✓ Created table: fact_sales")
print("✓ Created foreign key relationships")
print("✓ Created indexes for query optimization")

print("\n")

# ============================================================================
# 4. LOAD DATA FROM CSV FILES
# ============================================================================

print("[5/6] Loading data from CSV files...")

try:
    # Load dimension tables
    print("\n   → Loading dim_store...")
    dim_store_df = pd.read_csv('processed_dim_store.csv')
    
    # Replace NaN with None for proper NULL handling in MySQL
    dim_store_df = dim_store_df.replace({np.nan: None})
    
    for _, row in dim_store_df.iterrows():
        sql = """
        INSERT INTO dim_store 
        (StoreID, StoreType, Assortment, CompetitionDistance, 
         CompetitionOpenSinceMonth, CompetitionOpenSinceYear,
         Promo2, Promo2SinceWeek, Promo2SinceYear, PromoInterval,
         CompetitionCategory, HasCompetition)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = tuple(row)
        cursor.execute(sql, values)
    
    connection.commit()
    print(f"      Loaded {len(dim_store_df):,} records into dim_store")
    
    print("\n   → Loading dim_date...")
    dim_date_df = pd.read_csv('processed_dim_date.csv')
    
    # Replace NaN with None for proper NULL handling
    dim_date_df = dim_date_df.replace({np.nan: None})
    
    # Convert date to proper format
    dim_date_df['Date'] = pd.to_datetime(dim_date_df['Date']).dt.date
    
    for _, row in dim_date_df.iterrows():
        sql = """
        INSERT INTO dim_date 
        (DateID, Date, Year, Month, Day, Quarter, WeekOfYear, DayOfWeek,
         DayName, MonthName, IsWeekend, IsMonthStart, IsMonthEnd,
         IsQuarterStart, IsQuarterEnd, IsYearStart, IsYearEnd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = tuple(row)
        cursor.execute(sql, values)
    
    connection.commit()
    print(f"      Loaded {len(dim_date_df):,} records into dim_date")
    
    print("\n   → Loading fact_sales (this may take a few minutes)...")
    fact_sales_df = pd.read_csv('processed_fact_sales.csv')
    
    # Replace NaN with None for proper NULL handling
    fact_sales_df = fact_sales_df.replace({np.nan: None})
    
    # Convert date to proper format
    fact_sales_df['Date'] = pd.to_datetime(fact_sales_df['Date']).dt.date
    
    # Batch insert for better performance
    batch_size = 1000
    total_rows = len(fact_sales_df)
    
    for i in range(0, total_rows, batch_size):
        batch = fact_sales_df.iloc[i:i+batch_size]
        
        sql = """
        INSERT INTO fact_sales 
        (StoreID, Date, DayOfWeek, Sales, Customers, Promo, StateHoliday,
         SchoolHoliday, SalesPerCustomer, Year, Month, Quarter, IsWeekend, DateID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = []
        for _, row in batch.iterrows():
            values.append((
                int(row['StoreID']) if pd.notna(row['StoreID']) else None,
                row['Date'],
                int(row['DayOfWeek']) if pd.notna(row['DayOfWeek']) else None,
                float(row['Sales']) if pd.notna(row['Sales']) else None,
                int(row['Customers']) if pd.notna(row['Customers']) else None,
                int(row['Promo']) if pd.notna(row['Promo']) else None,
                str(row['StateHoliday']) if pd.notna(row['StateHoliday']) else None,
                int(row['SchoolHoliday']) if pd.notna(row['SchoolHoliday']) else None,
                float(row['SalesPerCustomer']) if pd.notna(row['SalesPerCustomer']) else None,
                int(row['Year']) if pd.notna(row['Year']) else None,
                int(row['Month']) if pd.notna(row['Month']) else None,
                int(row['Quarter']) if pd.notna(row['Quarter']) else None,
                int(row['IsWeekend']) if pd.notna(row['IsWeekend']) else None,
                int(row['DateID']) if pd.notna(row['DateID']) else None
            ))
        
        cursor.executemany(sql, values)
        connection.commit()
        
        if (i + batch_size) % 10000 == 0:
            print(f"      Loaded {i + batch_size:,} / {total_rows:,} records...")
    
    print(f"      Loaded {len(fact_sales_df):,} records into fact_sales")
    
    print("\n✓ All data loaded successfully!")

except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("Please ensure you've run '02_data_preprocessing.py' first!")
    cursor.close()
    connection.close()
    exit()

print("\n")

# ============================================================================
# 5. VERIFY DATA INTEGRITY
# ============================================================================

print("[6/6] Verifying data integrity...")

# Check record counts
cursor.execute("SELECT COUNT(*) FROM dim_store")
store_count = cursor.fetchone()[0]
print(f"   dim_store: {store_count:,} records")

cursor.execute("SELECT COUNT(*) FROM dim_date")
date_count = cursor.fetchone()[0]
print(f"   dim_date: {date_count:,} records")

cursor.execute("SELECT COUNT(*) FROM fact_sales")
sales_count = cursor.fetchone()[0]
print(f"   fact_sales: {sales_count:,} records")

# Check foreign key integrity
cursor.execute("""
    SELECT COUNT(*) 
    FROM fact_sales f
    LEFT JOIN dim_store s ON f.StoreID = s.StoreID
    WHERE s.StoreID IS NULL
""")
orphan_stores = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) 
    FROM fact_sales f
    LEFT JOIN dim_date d ON f.DateID = d.DateID
    WHERE d.DateID IS NULL
""")
orphan_dates = cursor.fetchone()[0]

print(f"\n   Foreign key integrity check:")
print(f"   Orphaned store records: {orphan_stores}")
print(f"   Orphaned date records: {orphan_dates}")

if orphan_stores == 0 and orphan_dates == 0:
    print("   ✓ All foreign key relationships are valid!")
else:
    print("   ⚠ Warning: Some foreign key issues detected!")

# Display sample data
print("\n   Sample data from fact_sales:")
cursor.execute("""
    SELECT f.StoreID, f.Date, f.Sales, f.Customers, s.StoreType
    FROM fact_sales f
    JOIN dim_store s ON f.StoreID = s.StoreID
    LIMIT 5
""")
sample = cursor.fetchall()
for row in sample:
    print(f"      Store {row[0]} ({row[4]}): ${row[2]:,.2f} sales, {row[3]} customers on {row[1]}")

print("\n")

# ============================================================================
# 6. DATABASE SUMMARY
# ============================================================================

# Get database statistics
cursor.execute("SELECT SUM(Sales) FROM fact_sales")
total_revenue = cursor.fetchone()[0]

cursor.execute("SELECT AVG(Sales) FROM fact_sales")
avg_daily_sales = cursor.fetchone()[0]

cursor.execute("SELECT MIN(Date), MAX(Date) FROM fact_sales")
date_range = cursor.fetchone()

summary = f"""
{'='*80}
DATABASE SETUP COMPLETE!
{'='*80}

Database: {DATABASE_NAME}
Schema: Star Schema

TABLES CREATED:
  1. dim_store (Dimension Table)
     - {store_count:,} stores
     - Attributes: StoreType, Assortment, Competition info, Promo2 info
     
  2. dim_date (Dimension Table)
     - {date_count:,} dates
     - Attributes: Year, Month, Quarter, Week, Day info, Flags
     
  3. fact_sales (Fact Table)
     - {sales_count:,} sales records
     - Date range: {date_range[0]} to {date_range[1]}
     - Total revenue: ${total_revenue:,.2f}
     - Average daily sales: ${avg_daily_sales:,.2f}
     
RELATIONSHIPS:
  • fact_sales.StoreID → dim_store.StoreID (Foreign Key)
  • fact_sales.DateID → dim_date.DateID (Foreign Key)
  
INDEXES CREATED:
  • idx_store (on StoreID)
  • idx_date (on DateID)
  • idx_year_month (on Year, Month)
  • idx_date_col (on Date)
  
{'='*80}

Ready for analysis and visualization!
Next Step: Run '04_data_analysis_visualization.py'

MySQL Connection Details:
  Host: {DB_CONFIG['host']}
  Database: {DATABASE_NAME}
  User: {DB_CONFIG['user']}
  
You can also connect using MySQL Workbench or any MySQL client.
{'='*80}
"""

print(summary)

# Save database info
with open('database_setup_info.txt', 'w') as f:
    f.write(summary)
print("💾 Saved database info to 'database_setup_info.txt'")

# Close connection
cursor.close()
connection.close()
print("\n✓ MySQL connection closed")
print("\n" + "="*80)