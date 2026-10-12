CREATE DATABASE student_portfolio;

USE student_portfolio;

-- Students table stores student registration, login, and profile details.
CREATE TABLE Students (
    -- Assigned by backend/register.py so the first missing ID is reused.
    Student_ID INT PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Student_Class VARCHAR(10) NOT NULL,
    Section VARCHAR(10) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15) NOT NULL,
    Career_Interest VARCHAR(100),
    Registration_Date DATE,
    Password VARCHAR(255) NOT NULL
);

-- Admin table stores administrator login details.
CREATE TABLE Admin (
    Admin_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL
);

-- Academics table stores academic marks and exam records of students.
CREATE TABLE Academics (
    Record_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NOT NULL,
    Subject VARCHAR(50) NOT NULL,
    Exam_Type VARCHAR(50) NOT NULL,
    Marks_Obtained INT NOT NULL,
    Maximum_Marks INT NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Activities table stores extracurricular and co-curricular activity records.
CREATE TABLE Activities (
    Activity_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NOT NULL,
    Activity_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Level VARCHAR(50) NOT NULL,
    Organizer VARCHAR(100),
    Activity_Date DATE NOT NULL,
    Description VARCHAR(255),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Achievements table stores awards, positions, and competition records.
CREATE TABLE Achievements (
    Achievement_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Competition VARCHAR(100),
    Position VARCHAR(50),
    Organization VARCHAR(100),
    Achievement_Date DATE NOT NULL,
    Certificate_ID VARCHAR(50),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Volunteer table stores volunteer work and service hour records.
CREATE TABLE Volunteer (
    Volunteer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NOT NULL,
    Organization VARCHAR(100) NOT NULL,
    Role VARCHAR(100) NOT NULL,
    Hours INT NOT NULL,
    Volunteer_Date DATE NOT NULL,
    Description VARCHAR(255),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Goals table stores student goals, status, and deadlines.
CREATE TABLE Goals (
    Goal_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NOT NULL,
    Goal_Title VARCHAR(100) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    Deadline DATE,
    Description VARCHAR(255),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);
