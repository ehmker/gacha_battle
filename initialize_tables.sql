DROP TABLE IF EXISTS Creatures;

DROP TABLE IF EXISTS Fight_Results;

DROP TABLE IF EXISTS Transactions;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    last_character_roll TimeStamp,
    has_started boolean DEFAULT false
);

CREATE TABLE Creatures (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES Users(id),
    creature_name VARCHAR(50) NOT NULL,
    base_hp INTEGER NOT NULL,
    base_atk INTEGER NOT NULL,
    base_def INTEGER NOT NULL
);

CREATE TABLE Fight_Results(
    id SERIAL PRIMARY KEY,
    aggressor_id INTEGER NOT NULL REFERENCES Users(id),
    target_id INTEGER NOT NULL REFERENCES Users(id),
    winner_id INTEGER NOT NULL REFERENCES Users(id)
);

CREATE TABLE Transactions(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users(id),
    note VARCHAR(255),
    amount NUMERIC
)