import psycopg2
import pandas as pd
import random

# ==========================================
# 1. EXTRACT STAGE: Ingest raw telemetry
# ==========================================
def extract_raw_data():
    print("[Extract] Simulating raw telecom telemetry ingestion...")
    raw_records = []
    
    for _ in range(49):
        customer_id = random.randint(100000, 999999)
        monthly_bill = random.randint(30, 150)
        complaints = random.randint(0, 10)
        late_payments = random.randint(0, 5)
        usage_gb = random.randint(10, 1000)
        contract_type = random.randint(1, 3)
        churn = random.choice([0, 1])
        
        raw_records.append((customer_id, monthly_bill, complaints, late_payments, usage_gb, contract_type, churn))
    
    # Intentionally inject a duplicate entry to test cleaning logic 
    duplicate_record = (raw_records[0][0], 120, 2, 1, 500, 2, 0)
    raw_records.append(duplicate_record)
    
    columns = ["customer_id", "monthly_bill", "complaints", "late_payments", "usage_gb", "contract_type", "churn"]
    return pd.DataFrame(raw_records, columns=columns)

# ==========================================
# 2. TRANSFORM STAGE: Clean duplicate records
# ==========================================
def transform_data(df):
    print(f"[Transform] Total raw records received: {len(df)}")
    duplicate_count = df.duplicated(subset=['customer_id']).sum()
    print(f"[Transform] Detected {duplicate_count} duplicate customer_id record(s).")
    
    # Deduplicate the dataset 
    cleaned_df = df.drop_duplicates(subset=['customer_id'], keep='first')
    print(f"[Transform] Cleaned records remaining: {len(cleaned_df)}")
    return cleaned_df

# ==========================================
# 3. LOAD STAGE: Push polished data to Postgres
# ==========================================
def load_data_to_postgres(df):
    print("[Load] Establishing target secure database connection...")
    try:
        conn = psycopg2.connect(
            dbname="datasetdb",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("[Load] Shipping data matrix into 'customer_data'...")
        
        for _, row in df.iterrows():
            cust_id = int(row['customer_id'])
            
            # Pre-check database to see if customer_id exists
            cursor.execute("SELECT 1 FROM customer_data WHERE customer_id = %s;", (cust_id,))
            exists = cursor.fetchone()
            
            if not exists:
                postgres_insert_query = """
                INSERT INTO customer_data (customer_id, monthly_bill, complaints, late_payments, usage_gb, contract_type, churn)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                record_to_insert = (
                    cust_id, int(row['monthly_bill']), int(row['complaints']),
                    int(row['late_payments']), int(row['usage_gb']), int(row['contract_type']), int(row['churn'])
                )
                cursor.execute(postgres_insert_query, record_to_insert)
            else:
                print(f"[Load] Skipping customer_id {cust_id} (Already exists in database)")
                
        print("[Load] ETL target sync finalized cleanly!")
        
    except Exception as e:
        print(f"[Load] ERROR: Pipeline write failed -> {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

# Orchestrator
if __name__ == "__main__":
    print("--- STARTING TELECOM ETL PIPELINE RUN ---")
    raw_data = extract_raw_data()
    cleaned_data = transform_data(raw_data)
    load_data_to_postgres(cleaned_data)
    print("--- ETL PIPELINE COMPLETE ---")
