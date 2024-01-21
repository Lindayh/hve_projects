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
rating INTEGER DEFAULT 1 CHECK (rating BETWEEN 1 AND 5), 
book_ID,
description VARCHAR(200),
FOREIGN KEY (book_ID) REFERENCES book(book_ID)
)

INSERT INTO review ('user', 'rating', 'book_ID', 'description') 
VALUES
('Bookworm101', 4, 2, 'Dracula is a classic vampire tale that keeps you on the edge of your seat. The atmospheric descriptions and suspenseful plot make it a timeless read.'),
('HorrorFanatic666', 2, 2, 'Dracula failed to live up to the hype for me. The intricate narrative structure and extensive diary entries felt cumbersome, detracting from the horror elements.'),
('HappyFangs', 5, 2, 'The epitome of vampire literature. Stoker''s depiction of the infamous count is chilling, leaving you captivated.'),
('DesertBookworm', 4, 5, 'A masterpiece of sci-fi with a richly constructed world and compelling characters. It keeps you hooked till the very end.'),
('NebulaNerd', 1, 5, 'An overrated snoozefest. The plot is convoluted, the characters are bland, and the pacing is torturous. Avoid at all costs.'),
('WhimsicalAlien', 3, 5, 'Dune has a fascinating world-building and intricate plot, but the pacing can be sluggish at times.'),
('Eldritch_Enthusiast', 5, 1, 'This book will transport you to a realm of cosmic terrors. His prose is haunting and imagery is unsettling. Only for the brave!'),
('Purple_Blob_Reader', 1, 1, 'A confusing mess. The prose is dense and stories are convoluted. A waste of time.'),
('Cthulhu_Lover', 3, 1, 'The Necronomicon is a paradox. His Cthulhu mythos is captivating, but his execution is lacking. Intriguing but frustrating'),
('CosmicCosmophile', 4, 4, 'A mind-bending journey into the depths of a captivating universe. While some plot elements may leave you scratching your head, the overall experience stimulating.'),
('LovecraftianLore', 2, 4, 'This is a convoluted mess of confusing science and philosophical musings. While the prose is engaging at times, the story is ultimately unsatisfying and leaves more questions than answers.'),
('EldritchEnigma', 3, 4, 'It is a mixed bag of brilliance and bewilderment. The exploration of humanity''s place in the cosmos is thought-provoking, but the plot can be difficult to follow and the characters are often underdeveloped.'),
('VictorianVoyeur', 5, 3, 'Wilde''s masterpiece, a captivating tale of beauty, vanity, and the consequences of a Faustian bargain. The prose and insightful observations on human nature make this a must-read'),
('DecadenceDweller', 3, 3, 'Fascinating work but not without its flaws. His characters are often underdeveloped and his prose can be overly theatrical.'),
('HistoryPoet', 5, 18, 'A masterpiece! Chaucer''s tales provide an invaluable glimpse into medieval life, blending humor, satire, and profound social commentary.'),
('MuseMagnet', 3, 18, 'Some stories captivate, while others drag. The language is a challenge, but the tales offer a mosaic of medieval society.');


INSERT INTO review ('user', 'rating', 'book_ID', 'description')
VALUES ('username', 6, 168, 'Review')

-- DROP TABLE book;
DROP table review
DROP TABLE review_test

SELECT * FROM review
SELECT * FROM book

ALTER TABLE review
ADD CONSTRAINT check_rating_range CHECK (rating BETWEEN 1 AND 5);

DELETE FROM review
WHERE reviewID>=44

DELETE FROM book
WHERE title like "%title%"

DELETE FROM book
WHERE book_ID >= 183

DELETE FROM review
WHERE reviewID LIKE 
(SELECT max(reviewID) FROM review) 

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


-- VG - GET /books visar all böcker + deras genomslittiga reviews
SELECT b.book_ID, b.title, b.author, b.year, b.genre, b.summary, round(avg(r.rating),2) as "avg_rating"
FROM book b
INNER JOIN review r ON b.book_ID LIKE r.book_ID
GROUP BY b.title

SELECT b.book_ID, b.title, b.author, b.year, b.genre, b.summary, round(avg(r.rating),2) as "avg_rating"
FROM book b
LEFT JOIN review r USING (book_ID)
WHERE b.book_ID LIKE 1
GROUP BY b.title
ORDER BY b.book_ID

