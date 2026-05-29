import pandas as pd
import random
import os

# Ensure directories exist
os.makedirs("data_lake/raw", exist_ok=True)
os.makedirs("data_lake/processed", exist_ok=True)
os.makedirs("data_lake/analytics", exist_ok=True)

# ==========================================
# 1. BRONZE LAYER: Drop raw file to landing zone
# ==========================================
def ingest_to_raw_landing():
    print("[Bronze Zone] Ingesting telemetry data streams...")
    raw_records = []
    
    for _ in range(99):
        customer_id = random.randint(100000, 999999)
        monthly_bill = random.randint(30, 150)
        churn = random.choice([0, 1])
        raw_records.append((customer_id, monthly_bill, churn))
        
    # Inject duplicate record to test storage filter
    raw_records.append((raw_records[0][0], 140, 1))
    
    df = pd.DataFrame(raw_records, columns=["customer_id", "monthly_bill", "churn"])
    
    # Save directly as a raw file drop
    raw_file_path = "data_lake/raw/daily_telemetry_raw.csv"
    df.to_csv(raw_file_path, index=False)
    print(f"[Bronze Zone] Raw file dropped successfully -> {raw_file_path}")

# ==========================================
# 2. SILVER LAYER: Clean data and save to processed zone
# ==========================================
def clean_to_processed_zone():
    print("[Silver Zone] Reading raw drop from landing files...")
    raw_file_path = "data_lake/raw/daily_telemetry_raw.csv"
    
    if not os.path.exists(raw_file_path):
        print("[Silver Zone] Error: No raw data found to transform.")
        return
        
    # Read the raw file
    df = pd.read_csv(raw_file_path)
    
    # Process and remove duplicates
    initial_len = len(df)
    df_cleaned = df.drop_duplicates(subset=["customer_id"], keep="first")
    print(f"[Silver Zone] Deduplication dropped {initial_len - len(df_cleaned)} row(s).")
    
    # Save clean file to processed zone
    processed_file_path = "data_lake/processed/daily_telemetry_clean.csv"
    df_cleaned.to_csv(processed_file_path, index=False)
    print(f"[Silver Zone] Polished file saved successfully -> {processed_file_path}")

# ==========================================
# 3. GOLD LAYER: Aggregate insights for business managers
# ==========================================
def aggregate_to_analytics_zone():
    print("[Gold Zone] Compiling high-value metrics for analytics...")
    processed_file_path = "data_lake/processed/daily_telemetry_clean.csv"
    
    if not os.path.exists(processed_file_path):
        print("[Gold Zone] Error: No processed data found.")
        return
        
    df = pd.read_csv(processed_file_path)
    
    # Generate business summary metrics
    summary_data = {
        "total_tracked_customers": [len(df)],
        "average_monthly_bill": [round(df["monthly_bill"].mean(), 2)],
        "total_churned_users": [int(df["churn"].sum())]
    }
    summary_df = pd.DataFrame(summary_data)
    
    # Save final aggregate metrics file
    analytics_file_path = "data_lake/analytics/executive_churn_summary.csv"
    summary_df.to_csv(analytics_file_path, index=False)
    print(f"[Gold Zone] Analytics summary ready for dashboards -> {analytics_file_path}")

if __name__ == "__main__":
    print("--- STARTING DATA LAKE ARCHITECTURE RUN ---")
    ingest_to_raw_landing()
    clean_to_processed_zone()
    aggregate_to_analytics_zone()
    print("--- DATA LAKE RUN COMPLETED CLEANLY ---")
