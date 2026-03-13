# EV Market India – Data Pipeline & Analytics Dashboard
PPT LINK --> https://github.com/06-10-2004/EV_Market_India/blob/main/Electric%20Vehicle%20In%20India.pdf
---
EV PROJECT VIDEO [Demo] --> https://github.com/06-10-2004/EV_Market_India/blob/main/Electric%20Vehicle%20in%20India.mp4
---

## 1. Introduction
The Electric Vehicle (EV) industry is growing rapidly as countries focus on reducing carbon emissions and promoting sustainable transportation.  
This project analyzes EV adoption trends across India, pricing and driving range preferences, and generates actionable insights for policymakers, manufacturers, and infrastructure planners.

## 2. Project Objective
Build a **comprehensive end-to-end EV data analytics pipeline and interactive dashboard** to monitor and analyze EV adoption trends in India. The project lifecycle includes:
- Data Cleaning
- Feature Engineering
- SQL Data Warehouse Loading
- Analytics & Insights
- Interactive Dashboard Visualization

## 3. Tools and Technologies Used
- Python (Pandas, NumPy, Matplotlib, Seaborn, Streamlit, PyODBC)
- SQL Server
- Power BI / Streamlit Dashboard
- Libraries for data cleaning and visualization

## 4. Business Problem
As the EV market grows, companies and policymakers struggle to make informed decisions due to limited insights.  
Challenges include:
- Lack of clarity on **high and low adoption regions**
- Limited insights on **pricing trends and affordability**
- Unclear **driving range preferences**
- Uneven **demand across range categories**
- Difficulty planning **charging infrastructure and market strategies**

## 5. Target Audience
- Government / Policy Makers  
- EV Manufacturing Companies  
- Infrastructure Planners  
- Market Analysts / Researchers

## 6. System Architecture
The system captures data from multiple sources, processes it via an ETL pipeline, stores it in a SQL data warehouse, and provides an interactive dashboard for analysis.

## 7. Data Pipeline Organisation

D:\Desktop\Electric_Vehicle
├── EV_Datasets         # Raw CSV data files
├── cleaned_data        # Cleaned datasets after preprocessing
├── feature_engineer    # Feature-engineered datasets
├── Ev_python_file      # Python scripts for cleaning, feature engineering, SQL loading, dashboard
├── SQL - DB            # SQL scripts: Data warehouse, analytics queries
├── virtuaenv           # Python virtual environment
└── .idea               # IDE project files

## 8. Data Analysis & Key Insights
**Insights Generated in the Project:**
- Metro vs Non-Metro adoption trends  
- Regional adoption differences  
- EV range vs price category analysis  
- High-Range EV penetration    
- Top EV models by price  

## 9. Business Impact
- **EV adoption is higher in non-metro areas (82.1%)** → Need to expand charging stations  
- **East region has the lowest adoption (26,033 vehicles)** → Targeted incentives and awareness programs  
- **Average EV price ~₹2.7 lakh** → Focus on affordable EV models  
- **Non-metro users prefer slightly higher range (~298.9 km)** → Design higher range EVs for non-metro areas  
- **Medium and High-range EVs (33.8% each)** → Balanced demand based on price and range

## 10. Future Enhancements
- **Predictive Modeling:** Forecast EV adoption trends by region or state  
- **Computer Vision:** Analyze EV images for design or safety  
- **Infrastructure Planning:** Combine EV data with charging station locations to optimize placement

## 11. Conclusion
This project developed an **end-to-end EV analytics pipeline**, from data cleaning to interactive dashboard visualization.  
The insights help policymakers, manufacturers, and businesses make **data-driven decisions** to improve EV infrastructure, pricing strategy, and adoption across India.
