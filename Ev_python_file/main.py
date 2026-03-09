# =====================================
# EV MASTER EXECUTION FILE (main.py)
# =====================================

import subprocess
import sys
import time
import logging
from colorama import init, Fore

# -------------------------------------
# Initialize colorama
# -------------------------------------
init(autoreset=True)

# -------------------------------------
# Logging Setup (File Only)
# -------------------------------------
logging.basicConfig(
    filename="master_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------
# Function to Run Each Script
# -------------------------------------
def run_script(script_name):

    print(Fore.YELLOW + f"\nRunning {script_name}...")
    logging.info(f"Running {script_name}")
    time.sleep(2)

    try:
        # Use same Python interpreter
        subprocess.run([sys.executable, script_name], check=True)

        print(Fore.GREEN + f"{script_name} completed successfully.")
        logging.info(f"{script_name} completed successfully.")
        time.sleep(2)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"{script_name} failed!")
        logging.error(f"{script_name} failed: {e}")
        sys.exit(1)


# =====================================
# MAIN EXECUTION
# =====================================
if __name__ == "__main__":

    start_time = time.time()

    print(Fore.CYAN + "\nEV END-TO-END PIPELINE STARTED\n")
    logging.info("Pipeline started")

    # ---------------------------------
    # Run Scripts in Order
    # ---------------------------------

    run_script("data_cleaning.py")
    run_script("feature_engineering.py")
    run_script("loading_to_SQL.py")
    run_script("Visual_analysis.py")   # ← Added Analysis Step

    # ---------------------------------
    # Pipeline Completed
    # ---------------------------------

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print(Fore.CYAN + "\nALL TASKS COMPLETED SUCCESSFULLY!")
    print(Fore.CYAN + f"Total Execution Time: {duration} seconds\n")

    logging.info(f"Pipeline completed in {duration} seconds")