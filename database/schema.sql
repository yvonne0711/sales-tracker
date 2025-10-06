DROP DATABASE sales;
CREATE DATABASE sales;
\c sales

CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS website (
    website_id INT GENERATED ALWAYS AS IDENTITY,
    website_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (website_id)
);

CREATE TABLE IF NOT EXISTS product (
    product_id INT GENERATED ALWAYS AS IDENTITY,
    product_name VARCHAR(100) NOT NULL,
    product_url VARCHAR(255) NOT NULL,
    website_id INT NOT NULL,
    PRIMARY KEY (product_id)
);

CREATE TABLE IF NOT EXISTS subscription (
    subscription_id INT GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    desired_price DECIMAL NOT NULL,
    PRIMARY KEY (subscription_id)
);

CREATE TABLE IF NOT EXISTS price_update (
    price_update_id INT GENERATED ALWAYS AS IDENTITY,
    product_id INT NOT NULL,
    new_price DECIMAL NOT NULL,
    change_at timestamp NOT NULL,
    PRIMARY KEY (price_update_id)
);

INSERT INTO website (
    website_name
)
VALUES (
    'steam'
);

INSERT INTO USERS (
    user_name,user_email
)
VALUES (
    'test_user','b_yacquub@hotmail.co.uk'
)
