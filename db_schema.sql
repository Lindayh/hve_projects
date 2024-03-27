-- SQLite
CREATE TABLE "person"
(
 personID INTEGER PRIMARY KEY AUTOINCREMENT, 
 name text,
 age INT,
 phone_nr text,
country text,
img text
)

CREATE TABLE "user"
(
userID INTEGER PRIMARY KEY AUTOINCREMENT, 
email text,
password text
)


INSERT INTO person ("name", "age", "phone_nr", "country") VALUES 
( 'John Doe', '30', '123-456-7890', 'USA'),
( 'Jane Smith', '25', '987-654-3210', 'Canada'),
( 'David Lee', '40', '555-123-4567', 'UK'),
( 'Maria Garcia', '35', '444-555-6666', 'Spain'),
('Ahmed Khan', '28', '777-888-9999', 'Pakistan'),
('John Smith', '33', '123-456-2390', 'UK'),
('John O''Connor', '33', '555-123-4567', 'Ireland');

INSERT INTO user (username, email, password) VALUES
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'abc123'),
('alexander', 'alex@example.com', 'securepwd'),
('emily_jones', 'emily@example.com', 'qwerty'),
('michael_brown', 'michael@example.com', 'letmein');