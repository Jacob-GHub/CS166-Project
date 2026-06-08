DELETE FROM shipment;

DELETE FROM payment;

DELETE FROM bid;

DELETE FROM auction;

DELETE FROM item;

DELETE FROM users;

INSERT INTO
  users (
    login,
    password,
    phone_num,
    address,
    role,
    favorite_category
  )
VALUES
  (
    'admin1',
    'admin123',
    '555-000-0001',
    '1 Admin Plaza, Sacramento CA',
    'Admin',
    NULL
  ),
  (
    'alice',
    'pass1234',
    '555-101-0001',
    '12 Oak St, Los Angeles CA',
    'Seller',
    'Electronics'
  ),
  (
    'bob',
    'pass1234',
    '555-101-0002',
    '34 Pine Ave, San Diego CA',
    'Seller',
    'Collectibles'
  ),
  (
    'carol',
    'pass1234',
    '555-101-0003',
    '56 Maple Dr, San Francisco CA',
    'Seller',
    'Fashion'
  ),
  (
    'dave',
    'pass1234',
    '555-202-0001',
    '78 Elm Blvd, Riverside CA',
    'Buyer',
    'Electronics'
  ),
  (
    'eve',
    'pass1234',
    '555-202-0002',
    '90 Cedar Ln, Irvine CA',
    'Buyer',
    'Collectibles'
  ),
  (
    'frank',
    'pass1234',
    '555-202-0003',
    '11 Birch Rd, Oakland CA',
    'Buyer',
    'Fashion'
  ),
  (
    'grace',
    'pass1234',
    '555-202-0004',
    '22 Walnut St, Fresno CA',
    'Buyer',
    'Electronics'
  ),
  (
    'henry',
    'pass1234',
    '555-202-0005',
    '33 Spruce Ct, Long Beach CA',
    'Buyer',
    NULL
  ),
  (
    'isabella',
    'pass1234',
    '555-202-0006',
    '44 Ash Way, Bakersfield CA',
    'Buyer',
    'Collectibles'
  );

INSERT INTO
  item (
    item_id,
    item_name,
    category,
    starting_price,
    item_condition,
    description,
    seller_login,
    seller_role
  )
VALUES
  (
    1,
    'MacBook Pro 14"',
    'Electronics',
    800.00,
    'Used - Like New',
    '2022 M1 Pro, 16GB RAM, 512GB SSD.',
    'alice',
    'Seller'
  ),
  (
    2,
    'Vintage Rolex Submariner',
    'Collectibles',
    5000.00,
    'Used - Good',
    '1985 ref 16800. Serviced 2023.',
    'bob',
    'Seller'
  ),
  (
    3,
    'Sony WH-1000XM5',
    'Electronics',
    80.00,
    'Used - Good',
    'Noise cancelling headphones, all cables.',
    'alice',
    'Seller'
  ),
  (
    4,
    'Levi 501 Jeans',
    'Fashion',
    25.00,
    'Used - Good',
    'Size 32x32. Classic indigo wash.',
    'carol',
    'Seller'
  ),
  (
    5,
    'Nintendo Switch OLED',
    'Electronics',
    180.00,
    'Used - Like New',
    'Includes dock, Joy-Cons, charger.',
    'alice',
    'Seller'
  ),
  (
    6,
    'Air Jordan 1 Retro High',
    'Fashion',
    120.00,
    'New',
    'Chicago colorway, Size 10, Deadstock.',
    'carol',
    'Seller'
  ),
  (
    7,
    '1st Ed. Harry Potter',
    'Collectibles',
    2000.00,
    'Used - Fair',
    'Bloomsbury 1997. Wear on spine.',
    'bob',
    'Seller'
  ),
  (
    8,
    'iPad Pro 12.9" M2',
    'Electronics',
    500.00,
    'Used - Like New',
    '2022, 256GB WiFi, with Apple Pencil.',
    'alice',
    'Seller'
  ),
  (
    9,
    'Vintage Levi Trucker',
    'Fashion',
    60.00,
    'Used - Good',
    'Size M. 1990s. Faded wash.',
    'carol',
    'Seller'
  ),
  (
    10,
    'Pokemon Charizard Holo',
    'Collectibles',
    300.00,
    'Used - Good',
    'Shadowless base set. Light play.',
    'bob',
    'Seller'
  );

INSERT INTO
  auction (
    auction_id,
    item_id,
    seller_login,
    seller_role,
    current_highest_bid,
    auction_status,
    winner_login,
    winner_role
  )
VALUES
  (
    1,
    1,
    'alice',
    'Seller',
    950.00,
    'Active',
    NULL,
    NULL
  ),
  (
    2,
    2,
    'bob',
    'Seller',
    5800.00,
    'Active',
    NULL,
    NULL
  ),
  (
    3,
    3,
    'alice',
    'Seller',
    115.00,
    'Active',
    NULL,
    NULL
  ),
  (
    4,
    4,
    'carol',
    'Seller',
    30.00,
    'Active',
    NULL,
    NULL
  ),
  (
    5,
    5,
    'alice',
    'Seller',
    210.00,
    'Active',
    NULL,
    NULL
  ),
  (
    6,
    6,
    'carol',
    'Seller',
    175.00,
    'Closed',
    'dave',
    'Buyer'
  ),
  (
    7,
    7,
    'bob',
    'Seller',
    2500.00,
    'Closed',
    'eve',
    'Buyer'
  ),
  (
    8,
    8,
    'alice',
    'Seller',
    620.00,
    'Active',
    NULL,
    NULL
  ),
  (
    9,
    9,
    'carol',
    'Seller',
    85.00,
    'Active',
    NULL,
    NULL
  ),
  (
    10,
    10,
    'bob',
    'Seller',
    420.00,
    'Closed',
    'grace',
    'Buyer'
  );

