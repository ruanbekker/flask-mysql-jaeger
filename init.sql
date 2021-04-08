-- https://chartio.com/resources/tutorials/how-to-insert-if-row-does-not-exist-upsert-in-mysql/ :
CREATE DATABASE IF NOT EXISTS appdb;
CREATE TABLE IF NOT EXISTS appdb.inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL
);
INSERT IGNORE INTO appdb.inventory (id, name, category) VALUES (1, 'oakley', 'sunglasses');
INSERT IGNORE INTO appdb.inventory (id, name, category) VALUES (2, 'hurley', 'clothing');
INSERT IGNORE INTO appdb.inventory (id, name, category) VALUES (3, 'havianas', 'footwear');
