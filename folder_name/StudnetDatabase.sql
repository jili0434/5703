DROP TABLE IF EXISTS 
    Students,
    Values,
    Career_orientation,
    Personality,
    Creative_Thinking,
    Family_Info
CASCADE;

-- create tabkes
CREATE TABLE Students (
    Identifier INT PRIMARY KEY,
    First_letter_surname CHAR(1),
    Gender CHAR(1),
    Age INT,
    First_language VARCHAR(50),
    Other_language VARCHAR(50),
    Country_born VARCHAR(50),
    Current_country VARCHAR(50),
    Current_city VARCHAR(50),
    Type_of_school VARCHAR(50),
    Secondary_qualification VARCHAR(50),
    Work_experience VARCHAR(50),
    Dream_career VARCHAR(50),
    Academic INT,
    Subject_1 INT,
    Subject_2 INT,
    Subject_3 INT
);

CREATE TABLE Values (
    No INT PRIMARY KEY,
    Hedonism INT,
    Power_and_Status INT,
    Altruism INT,
    Learning_and_Achievement INT,
    Finance INT,
    Security INT,
    FOREIGN KEY (No) REFERENCES Students(Identifier)
);


CREATE TABLE Career_Orientation (
    No INT PRIMARY KEY,
    Artistic INT,
    Social INT,
    Investigative INT,
    Conventional INT,
    Enterprising INT,
    Realistic INT,
    FOREIGN KEY (No) REFERENCES Students(Identifier)
);

CREATE TABLE Personality (
    No INT PRIMARY KEY,
    Extrovert INT,
    Introvert INT,
    Sensing INT,
    Intuition_N INT,
    Thinking INT,
    Feeling INT,
    Judging INT,
    Perceiving INT,
	Result_ CHAR(4),
    FOREIGN KEY (No) REFERENCES Students(Identifier)
);

CREATE TABLE Creative_Thinking (
    No INT PRIMARY KEY,
    Q1 INT,
    Q2 INT,
    Q3 INT,
    FOREIGN KEY (No) REFERENCES Students(Identifier)
);

CREATE TABLE Family_Info (
    No INT PRIMARY KEY,
    Father_education VARCHAR(100),
    Mother_education VARCHAR(100),
    Father_occupation VARCHAR(100),
    Mother_occupation VARCHAR(100),
    Annual_budget_usd VARCHAR(100),
    Preferred_FoE_1 VARCHAR(100),
    Preferred_FoE_2 VARCHAR(100),
    Preferred_FoE_3 VARCHAR(100),
    Notes TEXT,
    Concern TEXT,
    Support TEXT,
    Preferred_country VARCHAR(50),
    FOREIGN KEY (No) REFERENCES Students(Identifier)
);

