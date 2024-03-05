CREATE DATABASE LogDatabase;
GO

USE LogDatabase;
GO

CREATE TABLE log_table (
    id INT PRIMARY KEY IDENTITY(1,1),
    timestamp DATETIME NOT NULL,
    log_level VARCHAR(50),
    message TEXT
);
GO
