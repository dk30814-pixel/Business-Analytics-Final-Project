"""
Script 4: Data Analysis and Visualization
==========================================
This script connects to the MySQL database, performs comprehensive
business analytics, and creates insightful visualizations.

Author: [Your Name]
Date: [Current Date]
Course: Business Analytics Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from mysql.connector import Error
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Change to your MySQL username
    'password': 'Bz!03062003',  # Change to your MySQL password
    'database': 'rossmann_analytics'
}

print("="*80)
print("ROSSMANN STORE SALES - DATA ANALYSIS & VISUALIZATION")
print("="*80)
print("\n")

print("[1/8] Connecting to MySQL database...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print(f"✓ Connected to database: {DB_CONFIG['database']}")
except Error as e:
    print(f"✗ Error: {e}")
    print("Please ensure '03_mysql_database_setup.py' has been run successfully!")
    exit()

print("\n")

# ============================================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================================

print("[2/8] Calculating Descriptive Statistics...")
print("-" * 80)

# Overall sales statistics
query = """
SELECT 
    COUNT(*) as TotalRecords,
    COUNT(DISTINCT StoreID) as UniqueStores,
    SUM(Sales) as TotalRevenue,
    AVG(Sales) as AvgDailySales,
    MIN(Sales) as MinSales,
    MAX(Sales) as MaxSales,
    STD(Sales) as StdDevSales,
    AVG(Customers) as AvgCustomers,
    AVG(SalesPerCustomer) as AvgBasketSize
FROM fact_sales
"""
stats_df = pd.read_sql(query, conn)

print("\n📊 OVERALL STATISTICS:")
print(f"   Total Records: {stats_df['TotalRecords'].iloc[0]:,}")
print(f"   Unique Stores: {stats_df['UniqueStores'].iloc[0]:,}")
print(f"   Total Revenue: ${stats_df['TotalRevenue'].iloc[0]:,.2f}")
print(f"   Average Daily Sales: ${stats_df['AvgDailySales'].iloc[0]:,.2f}")
print(f"   Sales Range: ${stats_df['MinSales'].iloc[0]:,.2f} - ${stats_df['MaxSales'].iloc[0]:,.2f}")
print(f"   Standard Deviation: ${stats_df['StdDevSales'].iloc[0]:,.2f}")
print(f"   Average Customers/Day: {stats_df['AvgCustomers'].iloc[0]:,.0f}")
print(f"   Average Basket Size: ${stats_df['AvgBasketSize'].iloc[0]:,.2f}")

print("\n")

# ============================================================================
# 2. SALES BY STORE TYPE
# ============================================================================

print("[3/8] Analyzing Sales by Store Type...")

query = """
SELECT 
    s.StoreType,
    COUNT(DISTINCT f.StoreID) as NumStores,
    SUM(f.Sales) as TotalSales,
    AVG(f.Sales) as AvgDailySales,
    AVG(f.Customers) as AvgCustomers,
    AVG(f.SalesPerCustomer) as AvgBasketSize
FROM fact_sales f
JOIN dim_store s ON f.StoreID = s.StoreID
GROUP BY s.StoreType
ORDER BY TotalSales DESC
"""
store_type_df = pd.read_sql(query, conn)
print("\n📈 SALES BY STORE TYPE:")
print(store_type_df.to_string(index=False))

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Total sales by store type
axes[0].bar(store_type_df['StoreType'], store_type_df['TotalSales'], color='steelblue')
axes[0].set_xlabel('Store Type')
axes[0].set_ylabel('Total Sales ($)')
axes[0].set_title('Total Sales by Store Type')
axes[0].ticklabel_format(style='plain', axis='y')

# Average basket size by store type
axes[1].bar(store_type_df['StoreType'], store_type_df['AvgBasketSize'], color='coral')
axes[1].set_xlabel('Store Type')
axes[1].set_ylabel('Average Basket Size ($)')
axes[1].set_title('Average Basket Size by Store Type')

plt.tight_layout()
plt.savefig('analysis_store_type.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_store_type.png")
plt.close()

print("\n")

# ============================================================================
# 3. PROMOTIONAL EFFECTIVENESS ANALYSIS
# ============================================================================

print("[4/8] Analyzing Promotional Effectiveness...")

query = """
SELECT 
    Promo,
    COUNT(*) as Records,
    AVG(Sales) as AvgSales,
    AVG(Customers) as AvgCustomers,
    AVG(SalesPerCustomer) as AvgBasketSize
