CREATE TABLE book(
ISBN TEXT UNIQUE,
title TEXT,
author TEXT,
summary TEXT,
genre TEXT,
PRIMARY KEY (ISBN)
);

CREATE TABLE review(
reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
rating INTEGER, -- from 1 to 5 ?
description VARCHAR(200)
)