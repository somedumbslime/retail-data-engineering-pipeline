INSERT INTO users (id, name, email, city, created_at, updated_at)
VALUES
    (1, 'Alice Kovalenko', 'alice@example.com', 'Kyiv', '2026-03-01 10:00:00', '2026-03-10 08:30:00'),
    (2, 'Bohdan Petrenko', 'bohdan@example.com', 'Lviv', '2026-03-02 11:15:00', '2026-03-10 08:30:00'),
    (3, 'Olena Melnyk', 'olena@example.com', 'Odesa', '2026-03-03 09:40:00', '2026-03-10 08:30:00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO products (id, name, category, price, created_at, updated_at)
VALUES
    (101, 'Espresso Beans', 'Grocery', 12.50, '2026-03-01 08:00:00', '2026-03-10 08:30:00'),
    (102, 'Coffee Machine', 'Electronics', 199.00, '2026-03-01 08:00:00', '2026-03-10 08:30:00'),
    (103, 'Travel Mug', 'Home', 15.90, '2026-03-01 08:00:00', '2026-03-10 08:30:00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO orders (id, user_id, order_date, status, created_at, updated_at)
VALUES
    (5001, 1, '2026-03-10', 'paid', '2026-03-10 09:10:00', '2026-03-10 09:10:00'),
    (5002, 2, '2026-03-10', 'paid', '2026-03-10 09:20:00', '2026-03-10 09:20:00'),
    (5003, 3, '2026-03-11', 'paid', '2026-03-11 10:05:00', '2026-03-11 10:05:00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO order_items (id, order_id, product_id, quantity, price_at_purchase, updated_at)
VALUES
    (9001, 5001, 101, 2, 12.50, '2026-03-10 09:10:00'),
    (9002, 5001, 103, 1, 15.90, '2026-03-10 09:10:00'),
    (9003, 5002, 102, 1, 199.00, '2026-03-10 09:20:00'),
    (9004, 5003, 101, 3, 12.50, '2026-03-11 10:05:00')
ON CONFLICT (id) DO NOTHING;