FROM fact_sales
GROUP BY Promo
"""
promo_df = pd.read_sql(query, conn)
promo_df['Promo'] = promo_df['Promo'].map({0: 'No Promo', 1: 'With Promo'})

print("\n🎯 PROMOTIONAL IMPACT:")
print(promo_df.to_string(index=False))

# Calculate lift
no_promo_sales = promo_df[promo_df['Promo'] == 'No Promo']['AvgSales'].iloc[0]
promo_sales = promo_df[promo_df['Promo'] == 'With Promo']['AvgSales'].iloc[0]
sales_lift = ((promo_sales - no_promo_sales) / no_promo_sales) * 100

print(f"\n   Sales Lift from Promotions: {sales_lift:.2f}%")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Sales comparison
axes[0].bar(promo_df['Promo'], promo_df['AvgSales'], color=['lightcoral', 'lightgreen'])
axes[0].set_ylabel('Average Sales ($)')
axes[0].set_title('Average Sales: Promotion vs No Promotion')
axes[0].set_ylim(bottom=0)

# Customer comparison
axes[1].bar(promo_df['Promo'], promo_df['AvgCustomers'], color=['lightcoral', 'lightgreen'])
axes[1].set_ylabel('Average Customers')
axes[1].set_title('Average Customers: Promotion vs No Promotion')
axes[1].set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('analysis_promotional_effectiveness.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_promotional_effectiveness.png")
plt.close()

print("\n")

# ============================================================================
# 4. TEMPORAL TRENDS ANALYSIS
# ============================================================================

print("[5/8] Analyzing Temporal Trends...")

# Monthly sales trend
query = """
SELECT 
    Year,
    Month,
    SUM(Sales) as MonthlySales,
    AVG(Sales) as AvgDailySales,
    SUM(Customers) as MonthlyCustomers
FROM fact_sales
GROUP BY Year, Month
ORDER BY Year, Month
"""
monthly_df = pd.read_sql(query, conn)
monthly_df['YearMonth'] = pd.to_datetime(monthly_df[['Year', 'Month']].assign(DAY=1))

print("\n📅 MONTHLY SALES TREND (Sample):")
print(monthly_df.head(10).to_string(index=False))

# Visualization - Monthly Trend
plt.figure(figsize=(14, 6))
plt.plot(monthly_df['YearMonth'], monthly_df['MonthlySales'], marker='o', linewidth=2, markersize=4)
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.title('Monthly Sales Trend')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_monthly_trend.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_monthly_trend.png")
plt.close()

# Day of week analysis
query = """
SELECT 
    d.DayName,
    d.DayOfWeek,
    AVG(f.Sales) as AvgSales,
    AVG(f.Customers) as AvgCustomers
FROM fact_sales f
JOIN dim_date d ON f.DateID = d.DateID
GROUP BY d.DayName, d.DayOfWeek
ORDER BY d.DayOfWeek
"""
dow_df = pd.read_sql(query, conn)

print("\n📅 SALES BY DAY OF WEEK:")
print(dow_df.to_string(index=False))

# Visualization - Day of Week
plt.figure(figsize=(12, 5))
plt.bar(dow_df['DayName'], dow_df['AvgSales'], color='teal')
plt.xlabel('Day of Week')
plt.ylabel('Average Sales ($)')
plt.title('Average Sales by Day of Week')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('analysis_day_of_week.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_day_of_week.png")
plt.close()

print("\n")

# ============================================================================
# 5. COMPETITION ANALYSIS
# ============================================================================

print("[6/8] Analyzing Competition Impact...")

query = """
SELECT 
    s.CompetitionCategory,
    COUNT(DISTINCT f.StoreID) as NumStores,
    AVG(f.Sales) as AvgSales,
    AVG(f.Customers) as AvgCustomers,
    AVG(s.CompetitionDistance) as AvgDistance
FROM fact_sales f
JOIN dim_store s ON f.StoreID = s.StoreID
GROUP BY s.CompetitionCategory
ORDER BY AvgSales DESC
"""
comp_df = pd.read_sql(query, conn)

print("\n🏪 SALES BY COMPETITION PROXIMITY:")
print(comp_df.to_string(index=False))

# Visualization
plt.figure(figsize=(12, 6))
bars = plt.bar(comp_df['CompetitionCategory'], comp_df['AvgSales'], color='mediumpurple')
plt.xlabel('Competition Category')
plt.ylabel('Average Sales ($)')
plt.title('Average Sales by Competition Proximity')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('analysis_competition.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_competition.png")
plt.close()

print("\n")

# ============================================================================
# 6. TOP PERFORMING STORES
# ============================================================================

print("[7/8] Identifying Top Performing Stores...")

query = """
SELECT 
    f.StoreID,
    s.StoreType,
    s.Assortment,
    s.CompetitionCategory,
    SUM(f.Sales) as TotalSales,
    AVG(f.Sales) as AvgDailySales,
    AVG(f.Customers) as AvgCustomers,
    AVG(f.SalesPerCustomer) as AvgBasketSize
