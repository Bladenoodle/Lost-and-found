CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    item_name TEXT UNIQUE,
    description TEXT,
    status TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER UNIQUE REFERENCES users,
    contact_info TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    class_name TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    item_class_name TEXT,
    value TEXT
);