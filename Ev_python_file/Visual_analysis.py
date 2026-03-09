import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc

sns.set_theme(style="whitegrid")

def run_visual_analysis():

    figures = []

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=Hari6104\\MSSQLSERVER1;"
        "DATABASE=EV_Database;"
        "Trusted_Connection=yes;"
    )

    # 1 Metro vs Non Metro
    query = """
    SELECT 
    COUNT(CASE WHEN dl.Metro_Flag = 1 THEN 1 END) Metro,
    COUNT(CASE WHEN dl.Metro_Flag = 0 THEN 1 END) Non_Metro
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(5,4))
    ax.pie(df.iloc[0], labels=["Metro","Non Metro"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Metro vs Non-Metro EV Adoption")
    figures.append(fig)

    # 2 Region EV Adoption
    query = """
    SELECT dl.Region, COUNT(*) Total_EV
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    GROUP BY dl.Region
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=df, x="Region", y="Total_EV", ax=ax)

    for container in ax.containers:
        ax.bar_label(container)

    ax.set_title("EV Adoption by Region")
    figures.append(fig)

    # 3 Average Range Metro vs Non-Metro
    query = """
    SELECT dl.Metro_Flag, AVG(fv.Electric_Range) Avg_Range
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    GROUP BY dl.Metro_Flag
    """
    df = pd.read_sql(query, conn)
    df["Metro_Flag"] = df["Metro_Flag"].map({1:"Metro",0:"Non-Metro"})

    fig, ax = plt.subplots(figsize=(5,4))
    sns.barplot(data=df, x="Metro_Flag", y="Avg_Range", ax=ax)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f")

    ax.set_title("Average EV Range")
    figures.append(fig)

    # 4 Top EV Models by Price
    query = """
    SELECT TOP 10 dm.Model, MAX(fv.Base_MSRP) Price
    FROM Fact_EV fv
    JOIN Dim_Model dm ON fv.ModelID = dm.ModelID
    GROUP BY dm.Model
    ORDER BY Price DESC
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(df["Price"], df["Model"])

    for i in range(len(df)):
        ax.text(df["Price"][i], df["Model"][i], f"{int(df['Price'][i])}")

    ax.set_title("Top EV Models by Price")
    figures.append(fig)

    # 5 Cost per Range by Region
    query = """
    SELECT dl.Region, AVG(Base_MSRP/Electric_Range) Cost_Per_Range
    FROM Fact_EV f
    JOIN Dim_Location dl ON f.LocationID = dl.LocationID
    GROUP BY dl.Region
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=df, x="Region", y="Cost_Per_Range", ax=ax)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")

    ax.set_title("Cost per Range by Region")
    figures.append(fig)

    # 6 Range Category Market Share
    query = """
    SELECT Range_Category, COUNT(*) Total
    FROM Fact_EV f
    JOIN Dim_Model dm ON f.ModelID = dm.ModelID
    GROUP BY Range_Category
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(5,4))
    ax.pie(df["Total"], labels=df["Range_Category"], autopct="%1.1f%%")
    ax.set_title("Range Category Share")
    figures.append(fig)

    # 7 Lowest EV Adoption States
    query = """
    SELECT TOP 10 l.State, COUNT(*) Total_EV
    FROM Fact_EV f
    JOIN Dim_Location l ON f.LocationID = l.LocationID
    GROUP BY l.State
    ORDER BY Total_EV ASC
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=df, x="Total_EV", y="State", ax=ax)

    for container in ax.containers:
        ax.bar_label(container)

    ax.set_title("Lowest EV Adoption States")
    figures.append(fig)

    # 8 Premium EV Adoption
    query = """
    SELECT dl.Metro_Flag, fv.Premium_Flag, COUNT(*) Total
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    GROUP BY dl.Metro_Flag, fv.Premium_Flag
    """
    df = pd.read_sql(query, conn)

    df["Metro_Flag"] = df["Metro_Flag"].map({1:"Metro",0:"Non-Metro"})
    df["Premium_Flag"] = df["Premium_Flag"].map({1:"Premium",0:"Non-Premium"})

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=df, x="Metro_Flag", y="Total", hue="Premium_Flag", ax=ax)

    for container in ax.containers:
        ax.bar_label(container)

    ax.set_title("Premium EV Adoption")
    figures.append(fig)

    # 9️⃣ Vehicle Age by Region
    query = """
    SELECT 
        dl.Region,
        AVG(fv.Vehicle_Age) AS Avg_Vehicle_Age
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    GROUP BY dl.Region
    ORDER BY Avg_Vehicle_Age DESC
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="Region", y="Avg_Vehicle_Age", ax=ax)

    # Annotate bars with integer values (no .00)
    for container in ax.containers:
        # cast to int directly
        ax.bar_label(container, labels=[str(int(x)) for x in container.datavalues])

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_ylabel("Average Vehicle Age (Years)")
    ax.set_title("Average EV Vehicle Age by Region")

    figures.append(fig)

    # 10 High Range EV Percentage by State
    query = """
    SELECT dl.State,
    100.0 * SUM(fv.High_Range_Flag) / COUNT(*) High_Range_Percentage
    FROM Fact_EV fv
    JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
    GROUP BY dl.State
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(7,4))
    sns.barplot(data=df, x="High_Range_Percentage", y="State", ax=ax)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")

    ax.set_title("High Range EV % by State")
    figures.append(fig)

    # 11 EV Price Trend
    query = """
    SELECT dd.Year, AVG(fv.Base_MSRP) Avg_Price
    FROM Fact_EV fv
    JOIN Dim_Date dd ON fv.DateID = dd.DateID
    GROUP BY dd.Year
    ORDER BY dd.Year
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(7,4))
    sns.lineplot(data=df, x="Year", y="Avg_Price", marker="o", ax=ax)

    for x,y in zip(df["Year"], df["Avg_Price"]):
        ax.text(x,y,f"{int(y)}",ha="center",va="bottom")

    ax.set_title("EV Price Trend Over Years")
    figures.append(fig)

    conn.close()