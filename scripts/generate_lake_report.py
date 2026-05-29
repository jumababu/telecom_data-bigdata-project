import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_executive_dashboard():
    print("[Report Engine] Loading metrics from Gold Analytics Zone...")
    analytics_file = "data_lake/analytics/executive_churn_summary.csv"
    output_image = "data_lake/analytics/manager_churn_report.png"
    
    if not os.path.exists(analytics_file):
        print(f"[Report Engine] Error: Missing analytics summary file at {analytics_file}")
        return
        
    # Read the data lake summary metrics
    df = pd.read_csv(analytics_file)
    
    total_users = df["total_tracked_customers"].iloc[0]
    avg_bill = df["average_monthly_bill"].iloc[0]
    churned_users = df["total_churned_users"].iloc[0]
    active_users = total_users - churned_users
    churn_rate = round((churned_users / total_users) * 100, 1)

    print(f"[Report Engine] Compiling visual layout for {total_users} customers...")
    
    # Set up dark/clean professional theme
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Telecom Operations & Churn Analysis — Executive Brief", fontsize=18, fontweight='bold', color='#1a1a1a')
    
    # --- Chart 1: Customer Segmentation Pie Chart ---
    labels = ['Active Subscribers', 'Churned Accounts']
    sizes = [active_users, churned_users]
    colors = ['#2ecc71', '#e74c3c']  # Clean green and corporate red
    
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, 
            textprops={'fontsize': 12, 'weight': 'bold'}, explode=(0, 0.1), shadow=True)
    ax1.set_title(f"Subscriber Distribution (Total: {total_users})", fontsize=14, fontweight='bold', pad=15)
    
    # --- Chart 2: Summary Metric KPI Card Display ---
    ax2.axis('off')  # Turn off grid lines for clean text presentation
    
    # Draw background box for KPI presentation card
    ax2.text(0.1, 0.8, "Key Performance Indicators (KPIs)", fontsize=15, fontweight='bold', color='#2c3e50')
    
    # Add structured metric rows
    ax2.text(0.1, 0.6, f"• Average Monthly Bill Amount:", fontsize=13, fontweight='bold')
    ax2.text(0.7, 0.6, f"${avg_bill}", fontsize=14, fontweight='bold', color='#2980b9')
    
    ax2.text(0.1, 0.4, f"• Lost Churned Accounts:", fontsize=13, fontweight='bold')
    ax2.text(0.7, 0.4, f"{churned_users} Users", fontsize=14, fontweight='bold', color='#c0392b')
    
    ax2.text(0.1, 0.2, f"• Overall Account Churn Rate:", fontsize=13, fontweight='bold')
    ax2.text(0.7, 0.2, f"{churn_rate}%", fontsize=16, fontweight='bold', color='#d35400')
    
    # Draw boundaries for corporate presentation format
    ax2.plot([0.05, 0.95], [0.73, 0.73], color='#bdc3c7', lw=1.5)
    ax2.plot([0.05, 0.95], [0.1, 0.1], color='#bdc3c7', lw=1.5)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Export to Gold Zone storage path
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"[Report Engine] Success! Graphic dashboard exported to -> {output_image}")

if __name__ == "__main__":
    create_executive_dashboard()
