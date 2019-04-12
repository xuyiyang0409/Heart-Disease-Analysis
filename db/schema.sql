-- Raw data table, contains all attributes from raw data
CREATE TABLE Rawdata(
    age NUMERIC,
    sex NUMERIC,
    cp NUMERIC,
    trestbps NUMERIC,
    chol NUMERIC,
    fbs NUMERIC,
    restecg NUMERIC,
    thalach NUMERIC,
    exang NUMERIC,
    oldpeak NUMERIC,
    slope NUMERIC,
    ca NUMERIC,
    thal NUMERIC,
    target NUMERIC
);

-- Important factors, requirement 2, initially set 5 factors
CREATE TABLE Impfactor(
    factor1 VARCHAR(20),
    factor2 VARCHAR(20),
    factor3 VARCHAR(20),
    factor4 VARCHAR(20),
    factor5 VARCHAR(20)
);

-- Prediction function weights, associated with important factor, initially set 5 factors
CREATE TABLE Predict(
    weifactor1 NUMERIC,
    weifactor2 NUMERIC,
    weifactor3 NUMERIC,
    weifactor4 NUMERIC,
    weifactor5 NUMERIC,
    weifactor6 NUMERIC
);