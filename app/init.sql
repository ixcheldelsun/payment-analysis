CREATE USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';

CREATE DATABASE test;

GRANT ALL PRIVILEGES ON test.* TO 'admin'@'localhost';

USE test;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE, 
    password VARCHAR(255) NOT NULL
);

CREATE TABLE payments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user INT NOT NULL,
    amount VARCHAR(255) NOT NULL,
    date_created DATETIME NOT NULL,
    FOREIGN KEY (user) REFERENCES users(id)
);