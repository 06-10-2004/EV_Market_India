# ==========================================
# EV FEATURE ENGINEERING
# (Called from main.py)
# ==========================================

import os
import pandas as pd
import logging
import time
from datetime import datetime

# ------------------------------------------
# Logging Configuration (File Only)
# ------------------------------------------
logging.basicConfig(
    filename="feature_engineering.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------
# Folder Paths
# ------------------------------------------
input_folder = r"D:\Desktop\Electric_Vehicle\cleaned_data"
output_folder = r"D:\Desktop\Electric_Vehicle\feature_engineer"

os.makedirs(output_folder, exist_ok=True)

current_year = datetime.now().year


# ==========================================
# EV_Model Feature Engineering
# ==========================================

def process_ev_model():

    print("\nStarting EV_Model Feature Engineering...")
    logging.info("EV_Model Feature Engineering Started")
    time.sleep(1)

    df_model = pd.read_csv(os.path.join(input_folder, "EV_Model_Cleaned.csv"))

    df_model.columns = df_model.columns.str.replace(" ", "_")

    df_model["Model_Year"] = pd.to_numeric(df_model["Model_Year"], errors="coerce")
    df_model["Electric_Range"] = pd.to_numeric(df_model["Electric_Range"], errors="coerce")
    df_model["Base_MSRP"] = pd.to_numeric(df_model["Base_MSRP"], errors="coerce")

    # Vehicle Age
    df_model["Vehicle_Age"] = current_year - df_model["Model_Year"]

    # Range Category
    df_model["Range_Category"] = "Low"
    df_model.loc[df_model["Electric_Range"] >= 100, "Range_Category"] = "Medium"
    df_model.loc[df_model["Electric_Range"] >= 250, "Range_Category"] = "High"

    # Price Category
    df_model["Price_Category"] = "Budget"
    df_model.loc[df_model["Base_MSRP"] >= 30000, "Price_Category"] = "Mid"
    df_model.loc[df_model["Base_MSRP"] >= 60000, "Price_Category"] = "Premium"

    # Price per Range
    df_model["Price_per_Range"] = (
        df_model["Base_MSRP"] / df_model["Electric_Range"]
    ).round(2)

    # EV Class
    df_model["EV_Class"] = df_model["Electric_Vehicle_Type"].apply(
        lambda x: "BEV" if "BEV" in str(x) else "PHEV"
    )

    # Flags
    df_model["High_Range_Flag"] = (df_model["Electric_Range"] >= 300).astype(int)
    df_model["Premium_Flag"] = (df_model["Base_MSRP"] >= 60000).astype(int)

    # Save
    df_model.to_csv(os.path.join(output_folder, "EV_Model_FE.csv"), index=False)

    print("EV_Model Feature Engineering Completed.")
    logging.info("EV_Model Feature Engineering Completed")
    time.sleep(1)


# ==========================================
# EV_India Feature Engineering
# ==========================================

def process_ev_india():

    print("\nStarting EV_India Feature Engineering...")
    logging.info("EV_India Feature Engineering Started")
    time.sleep(1)

    df_india = pd.read_csv(os.path.join(input_folder, "EV_India_Cleaned.csv"))

    df_india.columns = df_india.columns.str.replace(" ", "_")

    # Region Mapping
    region_map = {
        "Tamil Nadu": "South",
        "Karnataka": "South",
        "Kerala": "South",
        "Maharashtra": "West",
        "Gujarat": "West",
        "Delhi": "North",
        "Punjab": "North",
        "West Bengal": "East"
    }

    df_india["Region"] = df_india["State"].map(region_map)
    df_india["Region"] = df_india["Region"].fillna("Other")

    # Metro Flag
    metro_cities = [
        "Delhi", "Mumbai", "Bangalore",
        "Chennai", "Kolkata", "Hyderabad"
    ]

    df_india["Metro_Flag"] = df_india["City"].isin(metro_cities).astype(int)

    # High Adoption Flag
    high_states = ["Maharashtra", "Karnataka", "Delhi", "Tamil Nadu"]

    df_india["High_Adoption_State_Flag"] = (
        df_india["State"].isin(high_states)
    ).astype(int)

    # Save
    df_india.to_csv(os.path.join(output_folder, "EV_India_FE.csv"), index=False)

    print("EV_India Feature Engineering Completed.")
    logging.info("EV_India Feature Engineering Completed")
    time.sleep(1)


# ==========================================
# Main Block (Required for main.py execution)
# ==========================================

if __name__ == "__main__":

    print("\nFEATURE ENGINEERING PIPELINE STARTED\n")
    logging.info("Feature Engineering Pipeline Started")

    process_ev_model()
    process_ev_india()

    print("\nAll Feature Engineering Tasks Completed Successfully!\n")
    logging.info("Feature Engineering Pipeline Completed Successfully")