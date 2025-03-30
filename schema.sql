CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    item_name TEXT UNIQUE,
    description TEXT,
    user_id INTEGER REFERENCES users
);
