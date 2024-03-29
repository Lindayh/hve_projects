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

INSERT INTO person (name, age, phone_nr, country) VALUES
('Ming Lee', 32, '123456789', 'China'),
('Luis Rodriguez', 25, '987654321', 'Mexico'),
('Sofia Garcia', 40, '555123456', 'Spain'),
('Hiro Tanaka', 28, '999888777', 'Japan'),
('Raj Patel', 35, '777888999', 'India');

INSERT INTO person (name, age, phone_nr, country) VALUES 
('Maria Garcia', 32, '123456789', 'Spain'),
('Luisa Rossi', 45, '987654321', 'Italy'),
('Miguel Santos', 28, '555444333', 'Portugal'),
('Javier Hernandez', 40, '999888777', 'Mexico'),
('Sofia Costa', 27, '111222333', 'Brazil');

INSERT INTO person (name, age, phone_nr, country) VALUES
('Elena Martinez', 28, '+1234567890', 'Spain'),
('Mateo Silva', 35, '+2345678901', 'Brazil'),
('Sophie Dubois', 42, '+3456789012', 'France'),
('Luca Rossi', 31, '+4567890123', 'Italy'),
('Hans Schmidt', 29, '+5678901234', 'Germany'),
('Isabella Santos', 26, '+6789012345', 'Brazil'),
('Liam Nguyen', 39, '+7890123456', 'Vietnam'),
('Olivia Kim', 33, '+8901234567', 'South Korea'),
('Lucas Alves', 36, '+9012345678', 'Portugal'),
('Emma Tan', 45, '+0123456789', 'Singapore'),
('Gabriel Lee', 27, '+1123456789', 'South Korea'),
('Mia Wang', 30, '+2123456789', 'China'),
('David Garcia', 32, '+3123456789', 'Spain'),
('Sophia Silva', 29, '+4123456789', 'Brazil'),
('Leonardo Chen', 34, '+5123456789', 'China'),
('Amelia Wong', 37, '+6123456789', 'Singapore'),
('Matteo Russo', 41, '+7123456789', 'Italy'),
('Eva Lopez', 38, '+8123456789', 'Spain'),
('Julian Kim', 44, '+9123456789', 'South Korea'),
('Alessia Costa', 40, '+0123456789', 'Italy');



INSERT INTO user (username, email, password) VALUES
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'abc123'),
('alexander', 'alex@example.com', 'securepwd'),
('emily_jones', 'emily@example.com', 'qwerty'),
('michael_brown', 'michael@example.com', 'letmein');