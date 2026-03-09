# EV Market India – Data Pipeline & Analytics Dashboard
PPT LINK ---> https://github.com/06-10-2004/EV_Market_India/blob/main/Electric%20Vehicle%20In%20India.pdf
---
EV PROJECT VIDEO --> https://github.com/06-10-2004/EV_Market_India/blob/main/Project%20Video.mp4
---

This project analyzes Electric Vehicle (EV) adoption trends in India using a complete data pipeline and an interactive analytics dashboard. The system processes raw EV datasets, performs data cleaning and feature engineering, stores the data in a structured SQL database, and visualizes key insights using a Streamlit dashboard.

---

#### Project Objective

The objective of this project is to build an end-to-end ETL[Extract, Transform, Load] data pipeline that processes EV market data and provides meaningful insights through visual analytics via production level Streamlit Dashboard webapp.

---

#### Tools and Technologies Used

- Python
- Pandas
- Logging, Time, Sys, OS
- SQL Server
- Matplotlib
- Seaborn
- Streamlit
- Git & GitHub

---

#### Business Problem

The rapid growth of Electric Vehicles requires better understanding of regional adoption trends, price affordability, battery range demand, and infrastructure gaps. Without proper analysis, policymakers and companies cannot effectively plan EV infrastructure or market strategies.

---

#### Data Pipeline Architecture

The project follows a structured ETL pipeline:

1. Data Extraction from EV datasets
2. Data Cleaning and Validation to handle missing values and inconsistencies
3. Feature Engineering to create additional analytical variables
4. Loading processed data into a SQL Data Warehouse star schema
5. Visualization through a production level Streamlit dashboard

---

#### Project Organization and Purpose

The project is organized into multiple modules to manage different stages of the data pipeline including data cleaning, feature engineering, database loading, and visualization.

---

#### Data Analysis and Insights

The Streamlit dashboard provides visual analysis including:

- EV adoption by region
- Metro vs Non-Metro adoption comparison
- EV price distribution
- EV range analysis
- Premium vs non-premium EV comparison
- States with lowest EV adoption
- EV price trends over time

---

#### Key Insights and Business Impact

| Insight | Value / Observation |
|-------|----------------------|
| Non-Metro areas account for most adoption | 82.1% of EVs are in Non-Metro areas → need for infrastructure expansion |
| South India leads adoption; East India lags | South: 51,995 vehicles, East: 26,033 vehicles |
| Average EV price: ₹45 lakh (affordability barrier) | High prices highlight affordability issues |
| Battery range demand balanced (High / Medium / Low) | High: 33.8%, Medium: 33.8%, Low: 32.4% |
| States with low adoption indicate infrastructure gaps | Delhi: 4,143; Kerala: 8,217; Andhra Pradesh: 8,528 |

---

#### Future Enhancements

- Predictive Modeling:
Use machine learning to forecast EV adoption
trends by region or state
- Computer Vision:
Analyze images of EV models for features, design, or safety
compliance
