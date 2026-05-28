import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # 1. Connect to your validated PostgreSQL database
    conn = psycopg2.connect(
        dbname="datasetdb",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    
    # 2. SQL Query to fetch the columns we want to visualize
    query = "SELECT monthly_bill, complaints, late_payments, usage_gb, contract_type, churn FROM customer_data;"
    
    # 3. Read SQL data straight into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)
    print("Successfully loaded data from PostgreSQL into a Pandas DataFrame!")

except Exception as e:
    print(f"Database connection or read failed: {e}")
    exit()
finally:
    if 'conn' in locals() and conn:
        conn.close()

# Set a professional plotting style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 5))

# --- PLOT 1: Churn Correlation Heatmap ---
plt.subplot(1, 3, 1)
# Calculate the correlation matrix
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", cbar=False)
plt.title("Correlation Matrix (Churn Factors)")

# --- PLOT 2: Billing vs. Data Usage Scatter ---
plt.subplot(1, 3, 2)
sns.scatterplot(data=df, x="usage_gb", y="monthly_bill", hue="churn", palette="Set1", alpha=0.8)
plt.title("Monthly Bill vs. Internet Usage (GB)")
plt.xlabel("Usage (GB)")
plt.ylabel("Bill ($)")

# --- PLOT 3: Complaints Distribution by Contract Type ---
plt.subplot(1, 3, 3)
sns.boxplot(data=df, x="contract_type", y="complaints", hue="churn", palette="Set2")
plt.title("Complaints by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Complaints")

# Adjust spacing and display the dashboard
plt.tight_layout()
print("Generating charts... Saving to 'telecom_insights_dashboard.png'...")
plt.savefig("telecom_insights_dashboard.png", dpi=300)
print("Dashboard saved successfully to your project directory!")
plt.show()


# --- PLOT 2: Billing vs. Data Usage Scatter ---
plt.subplot(1, 3, 2)
sns.scatterplot(data=df, x="usage_gb", y="monthly_bill", hue="churn", palette="Set1", alpha=0.8)
plt.title("Monthly Bill vs. Internet Usage (GB)")
plt.xlabel("Usage (GB)")
plt.ylabel("Bill ($)")
# Moves scatter legend to the upper left corner inside, out of the way of data
plt.legend(title="Churn Status", loc="upper left")

# --- PLOT 3: Complaints Distribution by Contract Type ---
plt.subplot(1, 3, 3)
sns.boxplot(data=df, x="contract_type", y="complaints", hue="churn", palette="Set2")
plt.title("Complaints by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Complaints")
# Crucial Fix: Pushes the boxplot legend completely outside to the right of the chart
plt.legend(title="Churn Status", bbox_to_anchor=(1.05, 1), loc='upper left')
