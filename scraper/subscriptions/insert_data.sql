INSERT INTO product
    (product_name, product_url, website_id)
VALUES
    ('Sonic Racing: CrossWorlds',
    'https://store.steampowered.com/app/2486820/Sonic_Racing_CrossWorlds/?snr=1_4_4__118',
    1),
    ('CloverPit',
    'https://store.steampowered.com/app/3314790/CloverPit/',
    1);

INSERT INTO price_update
    (product_id, new_price, change_at)
VALUES
    (1,30,'2025-10-2 20:15');


INSERT into subscription (
    user_id, product_id, desired_price
)
VALUES(
    1,1,0.1
);
INSERT INTO USERS (
    user_name,user_email
)
VALUES (
    'test_user2','test_user2@hotmail.co.uk'
);
INSERT into subscription (
    user_id, product_id, desired_price
)
VALUES(
    5,1,30
);