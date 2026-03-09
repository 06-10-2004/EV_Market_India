-- DATA_WAREHOUSE

-- DIMENSION TABLES

CREATE TABLE Dim_Location (
    LocationID INT IDENTITY(1,1) PRIMARY KEY,
    State NVARCHAR(100),
    City NVARCHAR(100),
    Region NVARCHAR(50),
    Metro_Flag INT,
    High_Adoption_State_Flag INT
);

CREATE TABLE Dim_Model (
    ModelID INT IDENTITY(1,1) PRIMARY KEY,
    Make NVARCHAR(100),
    Model NVARCHAR(100),
    EV_Class NVARCHAR(50),
    Range_Category NVARCHAR(50),
    Price_Category NVARCHAR(50)
);

CREATE TABLE Dim_Date (
    DateID INT IDENTITY(1,1) PRIMARY KEY,
    Year INT,
    Quarter INT,
    Month INT
);

-- FACT TABLES

CREATE TABLE Fact_EV (
    FactID INT IDENTITY(1,1) PRIMARY KEY,
    LocationID INT NOT NULL,
    ModelID INT NOT NULL,
    DateID INT NOT NULL,
    Electric_Range FLOAT,
    Base_MSRP FLOAT,
    Vehicle_Age INT,
    High_Range_Flag INT,
    Premium_Flag INT,

    FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID),
    FOREIGN KEY (ModelID) REFERENCES Dim_Model(ModelID),
    FOREIGN KEY (DateID) REFERENCES Dim_Date(DateID)
	);

-- LOAD DATA FROM EXISTING TABLES

-- LOCATION VALUES:

INSERT INTO Dim_Location (State, City, Region, Metro_Flag, High_Adoption_State_Flag)
SELECT DISTINCT
    State,
    City,
    Region,
    Metro_Flag,
    High_Adoption_State_Flag
FROM EV_Database.dbo.EV_India_FE;

-- MODEL VALUES:

INSERT INTO Dim_Model (Make, Model, EV_Class, Range_Category, Price_Category)
SELECT DISTINCT
    Make,
    Model,
    EV_Class,
    Range_Category,
    Price_Category
FROM EV_Database.dbo.EV_Model_FE;

-- DATE VALUES:

INSERT INTO Dim_Date (Year, Quarter, Month)
SELECT DISTINCT
    Model_Year,
    1 AS Quarter,
    1 AS Month
FROM EV_Database.dbo.EV_Model_FE;

-- LOAD VALUES TO FACT TABLE:

INSERT INTO Fact_EV (
    LocationID,
    ModelID,
    DateID,
    Electric_Range,
    Base_MSRP,
    Vehicle_Age,
    High_Range_Flag,
    Premium_Flag
)
SELECT
    dl.LocationID,
    dm.ModelID,
    dd.DateID,
    m.Electric_Range,
    m.Base_MSRP,
    m.Vehicle_Age,
    m.High_Range_Flag,
    m.Premium_Flag
FROM EV_Database.dbo.EV_Model_FE m
JOIN EV_Database.dbo.EV_India_FE i
    ON m.DOL_Vehicle_ID = i.DOL_Vehicle_ID
JOIN Dim_Model dm
    ON m.Make = dm.Make
   AND m.Model = dm.Model
JOIN Dim_Location dl
    ON i.State = dl.State
   AND i.City = dl.City
JOIN Dim_Date dd
    ON m.Model_Year = dd.Year;