INSERT INTO
  bid (
    bid_id,
    auction_id,
    buyer_login,
    buyer_role,
    bid_amount,
    bid_timestamp
  )
VALUES
  (
    1,
    1,
    'dave',
    'Buyer',
    850.00,
    '2026-05-20 10:00:00'
  ),
  (
    2,
    1,
    'henry',
    'Buyer',
    900.00,
    '2026-05-21 11:00:00'
  ),
  (
    3,
    1,
    'dave',
    'Buyer',
    950.00,
    '2026-05-22 09:30:00'
  ),
  (
    4,
    2,
    'eve',
    'Buyer',
    5100.00,
    '2026-05-19 14:00:00'
  ),
  (
    5,
    2,
    'frank',
    'Buyer',
    5400.00,
    '2026-05-20 16:00:00'
  ),
  (
    6,
    2,
    'eve',
    'Buyer',
    5800.00,
    '2026-05-22 10:00:00'
  ),
  (
    7,
    3,
    'grace',
    'Buyer',
    90.00,
    '2026-05-21 08:00:00'
  ),
  (
    8,
    3,
    'henry',
    'Buyer',
    110.00,
    '2026-05-22 12:00:00'
  ),
  (
    9,
    3,
    'grace',
    'Buyer',
    115.00,
    '2026-05-23 09:00:00'
  ),
  (
    10,
    4,
    'isabella',
    'Buyer',
    28.00,
    '2026-05-22 15:00:00'
  ),
  (
    11,
    4,
    'frank',
    'Buyer',
    30.00,
    '2026-05-23 11:00:00'
  ),
  (
    12,
    5,
    'dave',
    'Buyer',
    190.00,
    '2026-05-20 13:00:00'
  ),
  (
    13,
    5,
    'henry',
    'Buyer',
    200.00,
    '2026-05-21 14:00:00'
  ),
  (
    14,
    5,
    'dave',
    'Buyer',
    210.00,
    '2026-05-23 10:00:00'
  ),
  (
    15,
    6,
    'frank',
    'Buyer',
    130.00,
    '2026-05-10 09:00:00'
  ),
  (
    16,
    6,
    'dave',
    'Buyer',
    155.00,
    '2026-05-11 10:00:00'
  ),
  (
    17,
    6,
    'frank',
    'Buyer',
    165.00,
    '2026-05-12 11:00:00'
  ),
  (
    18,
    6,
    'dave',
    'Buyer',
    175.00,
    '2026-05-13 12:00:00'
  ),
  (
    19,
    7,
    'isabella',
    'Buyer',
    2100.00,
    '2026-05-05 10:00:00'
  ),
  (
    20,
    7,
    'eve',
    'Buyer',
    2300.00,
    '2026-05-06 11:00:00'
  ),
  (
    21,
    7,
    'isabella',
    'Buyer',
    2400.00,
    '2026-05-07 12:00:00'
  ),
  (
    22,
    7,
    'eve',
    'Buyer',
    2500.00,
    '2026-05-08 13:00:00'
  ),
  (
    23,
    8,
    'frank',
    'Buyer',
    520.00,
    '2026-05-22 10:00:00'
  ),
  (
    24,
    8,
    'grace',
    'Buyer',
    580.00,
    '2026-05-23 09:00:00'
  ),
  (
    25,
    8,
    'frank',
    'Buyer',
    620.00,
    '2026-05-24 08:00:00'
  ),
  (
    26,
    9,
    'henry',
    'Buyer',
    65.00,
    '2026-05-23 14:00:00'
  ),
  (
    27,
    9,
    'dave',
    'Buyer',
    75.00,
    '2026-05-24 10:00:00'
  ),
  (
    28,
    9,
    'henry',
    'Buyer',
    85.00,
    '2026-05-25 09:00:00'
  ),
  (
    29,
    10,
    'eve',
    'Buyer',
    320.00,
    '2026-05-12 10:00:00'
  ),
  (
    30,
    10,
    'grace',
    'Buyer',
    370.00,
    '2026-05-13 11:00:00'
  ),
  (
    31,
    10,
    'eve',
    'Buyer',
    400.00,
    '2026-05-14 12:00:00'
  ),
  (
    32,
    10,
    'grace',
    'Buyer',
    420.00,
    '2026-05-15 13:00:00'
  );

INSERT INTO
  payment (
    payment_id,
    auction_id,
    buyer_login,
    buyer_role,
    amount,
    payment_status
  )
VALUES
  (1, 6, 'dave', 'Buyer', 175.00, 'Completed'),
  (2, 7, 'eve', 'Buyer', 2500.00, 'Completed'),
  (3, 10, 'grace', 'Buyer', 420.00, 'Pending');

INSERT INTO
  shipment (
    shipment_id,
    auction_id,
    address,
    shipment_status,
    tracking_number
  )
VALUES
  (
    1,
    6,
    '78 Elm Blvd, Riverside CA',
    'Delivered',
    'UPS-2026-00441'
  ),
  (
    2,
    7,
    '90 Cedar Ln, Irvine CA',
    'Shipped',
    'FEDEX-2026-00882'
  );