import random
import psycopg2

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
    print("Connected to datasetdb successfully!")
    print("Inserting 50 mock customer records...")
    
    for _ in range(50):
        customer_id = random.randint(100000, 999999) 
        monthly_bill = random.randint(30, 150)        
        complaints = random.randint(0, 10)           
        late_payments = random.randint(0, 5)          
        usage_gb = random.randint(10, 1000)          
        contract = random.randint(1, 3)              
        churn = random.choice([0, 1])                

        postgres_insert_query = """ 
            INSERT INTO customer_data (customer_id, monthly_bill, complaints, late_payments, usage_gb, contract_type, churn) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
        """
        record_to_insert = (customer_id, monthly_bill, complaints, late_payments, usage_gb, contract, churn)
        
        cursor.execute(postgres_insert_query, record_to_insert)

    print("Data inserted successfully!")

except Exception as error:
    print(f"Error while connecting to PostgreSQL: {error}")

finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed.")

