DROP TABLE IF EXISTS userData;
DROP TABLE IF EXISTS eventsData;
DROP TABLE IF EXISTS userProfile;
CREATE TABLE userData (
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	events_joined TEXT
);

CREATE TABLE eventsData (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tipo_evento text NOT NULL,
	limite int NOT NULL,
	timest TEXT UNIQUE NOT NULL,
	latitude TEXT NOT NULL,
	longitude TEXT NOT NULL
);

CREATE TABLE userProfile(
	nome text NOT NULL,
	idade int NOT NULL,
	sexo text NOT NULL,
	score int NOT NULL,
	bpm int NOT NULL,
	peso FLOAT NOT NULL,
	altura FLOAT NOT NULL
);

CREATE TABLE products(
	nomeProd text NOT NULL,
	preco FLOAT NOT NULL,
);

CREATE TABLE kart(
	userId  text NOT NULL,
	productId  FLOAT NOT NULL,
);

CREATE TABLE Orders(
	userId  text NOT NULL,
	productId  FLOAT NOT NULL,
);