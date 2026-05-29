import psycopg2
import pandas as pd
import random

# ==========================================
# 1. EXTRACT STAGE: Ingest raw telemetry
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
    
    # Inject an intentional duplicate entry to test cleaning logic
    duplicate_record = (raw_records[0][0], 120, 2, 1, 500, 2, 0)
    raw_records.append(duplicate_record)
    
    columns = ["customer_id", "monthly_bill", "complaints", "late_payments", "usage_gb", "contract_type", "churn"]
    return pd.DataFrame(raw_records, columns=columns)

# ==========================================
# 2. TRANSFORM STAGE: Deduplication & Feature Engineering
# ==========================================
def transform_data(df):
    print(f"[Transform] Total raw records received: {len(df)}")
    
    # Action A: Deduplicate records
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    
    # Action B: Feature Engineering (Adding Customer Tenure in months) 
    print("[Transform] Engineering new AI feature: 'customer_tenure'...") 
    # We will generate reasonable tenures from 1 to 72 months (up to 6 years)
    df['customer_tenure'] = [random.randint(1, 72) for _ in range(len(df))]
    
    print(f"[Transform] Cleaned & enriched records remaining: {len(df)}")
    return df

# ==========================================
# 3. LOAD STAGE: Push enriched data matrix to Postgres
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
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("[Load] Shipping feature-engineered data matrix into 'customer_data'...")
        
        for _, row in df.iterrows():
            cust_id = int(row['customer_id'])
            
            # Pre-check database to see if customer_id exists
            cursor.execute("SELECT 1 FROM customer_data WHERE customer_id = %s;", (cust_id,))
            exists = cursor.fetchone()
            
            if not exists:
                postgres_insert_query = """
                INSERT INTO customer_data (customer_id, monthly_bill, complaints, late_payments, usage_gb, contract_type, churn, customer_tenure)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                record_to_insert = (
                    cust_id, int(row['monthly_bill']), int(row['complaints']),
                    int(row['late_payments']), int(row['usage_gb']), int(row['contract_type']), 
                    int(row['churn']), int(row['customer_tenure'])
                )
                cursor.execute(postgres_insert_query, record_to_insert)
            else:
                # If it already exists, let's update the tenure value for that customer
                cursor.execute(
                    "UPDATE customer_data SET customer_tenure = %s WHERE customer_id = %s;",
                    (int(row['customer_tenure']), cust_id)
                )
                
        print("[Load] Pipeline synchronized smoothly!")
        
    except Exception as e:
        print(f"[Load] ERROR: Pipeline write failed -> {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("--- STARTING ENRICHED TELECOM ETL PIPELINE RUN ---")
    raw_data = extract_raw_data()
    enriched_data = transform_data(raw_data)
    load_data_to_postgres(enriched_data)
    print("--- ETL PIPELINE COMPLETE ---")
