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
    user_id INTEGER REFERENCES users,
    upload_time INTEGER,
    edit_time INTEGER
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
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

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    image BLOB
);

CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_upload_time ON items(upload_time);
CREATE INDEX idx_items_edit_time ON items(edit_time);
CREATE INDEX idx_claims_item_id ON claims(item_id);
CREATE INDEX idx_claims_user_id ON claims(user_id);
CREATE INDEX idx_item_classes_item_id ON item_classes(item_id);
CREATE INDEX idx_item_classes_name_value ON item_classes(item_class_name, value);
CREATE INDEX idx_classes_class_name_value ON classes(class_name, value);
CREATE INDEX idx_images_item_id ON images(item_id);
