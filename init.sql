DELETE FROM classes;
/*
in this file '-symbol is used instead of "-symbol,
because "-symbol causes unexpected errors for windows users
*/
INSERT INTO classes (class_name, value) VALUES ('When', 'Today');
INSERT INTO classes (class_name, value) VALUES ('When', 'This week');
INSERT INTO classes (class_name, value) VALUES ('When', 'This month');
INSERT INTO classes (class_name, value) VALUES ('When', 'This year');
INSERT INTO classes (class_name, value) VALUES ('When', 'More than a year');

INSERT INTO classes (class_name, value) VALUES ('Where', 'City Centre Campus');
INSERT INTO classes (class_name, value) VALUES ('Where', 'Kumpula Campus');
INSERT INTO classes (class_name, value) VALUES ('Where', 'Meilahti Campus');
INSERT INTO classes (class_name, value) VALUES ('Where', 'Viikki Campus');
