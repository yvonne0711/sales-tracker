DROP DATABASE sales;
CREATE DATABASE sales;
\c sales

CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS website (
    website_id INT GENERATED ALWAYS AS IDENTITY,
    website_name VARCHAR(255) NOT NULL,
    price_class VARCHAR(255) NOT NULL,
    discount_class VARCHAR(255),
    PRIMARY KEY (website_id)
);

CREATE TABLE IF NOT EXISTS product (
    product_id INT GENERATED ALWAYS AS IDENTITY,
    product_name VARCHAR(100) NOT NULL,
    product_url VARCHAR(255) NOT NULL,
    website_id INT NOT NULL,
    PRIMARY KEY (product_id),
    FOREIGN KEY (website_id) REFERENCES website(website_id)
);

CREATE TABLE IF NOT EXISTS subscription (
    subscription_id INT GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    desired_price DECIMAL NOT NULL,
    PRIMARY KEY (subscription_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE IF NOT EXISTS price_update (
    price_update_id INT GENERATED ALWAYS AS IDENTITY,
    product_id INT NOT NULL,
    new_price DECIMAL NOT NULL,
    change_at timestamp NOT NULL,
    PRIMARY KEY (price_update_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

INSERT INTO website (
    website_name,price_class,discount_class
)
VALUES (
    'steam','game_purchase_price price','discount_class": "discount_final_price'
);

INSERT INTO USERS (
    user_name,user_email
)
VALUES (
    'test_user','b_yacquub@hotmail.co.uk'
)
