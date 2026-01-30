"""
Script 1: Data Extraction and Exploration
==========================================
This script loads the Rossmann dataset and performs initial data exploration
to understand the structure, identify data quality issues, and prepare for preprocessing.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 1. DATA EXTRACTION

print("="*80)
print("ROSSMANN STORE SALES - DATA EXTRACTION & EXPLORATION")
print("="*80)
print("\n")

# Load the datasets
print("[1/6] Loading datasets...")
try:
    train_df = pd.read_csv('train.csv')
    store_df = pd.read_csv('store.csv')
    print("✓ Datasets loaded successfully!")
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("Please ensure train.csv and store.csv are in the same directory as this script.")
    exit()

print("\n")

# ============================================================================
# 2. BASIC INFORMATION
# ============================================================================

print("[2/6] Dataset Overview")
print("-" * 80)
print(f"\nTRAIN Dataset Shape: {train_df.shape[0]:,} rows × {train_df.shape[1]} columns")
print(f"STORE Dataset Shape: {store_df.shape[0]:,} rows × {store_df.shape[1]} columns")

print("\n--- TRAIN Dataset Columns ---")
print(train_df.dtypes)

print("\n--- STORE Dataset Columns ---")
print(store_df.dtypes)

print("\n")

# 3. DATA PREVIEW

print("[3/6] Data Preview")
print("-" * 80)
print("\n--- First 5 rows of TRAIN data ---")
print(train_df.head())

print("\n--- First 5 rows of STORE data ---")
print(store_df.head())

print("\n")

# 4. DATA QUALITY ASSESSMENT

print("[4/6] Data Quality Assessment")
print("-" * 80)

print("\n--- Missing Values in TRAIN dataset ---")
train_missing = train_df.isnull().sum()
train_missing_pct = (train_df.isnull().sum() / len(train_df)) * 100
train_quality = pd.DataFrame({
    'Missing_Count': train_missing,
    'Missing_Percentage': train_missing_pct
})
print(train_quality[train_quality['Missing_Count'] > 0])

print("\n--- Missing Values in STORE dataset ---")
store_missing = store_df.isnull().sum()
store_missing_pct = (store_df.isnull().sum() / len(store_df)) * 100
store_quality = pd.DataFrame({
    'Missing_Count': store_missing,
    'Missing_Percentage': store_missing_pct
})
print(store_quality[store_quality['Missing_Count'] > 0])

print("\n--- Duplicates Check ---")
print(f"Duplicate rows in TRAIN: {train_df.duplicated().sum()}")
print(f"Duplicate rows in STORE: {store_df.duplicated().sum()}")

print("\n")

# 5. DESCRIPTIVE STATISTICS

print("[5/6] Descriptive Statistics")
print("-" * 80)

print("\n--- TRAIN Dataset - Numerical Summary ---")
print(train_df.describe())

print("\n--- STORE Dataset - Numerical Summary ---")
print(store_df.describe())

print("\n--- Categorical Variables Distribution (TRAIN) ---")
categorical_cols_train = ['DayOfWeek', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday']
for col in categorical_cols_train:
    if col in train_df.columns:
        print(f"\n{col}:")
        print(train_df[col].value_counts())

print("\n--- Categorical Variables Distribution (STORE) ---")
categorical_cols_store = ['StoreType', 'Assortment', 'Promo2']
for col in categorical_cols_store:
    if col in store_df.columns:
        print(f"\n{col}:")
        print(store_df[col].value_counts())

print("\n")

# 6. KEY FINDINGS & DATA ISSUES IDENTIFIED

print("[6/6] Key Findings & Data Quality Issues")
print("-" * 80)

print("\n DATASET SUMMARY:")
print(f"   • Total training records: {len(train_df):,}")
print(f"   • Number of unique stores: {train_df['Store'].nunique():,}")
print(f"   • Date range: Unable to determine (contains invalid dates)")
print(f"   • Total stores in metadata: {len(store_df):,}")

print("\n  DATA QUALITY ISSUES IDENTIFIED:")

# Issue 1: Closed stores
closed_stores = train_df[train_df['Open'] == 0]
print(f"   1. Closed store records: {len(closed_stores):,} ({len(closed_stores)/len(train_df)*100:.2f}%)")
print(f"      → These records have Sales=0 and need to be removed for analysis")

# Issue 2: Missing competition data
comp_missing = store_df['CompetitionDistance'].isnull().sum()
print(f"\n   2. Missing CompetitionDistance: {comp_missing} stores ({comp_missing/len(store_df)*100:.2f}%)")
print(f"      → Need imputation strategy")

# Issue 3: Missing Promo2 data
promo2_missing = store_df[['Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']].isnull().sum()
print(f"\n   3. Missing Promo2 data:")
for col, missing in promo2_missing.items():
    if missing > 0:
        print(f"      → {col}: {missing} missing values")

# Issue 4: Zero sales on open days
zero_sales_open = train_df[(train_df['Open'] == 1) & (train_df['Sales'] == 0)]
print(f"\n   4. Zero sales on open days: {len(zero_sales_open):,} records")
print(f"      → Potential data quality issue or special circumstances")

# Issue 5: Date format and null dates
date_nulls = train_df['Date'].isnull().sum()
print(f"\n   5. Date column issues:")
print(f"      → Data type: {train_df['Date'].dtype}")
print(f"      → Null/Invalid dates: {date_nulls}")
print(f"      → Needs conversion to datetime format")

print("\n✓ PREPROCESSING OPPORTUNITIES IDENTIFIED:")
print("   • Remove closed store records (Open = 0)")
print("   • Handle missing values in competition data")
print("   • Convert date strings to datetime objects")
print("   • Create date dimension table with temporal features")
print("   • Add derived columns (sales_per_customer, weekend flags, etc.)")
print("   • Merge train and store datasets")

print("\n")
print("="*80)
print("EXPLORATION COMPLETE - Ready for Preprocessing!")
print("="*80)
print("\n")

# Save summary report
print(" Saving exploration summary to 'data_exploration_report.txt'...")

# Get date range safely
date_range_str = f"{'N/A'}"

with open('data_exploration_report.txt', 'w') as f:
    f.write("ROSSMANN STORE SALES - DATA EXPLORATION REPORT\n")
    f.write("="*80 + "\n\n")
    f.write(f"Train Dataset: {train_df.shape[0]:,} rows × {train_df.shape[1]} columns\n")
    f.write(f"Store Dataset: {store_df.shape[0]:,} rows × {store_df.shape[1]} columns\n")
    f.write(f"\nDate Range: {date_range_str}\n")
    f.write(f"Unique Stores: {train_df['Store'].nunique():,}\n")
    f.write(f"\nMissing Values Summary:\n")
    f.write(store_quality[store_quality['Missing_Count'] > 0].to_string())
    f.write(f"\n\nClosed Store Records: {len(closed_stores):,}\n")
    f.write(f"Zero Sales on Open Days: {len(zero_sales_open):,}\n")

print("✓ Report saved successfully!")
print("\nNext Step: Run '02_data_preprocessing.py' to clean and transform the data.")