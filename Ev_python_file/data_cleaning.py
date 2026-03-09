# =============================================
# EV DATA CLEANING & VALIDATION PIPELINE
# =============================================

import pandas as pd
import os
import time
import logging

# ---------------------------------------------
# Logging Configuration (File Only)
# ---------------------------------------------
logging.basicConfig(
    filename="data_cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------
# Folders
# ---------------------------------------------
input_folder = r"D:\Desktop\Electric_Vehicle\EV_Datasets"
output_folder = r"D:\Desktop\Electric_Vehicle\cleaned_data"

os.makedirs(output_folder, exist_ok=True)

start_time = time.time()

print("\nStarting EV Data Cleaning & Validation Pipeline...\n")
logging.info("Data Cleaning Pipeline Started")
time.sleep(1)

# =====================================================
# DATASET 1 — EV_India
# =====================================================

print("Loading EV_India dataset...")
logging.info("Loading EV_India dataset")

file_city = os.path.join(input_folder, "EV_India.csv")
city_df = pd.read_csv(file_city)

orig_rows, orig_cols = city_df.shape
print(f"Original Shape: {orig_rows} rows × {orig_cols} columns")
logging.info(f"EV_India Original Shape: {orig_rows} x {orig_cols}")
time.sleep(1)

# Rename column
print("Renaming column County → Country")
city_df.rename(columns={"County": "Country"}, inplace=True)
logging.info("Renamed County to Country")
time.sleep(1)

# Remove unwanted column
if "Vehicle Location" in city_df.columns:
    city_df.drop(columns=["Vehicle Location"], inplace=True)
    print("Removed column: Vehicle Location")
    logging.info("Removed column: Vehicle Location")
else:
    print("No columns removed")
    logging.info("No columns removed")

time.sleep(1)

# Fix data types
print("Fixing data types...")
logging.info("Fixing data types for EV_India")

city_df["DOL Vehicle ID"] = pd.to_numeric(
    city_df["DOL Vehicle ID"], errors="coerce"
).astype("Int64")

time.sleep(1)

# Remove duplicates
print("Removing duplicate rows...")
before = len(city_df)
city_df.drop_duplicates(inplace=True)
after = len(city_df)

print(f"Removed {before - after} duplicate rows")
logging.info(f"Removed {before - after} duplicate rows from EV_India")
time.sleep(1)

# Validation
print("Validating EV_India dataset...")
logging.info("Validating EV_India dataset")

print(f"Missing DOL Vehicle ID: {city_df['DOL Vehicle ID'].isna().sum()}")
print(f"Missing City: {city_df['City'].isna().sum()}")
print(f"Missing State: {city_df['State'].isna().sum()}")
print(f"Missing Country: {city_df['Country'].isna().sum()}")

time.sleep(2)

# Save file
city_output = os.path.join(output_folder, "EV_India_Cleaned.csv")
city_df.to_csv(city_output, index=False)

print("EV_India cleaned & saved\n")
logging.info("EV_India cleaned and saved successfully")
time.sleep(1)

# =====================================================
# DATASET 2 — EV_Model
# =====================================================

print("Loading EV_Model dataset...")
logging.info("Loading EV_Model dataset")

file_type = os.path.join(input_folder, "EV_Model.csv")
type_df = pd.read_csv(file_type)

orig_rows, orig_cols = type_df.shape
print(f"Original Shape: {orig_rows} rows × {orig_cols} columns")
logging.info(f"EV_Model Original Shape: {orig_rows} x {orig_cols}")
time.sleep(1)

# Standardize EV Type
print("Standardizing Electric Vehicle Type...")
logging.info("Standardizing Electric Vehicle Type")

type_df["Electric Vehicle Type"] = (
    type_df["Electric Vehicle Type"]
    .replace({
        "Battery Electric Vehicle (BEV)": "BEV",
        "Battery Electric Vehicle": "BEV",
        "Plug-in Hybrid Electric Vehicle (PHEV)": "PHEV",
        "Plug-in Hybrid Electric Vehicle": "PHEV"
    })
    .astype("string")
)

time.sleep(1)

# Fix numeric columns
print("Fixing numeric data types...")
logging.info("Fixing numeric columns for EV_Model")

type_df["DOL Vehicle ID"] = pd.to_numeric(
    type_df["DOL Vehicle ID"], errors="coerce"
).astype("Int64")

type_df["Model Year"] = pd.to_numeric(
    type_df["Model Year"], errors="coerce"
).astype("Int64")

type_df["Electric Range"] = pd.to_numeric(
    type_df["Electric Range"], errors="coerce"
).astype("Int64")

type_df["Base MSRP"] = pd.to_numeric(
    type_df["Base MSRP"], errors="coerce"
).astype("Int64")

time.sleep(1)

# Remove duplicates
print("Removing duplicate rows...")
before = len(type_df)
type_df.drop_duplicates(inplace=True)
after = len(type_df)

print(f"Removed {before - after} duplicate rows")
logging.info(f"Removed {before - after} duplicate rows from EV_Model")
time.sleep(1)

# Validation
print("Validating EV_Model dataset...")
logging.info("Validating EV_Model dataset")

print(f"Missing DOL Vehicle ID: {type_df['DOL Vehicle ID'].isna().sum()}")
print(f"Missing Model Year: {type_df['Model Year'].isna().sum()}")
print(f"Missing Electric Range: {type_df['Electric Range'].isna().sum()}")
print(f"Missing Base MSRP: {type_df['Base MSRP'].isna().sum()}")

time.sleep(2)

# Save file
type_output = os.path.join(output_folder, "EV_Model_Cleaned.csv")
type_df.to_csv(type_output, index=False)

print("EV_Model cleaned & saved\n")
logging.info("EV_Model cleaned and saved successfully")
time.sleep(1)

# =====================================================
# FINAL SUMMARY
# =====================================================

end_time = time.time()
duration = round(end_time - start_time, 2)

print("ALL TASKS COMPLETED SUCCESSFULLY!")
print(f"Cleaned files saved in: {output_folder}")
print(f"Total processing time: {duration} seconds\n")

logging.info(f"Data Cleaning Completed in {duration} seconds")