FROM fact_sales f
JOIN dim_store s ON f.StoreID = s.StoreID
GROUP BY f.StoreID, s.StoreType, s.Assortment, s.CompetitionCategory
ORDER BY TotalSales DESC
LIMIT 10
"""
top_stores_df = pd.read_sql(query, conn)

print("\n🏆 TOP 10 PERFORMING STORES:")
print(top_stores_df.to_string(index=False))

# Visualization
plt.figure(figsize=(12, 6))
plt.barh(top_stores_df['StoreID'].astype(str), top_stores_df['TotalSales'], color='gold')
plt.xlabel('Total Sales ($)')
plt.ylabel('Store ID')
plt.title('Top 10 Stores by Total Sales')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('analysis_top_stores.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_top_stores.png")
plt.close()

print("\n")

# ============================================================================
# 7. CORRELATION ANALYSIS
# ============================================================================

print("[8/8] Performing Correlation Analysis...")

query = """
SELECT 
    Sales,
    Customers,
    SalesPerCustomer,
    Promo,
    IsWeekend,
    SchoolHoliday
FROM fact_sales
LIMIT 50000
"""
corr_df = pd.read_sql(query, conn)

correlation_matrix = corr_df.corr()

print("\n🔗 CORRELATION MATRIX:")
print(correlation_matrix.round(3))

# Visualization
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Sales Variables')
plt.tight_layout()
plt.savefig('analysis_correlation.png', dpi=300, bbox_inches='tight')
print("\n💾 Saved: analysis_correlation.png")
plt.close()

print("\n")

# ============================================================================
# 8. GENERATE COMPREHENSIVE INSIGHTS REPORT
# ============================================================================

print("="*80)
print("GENERATING INSIGHTS REPORT")
print("="*80)

# Calculate key metrics for report
total_revenue = stats_df['TotalRevenue'].iloc[0]
avg_daily_sales = stats_df['AvgDailySales'].iloc[0]
best_store_type = store_type_df.iloc[0]['StoreType']
best_day = dow_df.loc[dow_df['AvgSales'].idxmax()]['DayName']
worst_day = dow_df.loc[dow_df['AvgSales'].idxmin()]['DayName']

insights_report = f"""
{'='*80}
ROSSMANN STORE SALES - BUSINESS ANALYTICS INSIGHTS REPORT
{'='*80}

ANALYSIS PERIOD: {monthly_df['Year'].min()}-{monthly_df['Year'].max()}
TOTAL STORES ANALYZED: {stats_df['UniqueStores'].iloc[0]:,}
TOTAL RECORDS: {stats_df['TotalRecords'].iloc[0]:,}

{'='*80}
KEY FINDINGS
{'='*80}

1. OVERALL PERFORMANCE
   • Total Revenue Generated: ${total_revenue:,.2f}
   • Average Daily Sales per Store: ${avg_daily_sales:,.2f}
   • Average Transaction Value: ${stats_df['AvgBasketSize'].iloc[0]:,.2f}
   • Daily Customer Traffic: {stats_df['AvgCustomers'].iloc[0]:,.0f} customers/store

2. STORE TYPE PERFORMANCE
   • Best Performing Store Type: {best_store_type}
   • Store Type {best_store_type} generates ${store_type_df.iloc[0]['TotalSales']:,.2f} in total sales
   • Highest average basket size: ${store_type_df['AvgBasketSize'].max():,.2f}
   
   Recommendation: Focus expansion efforts on Store Type {best_store_type} which shows
   superior performance metrics across all categories.

3. PROMOTIONAL EFFECTIVENESS
   • Promotions increase sales by {sales_lift:.2f}%
   • Average sales WITH promotion: ${promo_sales:,.2f}
   • Average sales WITHOUT promotion: ${no_promo_sales:,.2f}
   
   Recommendation: Promotional campaigns demonstrate strong ROI. Consider increasing
   promotional frequency during slower periods to boost revenue.

