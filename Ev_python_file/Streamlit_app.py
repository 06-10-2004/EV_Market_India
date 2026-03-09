import os
import sys
import time
import subprocess
import webbrowser
import re

import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="⚡ EV Data Analytics Platform",
    page_icon="⚡",
    layout="wide"
)

# ===============================
# RELATIVE PATHS
# ===============================
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')

HERO_IMAGE = os.path.join(IMAGES_DIR, 'EV_image.png')  # hero image
TOOLS_IMAGE = os.path.join(IMAGES_DIR, 'Data_tools.png')
PIPELINE_IMAGE = os.path.join(IMAGES_DIR, 'data_pipeline.png')

# ===============================
# SIDEBAR NAVIGATION
# ===============================
page = st.sidebar.radio(
    "Navigation",
    ["Hero Page", "Project Overview", "Visual Analytics Dashboard"]
)

# ===============================
# PAGE 1 — HERO PAGE
# ===============================
if page == "Hero Page":
    if os.path.exists(HERO_IMAGE):
        hero_img = Image.open(HERO_IMAGE)
        st.image(hero_img, use_column_width=True)

    st.markdown(
        """
        <div style='
            position: relative;
            top: -100px; 
            color: white;
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            text-shadow: 2px 2px 6px black;
        '>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='
            position: relative;
            top: -80px;
            color: white;
            text-align: center;
            font-size: 24px;
            text-shadow: 1px 1px 4px black;
        '>
            Driving Insights on EV Adoption in India
        </div>
        """, unsafe_allow_html=True
    )

# ===============================
# PAGE 2 — PROJECT OVERVIEW
# ===============================
elif page == "Project Overview":
    st.title("⚡  EV Project  ")
    st.subheader("INDEX")
    st.markdown("""
            1. Project Objective
            2. Tools and Technologies used  
            3. Business Problem 
            3. Data Pipeline Architecture 
            4. Project Organization & Purpose 
            5. Data analysis and Insights  
            6. Key Insights and Business Impact  
            7. Future Enhancement 
            """)

    st.subheader("Project Objective")
    st.write("""
    Build a **comprehensive end-to-end EV data analytics pipeline and interactive dashboard** 
    to monitor and analyze EV adoption trends in India. Lifecycle includes:
    - Data Cleaning
    - Feature Engineering
    - SQL Data Warehouse Loading
    - Analytics & Insights
    - Interactive Dashboard Visualization
    """)

    st.subheader("Tools & Technologies Used")
    if os.path.exists(TOOLS_IMAGE):
        img = Image.open(TOOLS_IMAGE)
        st.image(img, caption="EV Data Pipeline Architecture", width=500)

    st.subheader("Business Problem")
    st.write("""
    Electric vehicle adoption in India faces challenges:
    - High upfront costs
    - Limited battery range options
    - Vehicle safety and age concerns
    - Uneven adoption across regions and metro/non-metro areas
    """)

    st.subheader("Data Pipeline Architecture")
    if os.path.exists(PIPELINE_IMAGE):
        img = Image.open(PIPELINE_IMAGE)
        st.image(img, caption="EV Data Pipeline Architecture", width=500)

    st.subheader("Project Organization & Purpose")
    st.code("""
    D:\\Desktop\\Electric_Vehicle
    ├── EV_Datasets         # Raw CSV data files
    ├── cleaned_data        # Cleaned datasets after preprocessing
    ├── feature_engineer    # Feature-engineered datasets
    ├── Ev_python_file      # Python scripts for cleaning, feature engineering, SQL loading, dashboard
    ├── SQL - DB            # SQL scripts: Data warehouse, analytics queries
    ├── virtuaenv           # Python virtual environment
    └── .idea               # IDE project files
    """)
    st.write("""
    **Pipeline Purpose:**
    - **Data Cleaning:** Remove duplicates, fix missing values, standardize  
    - **Feature Engineering:** Create derived columns, price/range categories, flags, vehicle age  
    - **SQL Loading:** Load cleaned and feature-engineered datasets into SQL Server  
    - **Analytics Layer:** Run queries to generate insights on adoption, cost, range, and safety  
    - **Dashboard:** Visualize results interactively with filters and charts
    """)

    # == == == == == == == == == == == == == == == =
    # 8️⃣ Data Analysis & Insights
    # ===============================
    st.header("Data Analysis & Key Insights")
    st.write("""
        **Insights Generated in the Project:**  
        - Metro vs Non-Metro adoption trends  
        - Regional adoption differences  
        - EV range vs price category analysis  
        - High-Range EV penetration  
        - Vehicle age and safety trends  
        - Top EV models by price
        """)

    # Business Impact Table
    st.header("Key Insights & Business Impact")
    impact_data = {
        "Insight": [
            "Non-Metro areas account for most adoption",
            "South India leads adoption; East India lags",
            "Average EV price: ₹45 lakh (affordability barrier)",
            "Battery range demand balanced (High/Medium/Low)",
            "States with low adoption indicate infrastructure gaps"
        ],
        "Value / Observation": [
            "82.1% of EVs are in Non-Metro areas → need for infrastructure expansion",
            "South: 51,995 vehicles, East: 26,033 vehicles",
            "High prices highlight affordability issues",
            "High: 33.8%, Medium: 33.8%, Low: 32.4%",
            "Delhi: 4,143; Kerala: 8,217; Andhra Pradesh: 8,528"
        ]
    }
    impact_df = pd.DataFrame(impact_data)
    st.table(impact_df)

    st.header("Future Enhancements")
    st.write("""
              **Future Enhancements / Advanced Analytics Possibilities:**  
       - **Predictive Modeling:** Use machine learning to forecast EV adoption trends by region or state  
       - **Computer Vision:** Analyze images of EV models for features, design, or safety compliance  
       - **Infrastructure Planning:** Combine EV data with charging station locations to optimize network placement  
       """)

