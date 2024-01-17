CREATE DATABASE bookReviews.db;

CREATE TABLE book(
book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
author TEXT,
year VARCHAR(4),
genre TEXT,
summary TEXT
);

CREATE TABLE review(
reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
rating INTEGER DEFAULT 0 CHECK (rating <= 5), 
book_ID,
description VARCHAR(200),
FOREIGN KEY (book_ID) REFERENCES book(book_ID)
)

DROP TABLE book;
DROP table review


SELECT * FROM book;
SELECT * FROM review;

DELETE FROM book
WHERE title like "Pytest_title"

INSERT INTO book ('title','author','year','genre','summary')
VALUES 
('Necronomicon','H.P. Lovecraft','2008','Horror','Collection of tales that blend elements of horror, science fiction, and cosmic terror'),
('Dracula','Bram Stoker','2012','Horror','When Jonathan Harker visits Count Dracula in Transylvania , he makes a horrifying discovery. Soon afterwards, a number of disturbing incidents unfold in England'),
('The Picture of Dorian Gray','Oscar Wilde','2021','Fiction','Dorian, fearful of age and the subsequent fading of his beauty, expresses a wish: that a glorious oil portrait of him suffers the burden of age, and not him.'),
('Echopraxia','Peter Watts','2015','Sci-Fi','A field biologist is drawn into a journey to the center of the solar system with a group of strange individuals. They are seeking a meeting with "The Angels of the Asteroids," which could lead to a major evolutionary breakthrough.'),
('Dune','Frank Herbert','2015','Sci-Fi','In a universe where the most valuable spice "melange" is essential for interstellar travel, the noble House Atreides is betrayed and forced to fight for survival on the desert planet Arrakis, where the spice is produced.');


INSERT INTO book ('title','author','year','genre','summary')
VALUES 
('Random Book','Writer McScribbly','425 BCE','Classics','My nice summary');

SELECT review.reviewID, review.user, book.title, review.book_ID, review.description
FROM review
INNER JOIN book ON book.book_ID like review.book_ID
WHERE review.book_ID LIKE 14




SELECT review.book_ID, book.title, book.author, round(avg(review.rating),2) as 'Average review'
FROM review
INNER JOIN book ON book.book_ID like review.book_ID
GROUP BY review.book_ID
ORDER BY avg(review.rating) DESC
LIMIT 5