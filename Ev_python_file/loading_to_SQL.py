# ==========================================
# LOAD FEATURE ENGINEERED DATA INTO SQL SERVER
# ==========================================

import pandas as pd
import pyodbc
from colorama import Fore, init

init(autoreset=True)

print(Fore.CYAN + "Starting SQL Data Loading...")

# ------------------------------------------
# File Paths
# ------------------------------------------

india_path = r"D:\Desktop\Electric_Vehicle\feature_engineer\EV_India_FE.csv"
model_path = r"D:\Desktop\Electric_Vehicle\feature_engineer\EV_Model_FE.csv"

# ------------------------------------------
# Read CSV files
# ------------------------------------------

df_india = pd.read_csv(india_path)
df_model = pd.read_csv(model_path)

print(Fore.GREEN + "CSV files loaded successfully")

# ------------------------------------------
# SQL Server Connection
# ------------------------------------------

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Hari6104\\MSSQLSERVER1;"
    "DATABASE=EV_Database;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Faster insert
cursor.fast_executemany = True

print(Fore.GREEN + "Connected to SQL Server")

# ------------------------------------------
# Function to load dataframe
# ------------------------------------------

def load_table(df, table_name):

    # Wrap column names with []
    columns = ", ".join([f"[{col}]" for col in df.columns])

    placeholders = ", ".join(["?"] * len(df.columns))

    insert_query = f"""
    INSERT INTO {table_name} ({columns})
    VALUES ({placeholders})
    """

    data = [tuple(row) for row in df.to_numpy()]

    cursor.executemany(insert_query, data)

    conn.commit()

    print(Fore.GREEN + f"{table_name} loaded successfully")


# ------------------------------------------
# Load Data
# ------------------------------------------

load_table(df_india, "EV_India_FE")
load_table(df_model, "EV_Model_FE")

# ------------------------------------------
# Close Connection
# ------------------------------------------

cursor.close()
conn.close()

print(Fore.CYAN + "SQL Loading Completed Successfully")