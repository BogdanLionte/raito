DROP DATABASE IF EXISTS raito;

CREATE DATABASE raito;

USE raito;

DROP TABLE IF EXISTS UserQueries;

CREATE TABLE UserQueries (
    `id` INT AUTO_INCREMENT,
    `user_email` VARCHAR(255) NOT NULL,
    `api` VARCHAR(255) NOT NULL,
    `result` MEDIUMTEXT NOT NULL,
    `sentence` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
)