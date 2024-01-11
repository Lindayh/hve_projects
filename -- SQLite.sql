CREATE DATABASE bookReviews.db;

CREATE TABLE book(
ISBN TEXT UNIQUE,
title TEXT,
author TEXT,
year VARCHAR(4),
genre TEXT,
summary TEXT,
PRIMARY KEY (ISBN)
);

CREATE TABLE review(
reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
ISBN TEXT UNIQUE,
rating INTEGER CHECK (rating <= 5), -- from 1 to 5 ?
description VARCHAR(200),
FOREIGN KEY (ISBN) REFERENCES book(ISBN)
)

DROP TABLE book;
DROP table review

INSERT INTO book 
VALUES 
('9780575081574','Necronomicon','H.P. Lovecraft','2008','Horror','Collection of tales that blend elements of horror, science fiction, and cosmic terror'),
('9780141199337','Dracula','Bram Stoker','2012','Horror','When Jonathan Harker visits Count Dracula in Transylvania , he makes a horrifying discovery. Soon afterwards, a number of disturbing incidents unfold in England'),
('9781789559620','The Picture of Dorian Gray','Oscar Wilde','2021','Dorian, fearful of age and the subsequent fading of his beauty, expresses a wish: that a glorious oil portrait of him suffers the burden of age, and not him.','Fiction'),
('9780765328038','Echopraxia','Peter Watts','2015','A field biologist is drawn into a journey to the center of the solar system with a group of strange individuals. They are seeking a meeting with "The Angels of the Asteroids," which could lead to a major evolutionary breakthrough.','Sci-Fi'),
('9780340960196','Dune','Frank Herbert','2015','In a universe where the most valuable spice "melange" is essential for interstellar travel, the noble House Atreides is betrayed and forced to fight for survival on the desert planet Arrakis, where the spice is produced.','Sci Fi');