# ===============================
# PAGE 3 — VISUAL ANALYTICS DASHBOARD
# ===============================
elif page == "Visual Analytics Dashboard":
    st.title("⚡ EV Data Pipeline Execution & Visual Insights")

    st.write("""
        Explore interactive visualizations showing EV adoption patterns across India.
        Filters include Region, State, Metro vs Non-Metro, and more.
    """)

    st.info("Dashboard and pipeline visualizations will appear here after execution.")

    # -------------------------------
    # Initialize session state
    # -------------------------------
    if "pipeline_completed" not in st.session_state:
        st.session_state.pipeline_completed = False
    if "pipeline_data" not in st.session_state:
        st.session_state.pipeline_data = None
    if "run_status" not in st.session_state:
        st.session_state.run_status = False

    # -------------------------------
    # Clean ANSI codes
    # -------------------------------
    def clean_logs(text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)


    # -------------------------------
    # RUN PIPELINE FUNCTION
    # -------------------------------
    def run_pipeline():
        log_area = st.empty()
        logs = ""

        if not st.session_state.pipeline_completed:
            try:
                # Instead of subprocess, import main.py functions directly
                # from Ev_python_file import main  <-- if you have a main() function there
                # main.run_pipeline()  # call your pipeline logic directly

                # For now, you can simulate pipeline execution with logs
                for i in range(5):
                    logs += f"Step {i + 1} completed...\n"
                    log_area.code(logs)
                    time.sleep(0.5)

                st.success("Pipeline Completed Successfully ✅")
                st.session_state.pipeline_completed = True
                return True
            except Exception as e:
                st.error(f"Pipeline Failed ❌\n{e}")
                return False
        else:
            st.info("Pipeline already completed ✅")
            return True


    # -------------------------------
    # Run pipeline button
    # -------------------------------
    if st.button("🚀 Run EV Pipeline") and not st.session_state.pipeline_completed:
        if run_pipeline():
            # Load SQL data only once
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=Hari6104\\MSSQLSERVER1;"
                "DATABASE=EV_Database;"
                "Trusted_Connection=yes;"
            )
            query = """
                SELECT
                    dl.State,
                    dl.Region,
                    dl.Metro_Flag,
                    fv.Electric_Range,
                    fv.Base_MSRP,
                    fv.High_Range_Flag,
                    fv.Premium_Flag,
                    fv.Vehicle_Age,
                    dm.Model,
                    dd.Year,
                    dm.Range_Category
                FROM Fact_EV fv
                JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
                JOIN Dim_Model dm ON fv.ModelID = dm.ModelID
                JOIN Dim_Date dd ON fv.DateID = dd.DateID
            """
            st.session_state.pipeline_data = pd.read_sql(query, conn)
            conn.close()
            st.session_state.run_status = True

    # -------------------------------
    # Display visuals only after pipeline completion
    # -------------------------------
    if st.session_state.pipeline_completed or st.session_state.run_status:
        df = st.session_state.pipeline_data.copy()

        # -------------------------------
        # Filters
        # -------------------------------
        col1, col2 = st.columns(2)
        with col1:
            region_filter = st.selectbox("Select Region", ["All"] + sorted(df["Region"].unique()))
        with col2:
            state_filter = st.selectbox("Select State", ["All"] + sorted(df["State"].unique()))
        metro_filter = st.radio("Metro vs Non-Metro", ["All", "Metro", "Non-Metro"])

        if region_filter != "All":
            df = df[df["Region"] == region_filter]
        if state_filter != "All":
            df = df[df["State"] == state_filter]
        if metro_filter != "All":
            df = df[df["Metro_Flag"].map({1: "Metro", 0: "Non-Metro"}) == metro_filter]

        # -------------------------------
        # KPI Cards
        # -------------------------------
        total_ev = len(df)
        avg_price = df["Base_MSRP"].mean()
        avg_range = df["Electric_Range"].mean()
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total EVs", f"{total_ev}")
        kpi2.metric("Average Price", f"₹{avg_price:,.0f}")
        kpi3.metric("Average Range", f"{avg_range:.1f} km")
        sns.set_theme(style="whitegrid")

        # -------------------------------
        # GRID LAYOUT FOR ALL 11 VISUALS
        # -------------------------------
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)
        row4_col1, row4_col2 = st.columns(2)
        row5_col1, row5_col2 = st.columns(2)
        row6_col1 = st.columns(1)[0]

        # -------------------------------
        # VISUALS 1–8
        # -------------------------------
        # 1️⃣ Metro vs Non-Metro
        with row1_col1:
            st.subheader("EV Adoption: Metro vs Non-Metro")
            metro_count = [df[df["Metro_Flag"] == 1].shape[0], df[df["Metro_Flag"] == 0].shape[0]]
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(metro_count, labels=["Metro", "Non-Metro"], autopct='%1.1f%%', startangle=90)
            st.pyplot(fig)

        # 2️⃣ Region Wise Adoption
        with row1_col2:
            st.subheader("Region Wise EV Adoption")
            region_counts = df.groupby("Region").size().reset_index(name="Total_EV")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=region_counts, x="Region", y="Total_EV", ax=ax)
            for i, row in region_counts.iterrows():
                val = row["Total_EV"]
                ax.text(i, val, f'{val}', ha='center', va='bottom')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

        # 3️⃣ Average Range: Metro vs Non-Metro
        with row2_col1:
            st.subheader("Average EV Range: Metro vs Non-Metro")
            avg_range_df = df.groupby("Metro_Flag")["Electric_Range"].mean().reset_index()
            avg_range_df["Metro_Flag"] = avg_range_df["Metro_Flag"].map({1: "Metro", 0: "Non-Metro"})
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.barplot(data=avg_range_df, x="Metro_Flag", y="Electric_Range", ax=ax)
            for i, row in avg_range_df.iterrows():
                val = row["Electric_Range"]
                ax.text(i, val, f'{val:.1f}', ha='center', va='bottom')
            st.pyplot(fig)

        # 4️⃣ Top EV Models by Price
        with row2_col2:
            st.subheader("Top EV Models by Price")
            top_models = df.groupby("Model")["Base_MSRP"].max().sort_values(ascending=False).head(10).reset_index()
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(top_models["Base_MSRP"], top_models["Model"])
            for i in range(len(top_models)):
                ax.text(top_models["Base_MSRP"][i] + 200, top_models["Model"][i], f'{top_models["Base_MSRP"][i]:,.0f}')
            ax.set_xlabel("Price")
            st.pyplot(fig)

        # 5️⃣ Cost per Range by Region
        with row3_col1:
            st.subheader("EV Cost per Driving Range by Region")
            cost_range = df.groupby("Region").apply(
                lambda x: (x["Base_MSRP"] / x["Electric_Range"]).mean()).reset_index(name="Price_Per_Range")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=cost_range, x="Region", y="Price_Per_Range", ax=ax)
            for i, row in cost_range.iterrows():
                val = row["Price_Per_Range"]
                ax.text(i, val, f'{val:.2f}', ha='center', va='bottom')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

        # 6️⃣ Range Category Market Share
        with row3_col2:
            st.subheader("EV Range Category Market Share")
            range_count = df.groupby("Range_Category").size().reset_index(name="Total_Vehicles")
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(range_count["Total_Vehicles"], labels=range_count["Range_Category"], autopct='%1.1f%%',
                   startangle=90)
            st.pyplot(fig)

        # 7️⃣ Lowest EV Adoption States
        with row4_col1:
            st.subheader("States with Lowest EV Adoption")
            state_counts = df.groupby("State").size().sort_values().reset_index(name="Total_EV")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=state_counts, x="Total_EV", y="State", ax=ax)
            for i, row in state_counts.iterrows():
                val = row["Total_EV"]
                ax.text(val + 1, i, f'{val}', ha='left', va='center')
            st.pyplot(fig)

        # 8️⃣ Premium EV Adoption by Metro
        with row4_col2:
            st.subheader("Premium vs Non-Premium EVs by Metro Status")
            premium_df = df.groupby(["Metro_Flag", "Premium_Flag"]).size().reset_index(name="Total_EV")
            premium_df["Metro_Flag"] = premium_df["Metro_Flag"].map({1: "Metro", 0: "Non-Metro"})
            premium_df["Premium_Flag"] = premium_df["Premium_Flag"].map({1: "Premium", 0: "Non-Premium"})
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.barplot(data=premium_df, x="Metro_Flag", y="Total_EV", hue="Premium_Flag", ax=ax)
            for i, row in premium_df.iterrows():
                val = row["Total_EV"]
                ax.text(i, val, f'{val}', ha='center', va='bottom')
            st.pyplot(fig)

        # 9️⃣ Average EV Vehicle Age by Region
        # 9️⃣ Average EV Vehicle Age by Region — vertical bars, truncated values
        with row5_col1:
            st.subheader("Average EV Vehicle Age by Region")

            # Compute average Vehicle_Age by Region and truncate to integer
            age_df = df.groupby("Region")["Vehicle_Age"].mean().apply(int).reset_index()

            fig, ax = plt.subplots(figsize=(6, 4))

            # Vertical bar plot using truncated integers
            sns.barplot(data=age_df, x="Region", y="Vehicle_Age", ax=ax)

            # Annotate bars with integer values (same as heights now)
            for i, row in age_df.iterrows():
                ax.text(i, row["Vehicle_Age"] + 0.1, f'{row["Vehicle_Age"]}', ha='center', va='bottom')

            ax.set_ylabel("Average Vehicle Age (Years)")
            ax.set_xlabel("Region")
            ax.set_title("Average EV Vehicle Age by Region")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

        # 10️⃣ High-Range EV % by State
        with row5_col2:
            st.subheader("High-Range EV Percentage by State")
            high_range_df = df.groupby("State")["High_Range_Flag"].mean().reset_index()
            high_range_df["High_Range_Flag"] = high_range_df["High_Range_Flag"] * 100
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=high_range_df, x="High_Range_Flag", y="State", ax=ax)
            for i, row in high_range_df.iterrows():
                val = row["High_Range_Flag"]
                ax.text(val + 0.5, i, f'{val:.1f}%', ha='left', va='center')
            st.pyplot(fig)

        # 11️⃣ Average EV Price Trend Over Years
        with row6_col1:
            st.subheader("Average EV Price Trend Over Years")
            price_trend_df = df.groupby("Year")["Base_MSRP"].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=price_trend_df, x="Year", y="Base_MSRP", marker="o", ax=ax)
            for i, row in price_trend_df.iterrows():
                ax.text(row["Year"], row["Base_MSRP"] + 1000, f'{row["Base_MSRP"]:,.0f}', ha='center')
            st.pyplot(fig)