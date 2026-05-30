import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import random

# ==========================================
# 1. EXTRACT STAGE: Vectorized Generation
# ==========================================
def extract_raw_data():
    print("[Extract] Ingesting raw telecom telemetry metrics...")
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
    
    duplicate_record = (raw_records[0][0], 120, 2, 1, 500, 2, 0)
    raw_records.append(duplicate_record)
    
    columns = ["customer_id", "monthly_bill", "complaints", "late_payments", "usage_gb", "contract_type", "churn"]
    return pd.DataFrame(raw_records, columns=columns)

# ==========================================
# 2. TRANSFORM STAGE: Vectorized Operations
# ==========================================
def transform_data(df):
    print(f"[Transform] Total raw records received: {len(df)}")
    
    df = df.drop_duplicates(subset=['customer_id'], keep='first').copy()
    print("[Transform] Engineering new AI feature: 'customer_tenure'...")
    df['customer_tenure'] = [random.randint(1, 72) for _ in range(len(df))]
    
    print(f"[Transform] Cleaned & enriched records remaining: {len(df)}")
    return df

# ==========================================
# 3. LOAD STAGE: Optimized Blazing Fast Bulk Batch Write
# ==========================================
def load_data_to_postgres(df):
    print("[Load] Connecting to target data warehouse...")
    try:
        conn = psycopg2.connect(
            dbname="datasetdb",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        print("[Load] Ensuring structural unique constraint exists on target table...")
        cursor.execute("""
            ALTER TABLE customer_data 
            ADD CONSTRAINT unique_cust_id_constraint UNIQUE (customer_id);
        """)
    except psycopg2.Error:
        conn.rollback()
    
    try:
        print("[Load] Shipping optimized data batch matrix into 'customer_data'...")
        
        # Pure Python extraction and explicit type casting to destroy any hidden NumPy data types
        data_tuples = [
            (
                int(row['customer_id']), 
                int(row['monthly_bill']), 
                int(row['complaints']), 
                int(row['late_payments']), 
                int(row['usage_gb']), 
                int(row['contract_type']), 
                int(row['churn']), 
                int(row['customer_tenure'])
            )
            for _, row in df.iterrows()
        ]
        
        batch_upsert_query = """
            INSERT INTO customer_data (customer_id, monthly_bill, complaints, late_payments, usage_gb, contract_type, churn, customer_tenure)
            VALUES %s
            ON CONFLICT (customer_id) 
            DO UPDATE SET 
                monthly_bill = EXCLUDED.monthly_bill,
                complaints = EXCLUDED.complaints,
                late_payments = EXCLUDED.late_payments,
                usage_gb = EXCLUDED.usage_gb,
                contract_type = EXCLUDED.contract_type,
                churn = EXCLUDED.churn,
                customer_tenure = EXCLUDED.customer_tenure;
        """
        
        execute_values(cursor, batch_upsert_query, data_tuples)
        conn.commit()
        print("[Load] Batch optimized pipeline synchronized smoothly!")
        
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"[Load] ERROR: Optimized batch write failed -> {e}")
        
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("--- STARTING HIGH-PERFORMANCE TELECOM ETL PIPELINE RUN ---")
    raw_data = extract_raw_data()
    enriched_data = transform_data(raw_data)
    load_data_to_postgres(enriched_data)
    print("--- ETL PIPELINE COMPLETE ---")
