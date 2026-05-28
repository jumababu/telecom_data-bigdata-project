# Telecom Customer Data Pipeline & Analytics Project

An end-to-end data engineering and analytics pipeline that automates the generation of relational mock telecom datasets, handles secure ingestion into a local PostgreSQL database, executes advanced business intelligence queries, and renders an exploratory data analytics dashboard.

## 🏗️ System Architecture & Workflow

The architecture transitions through three core layers to move raw simulated telemetry into actionable visual insights:

1. **Data Generation Layer (`Python`)**: A localized script using random distribution boundaries to simulate active telecom client accounts, financial billing, network performance metrics, and customer satisfaction events.
2. **Database Storage Layer (`PostgreSQL`)**: A structured relational model featuring explicit attribute typing, schema boundaries, and instant transaction-write safety logs.
3. **Analytics & Dashboard Layer (`Pandas / Seaborn`)**: An automatic ingestion script that pulls raw records via explicit database connections into an execution dataframe, calculating cross-factor correlations and outputting a multi-panel visual engine.

---

## 🛠️ Installation & Setup Runbook

### 1. Environment & Dependency Initialization
Clone the repository, initialize your isolated environment, and run the dependency installation pipeline:
```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required analytics packages
pip install psycopg2-binary pandas matplotlib seaborn
