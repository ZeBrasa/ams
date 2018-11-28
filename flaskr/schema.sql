DROP TABLE IF EXISTS userData;
DROP TABLE IF EXISTS eventsData;
DROP TABLE IF EXISTS userProfile;
CREATE TABLE userData (
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE eventsData (
	id_events int NOT NULL,
	tipo_evento text NOT NULL,
	limite int NOT NULL,
	timest TEXT UNIQUE NOT NULL,
	latitude TEXT NOT NULL,
	longitude TEXT NOT NULL
);

CREATE TABLE userProfile(
	nome text NOT NULL,
	idade int NOT NULL,
	score int NOT NULL,
	peso FLOAT NOT NULL,
	altura FLOAT NOT NULL
);