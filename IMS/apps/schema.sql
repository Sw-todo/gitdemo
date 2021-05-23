-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS good;

CREATE TABLE user (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (userid)
);

CREATE TABLE good (
  goodid INTEGER PRIMARY KEY AUTOINCREMENT,
  goodname TEXT UNIQUE NOT NULL,
  goodamount INTEGER NOT NULL,
  goodprice FLOAT NOT NULL
);

INSERT INTO user VALUES (1, 'myaron', '123456');
INSERT INTO good VALUES (1, 'good1', 12, 9.5);
INSERT INTO good VALUES (2, 'good2', 23, 102);
INSERT INTO good VALUES (3, 'good3', 23, 102);
INSERT INTO good VALUES (4, 'good4', 23, 102);
INSERT INTO good VALUES (5, 'good5', 23, 102);
