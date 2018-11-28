DROP TABLE IF EXISTS userData;

CREATE TABLE userData (
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);