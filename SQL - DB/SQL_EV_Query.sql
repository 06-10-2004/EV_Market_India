-- ELECTRIC VEHICLE DATA INSIGHTS

select * from Fact_EV;
select * from Dim_Location;
select * from Dim_Date;
select * from Dim_Model;

-- " INFRASTRUCTURE CHALLENGE: "

-- Metro vs Non-Metro Adoption : Is EV adoption concentrated only in metro cities?

select 
   COUNT(case when dl.Metro_Flag = 1 then 1 end) as Metro_flag,
   COUNT(case when dl.Metro_Flag = 0 then 1 end) as Non_Metro_flag,
cast(round(
   100.0 * count(case when  dl.Metro_Flag = 1 then 1 end)/ COUNT(*),2)
   AS DECIMAL(5,2)
   ) as Metro_percentage,
cast(round(
   100.0 * count(case when  dl.Metro_Flag = 0 then 1 end)/ COUNT(*),2)
   AS DECIMAL(5,2)
   ) as Non_Metro_percentage
from Fact_EV as fv
join Dim_Location as dl
    on fv.LocationID = dl.LocationID;

-- Region Wise Adoption : which region have lowest EV adoption?

SELECT 
    dl.Region,
    COUNT(*) AS Total_EV,
    CAST(ROUND(100.0 * COUNT(*) /SUM(COUNT(*))OVER(),2) AS DECIMAL(5,2)) AS Adoption_Percentage
FROM Fact_EV fv
JOIN Dim_Location dl 
    ON fv.LocationID = dl.LocationID
GROUP BY dl.Region
ORDER BY Total_EV ASC;

-- Avg Range: Metro vs Non-Metro : Do non-metro areas prefer higher-range EVs? 

SELECT dl.Metro_Flag, 
    ROUND(AVG(fv.Electric_Range),2) AS Avg_Range 
FROM Fact_EV fv 
JOIN Dim_Location dl 
ON fv.LocationID = dl.LocationID
GROUP BY dl.Metro_Flag;

-- " COST CHALLENGE: "

--  What is the distribution of EVs across price categories?

SELECT 
    dm.Price_Category,
    COUNT(*) AS Total_EV
FROM Fact_EV fv
JOIN Dim_Model dm ON fv.ModelID = dm.ModelID
GROUP BY dm.Price_Category
ORDER BY Total_EV DESC;

--  Is premium EV adoption limited to metro cities?

SELECT 
    dl.Metro_Flag,
    fv.Premium_Flag,
    COUNT(*) AS Total_EV
FROM Fact_EV fv
JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
GROUP BY dl.Metro_Flag, fv.Premium_Flag
ORDER BY dl.Metro_Flag asc;

-- Which regions have the highest EV cost per driving range?

SELECT 
    dl.Region,
    CAST(ROUND(AVG(f.Base_MSRP),2) AS DECIMAL(10,2)) AS Avg_EV_Price,
    CAST(ROUND(AVG(f.Electric_Range),2) AS DECIMAL(10,2)) AS Avg_Range,
    CAST(ROUND(AVG(f.Base_MSRP / f.Electric_Range),2) AS DECIMAL(10,2)) AS Avg_Price_Per_Range
FROM Fact_EV f
JOIN Dim_Location dl
    ON f.LocationID = dl.LocationID
GROUP BY dl.Region
ORDER BY Avg_Price_Per_Range DESC;


-- " BATTERY AND RANGE CHALLENGE: "

-- Which range category dominates the Indian EV market?
   
SELECT 
    Range_Category,
    COUNT(*) AS Total_Vehicles,
    cast(round(AVG(Base_MSRP),2) AS DECIMAL(10,2)) AS Avg_Price,
    cast(round(AVG(Electric_Range),2) AS DECIMAL(10,2)) AS Avg_Range
FROM Fact_EV f
JOIN Dim_Model dm
    ON f.ModelID = dm.ModelID
GROUP BY Range_Category
ORDER BY Avg_Price DESC;

-- Do low-adoption states rely more on high-range EVs?

SELECT 
    dl.State,
    COUNT(*) AS Total_EV,
    cast(ROUND(100.0 * SUM(fv.High_Range_Flag) / COUNT(*),2)AS DECIMAL(10,2)) AS High_Range_Percentage
FROM Fact_EV fv
JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
GROUP BY dl.State
ORDER BY Total_EV ASC;

-- " CHARGING TIME: "

--  What percentage of EVs are classified as high-range?

SELECT 
    COUNT(*) AS Total_EV,
    SUM(High_Range_Flag) AS High_Range_Count,
    cast(ROUND(100.0 * SUM(High_Range_Flag) / COUNT(*),2)AS DECIMAL(10,2)) AS High_Range_Percentage
FROM Fact_EV;

-- " SAFETY AND VEHICLE AGE: "

-- What is the average vehicle age across regions?

SELECT 
    dl.Region,
    ROUND(AVG(fv.Vehicle_Age),2) AS Avg_Vehicle_Age
FROM Fact_EV fv
JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
GROUP BY dl.Region
ORDER BY Avg_Vehicle_Age DESC;

-- Are newer EVs concentrated in metro cities?

SELECT 
    dl.Metro_Flag,
    ROUND(AVG(fv.Vehicle_Age),2) AS Avg_Vehicle_Age
FROM Fact_EV fv
JOIN Dim_Location dl ON fv.LocationID = dl.LocationID
GROUP BY dl.Metro_Flag;

-- " EV CHARGING TIME: "

-- High range EV % by state

SELECT 
    dl.State,
    COUNT(*) AS Total_EVs,
    SUM(fv.High_Range_Flag) AS High_Range_Count,
    CAST(ROUND(100.0 * SUM(fv.High_Range_Flag) / COUNT(*), 2) AS DECIMAL(5,2)) AS High_Range_Percentage
FROM Fact_EV fv
JOIN Dim_Location dl
    ON fv.LocationID = dl.LocationID
GROUP BY dl.State
ORDER BY High_Range_Percentage DESC;

-- " GEOGRAPHY OVER TIME: "

-- Which states have the lowest EV adoption?

SELECT TOP 10
    l.State,
    COUNT(*) AS Total_EV
FROM Fact_EV f
JOIN Dim_Location l ON f.LocationID = l.LocationID
GROUP BY l.State
ORDER BY Total_EV ASC;


-- Average EV Price per State
SELECT 
    dl.State,
    COUNT(*) AS Total_EVs,
    ROUND(AVG(fv.Base_MSRP), 2) AS Avg_EV_Price
FROM Fact_EV fv
JOIN Dim_Location dl
    ON fv.LocationID = dl.LocationID
GROUP BY dl.State
ORDER BY Avg_EV_Price DESC;

-- how EV adoption has grown year-over-year

SELECT 
    dd.Year,
    COUNT(*) AS Total_EVs,
    ROUND(AVG(fv.Base_MSRP), 2) AS Avg_EV_Price
FROM Fact_EV fv
JOIN Dim_Date dd ON fv.DateID = dd.DateID
GROUP BY dd.Year
ORDER BY dd.Year;