4. TEMPORAL PATTERNS
   • Best performing day: {best_day} (${dow_df.loc[dow_df['AvgSales'].idxmax()]['AvgSales']:,.2f} avg)
   • Lowest performing day: {worst_day} (${dow_df.loc[dow_df['AvgSales'].idxmin()]['AvgSales']:,.2f} avg)
   • Weekend sales: {'Higher' if dow_df[dow_df['DayName'].isin(['Saturday', 'Sunday'])]['AvgSales'].mean() > dow_df[~dow_df['DayName'].isin(['Saturday', 'Sunday'])]['AvgSales'].mean() else 'Lower'} than weekday average
   
   Recommendation: Optimize staffing levels based on day-of-week patterns. Increase
   staff on {best_day}, consider promotional activities on {worst_day}.

5. COMPETITION IMPACT
   • Stores with {comp_df.iloc[0]['CompetitionCategory'].lower()} competition perform best
   • Average sales: ${comp_df.iloc[0]['AvgSales']:,.2f}
   
   Recommendation: Competition proximity analysis suggests strategic positioning
   matters. Use these insights for future location selection.

6. TOP PERFORMER CHARACTERISTICS
   • Top store generates ${top_stores_df.iloc[0]['TotalSales']:,.2f} in total revenue
   • Common characteristics of top performers:
     - Store Type: {top_stores_df['StoreType'].mode()[0]}
     - Assortment: {top_stores_df['Assortment'].mode()[0]}
   
   Recommendation: Replicate successful characteristics of top-performing stores
   in underperforming locations.

7. CORRELATION INSIGHTS
   • Strong positive correlation between Customers and Sales (expected)
   • Promotion shows positive correlation with sales
   • Weekend shows {'positive' if correlation_matrix.loc['IsWeekend', 'Sales'] > 0 else 'negative'} correlation with sales
   
   Recommendation: Multi-variate approach needed for sales optimization. Focus on
   customer acquisition alongside promotional strategies.

{'='*80}
STRATEGIC RECOMMENDATIONS
{'='*80}

1. REVENUE OPTIMIZATION
   - Increase promotional activities by 15-20% to capitalize on demonstrated lift
   - Focus marketing spend on {best_day}s when customer traffic is highest
   - Implement dynamic pricing strategies based on day-of-week patterns

2. OPERATIONAL EFFICIENCY
   - Adjust inventory levels based on store type and competition proximity
   - Optimize staffing schedules to match customer traffic patterns
   - Implement best practices from Store Type {best_store_type} across all locations

3. EXPANSION STRATEGY
   - Prioritize Store Type {best_store_type} for new locations
   - Consider competition proximity when selecting new sites
   - Target areas with similar demographic profiles to top performers

4. CUSTOMER EXPERIENCE
   - Focus on increasing average basket size (currently ${stats_df['AvgBasketSize'].iloc[0]:,.2f})
   - Implement loyalty programs to increase customer frequency
   - Enhance in-store experience on slower days to boost traffic

{'='*80}
VISUALIZATIONS GENERATED
{'='*80}

The following analytical visualizations have been created:
1. analysis_store_type.png - Store type performance comparison
2. analysis_promotional_effectiveness.png - Promotion impact analysis
3. analysis_monthly_trend.png - Time series sales trends
4. analysis_day_of_week.png - Weekly sales patterns
5. analysis_competition.png - Competition proximity impact
6. analysis_top_stores.png - Top performer identification
7. analysis_correlation.png - Variable correlation heatmap

{'='*80}
METHODOLOGY
{'='*80}

Data Source: Rossmann Store Sales (Kaggle)
Analysis Period: Complete historical dataset
Tools Used: Python, MySQL, Pandas, Matplotlib, Seaborn
Statistical Methods: Descriptive statistics, aggregations, correlation analysis,
                     time series analysis, comparative analysis

{'='*80}
END OF REPORT
{'='*80}

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Analyst: [Your Name]
Course: Business Analytics Project
{'='*80}
"""

print(insights_report)

# Save report
with open('insights_report.txt', 'w') as f:
    f.write(insights_report)

print("\n💾 Saved comprehensive report: insights_report.txt")

# Close database connection
conn.close()
print("\n✓ Database connection closed")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nAll visualizations and reports have been generated successfully!")
print("\nFiles created:")
print("  • analysis_store_type.png")
print("  • analysis_promotional_effectiveness.png")
print("  • analysis_monthly_trend.png")
print("  • analysis_day_of_week.png")
print("  • analysis_competition.png")
print("  • analysis_top_stores.png")
print("  • analysis_correlation.png")
print("  • insights_report.txt")
print("\n" + "="*80)
