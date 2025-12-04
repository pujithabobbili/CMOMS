-- Initialize Data
-- At least 15 rows per table

-- 1. Users (15 rows)
INSERT INTO Users (username, password, role) VALUES 
('admin', 'admin123', 'MANAGER'),
('manager_jane', 'jane123', 'MANAGER'),
('cashier_bob', 'bob123', 'CASHIER'),
('cashier_alice', 'alice123', 'CASHIER'),
('cashier_tom', 'tom123', 'CASHIER'),
('cashier_sara', 'sara123', 'CASHIER'),
('manager_mike', 'mike123', 'MANAGER'),
('cashier_dave', 'dave123', 'CASHIER'),
('cashier_emma', 'emma123', 'CASHIER'),
('cashier_lucy', 'lucy123', 'CASHIER'),
('cashier_john', 'john123', 'CASHIER'),
('cashier_kate', 'kate123', 'CASHIER'),
('cashier_alex', 'alex123', 'CASHIER'),
('cashier_zoe', 'zoe123', 'CASHIER'),
('cashier_ben', 'ben123', 'CASHIER');

-- 2. MenuCategories (15 rows)
INSERT INTO MenuCategories (name, display_order) VALUES 
('Hot Coffee', 1),
('Cold Coffee', 2),
('Tea', 3),
('Bakery', 4),
('Sandwiches', 5),
('Salads', 6),
('Desserts', 7),
('Cold Drinks', 8),
('Smoothies', 9),
('Breakfast', 10),
('Lunch Specials', 11),
('Snacks', 12),
('Seasonal', 13),
('Merchandise', 14),
('Whole Beans', 15);

-- 3. MenuItems (20 rows)
INSERT INTO MenuItems (category_id, name, price, is_active) VALUES 
(1, 'Espresso', 2.50, 1),
(1, 'Americano', 3.00, 1),
(1, 'Cappuccino', 4.00, 1),
(1, 'Latte', 4.50, 1),
(2, 'Iced Coffee', 3.50, 1),
(2, 'Cold Brew', 4.00, 1),
(2, 'Iced Latte', 4.75, 1),
(3, 'Earl Grey', 3.00, 1),
(3, 'Green Tea', 3.00, 1),
(4, 'Croissant', 3.00, 1),
(4, 'Blueberry Muffin', 3.50, 1),
(4, 'Bagel with Cream Cheese', 3.50, 1),
(5, 'Ham & Cheese Sandwich', 6.50, 1),
(5, 'Turkey Club', 7.50, 1),
(6, 'Caesar Salad', 8.00, 1),
(7, 'Cheesecake', 5.00, 1),
(7, 'Brownie', 3.00, 1),
(8, 'Lemonade', 3.50, 1),
(9, 'Berry Smoothie', 6.00, 1),
(10, 'Breakfast Burrito', 7.00, 1);

-- 4. Orders (15 rows)
INSERT INTO Orders (user_id, table_number, order_status, notes, created_at, closed_at) VALUES 
(3, 'T1', 'SERVED', '', NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 1 DAY + INTERVAL 30 MINUTE),
(4, 'T2', 'SERVED', 'No receipt', NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 1 DAY + INTERVAL 20 MINUTE),
(3, 'T3', 'SERVED', '', NOW() - INTERVAL 5 HOUR, NOW() - INTERVAL 4 HOUR),
(5, 'Takeout', 'SERVED', '', NOW() - INTERVAL 4 HOUR, NOW() - INTERVAL 3 HOUR),
(3, 'T1', 'PENDING', '', NOW(), NULL),
(4, 'T4', 'IN_PREP', '', NOW(), NULL),
(6, 'T5', 'READY', 'Extra napkins', NOW(), NULL),
(3, 'T2', 'SERVED', '', NOW() - INTERVAL 2 HOUR, NOW() - INTERVAL 1 HOUR),
(5, 'T3', 'CANCELLED', 'Customer changed mind', NOW() - INTERVAL 3 HOUR, NOW() - INTERVAL 3 HOUR),
(4, 'Takeout', 'SERVED', '', NOW() - INTERVAL 6 HOUR, NOW() - INTERVAL 5 HOUR),
(3, 'T6', 'PENDING', '', NOW(), NULL),
(6, 'T7', 'IN_PREP', 'Allergy: Nuts', NOW(), NULL),
(5, 'T8', 'SERVED', '', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 2 DAY + INTERVAL 45 MINUTE),
(4, 'T9', 'SERVED', '', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 2 DAY + INTERVAL 30 MINUTE),
(3, 'T1', 'READY', '', NOW(), NULL);

-- 5. OrderItems (at least 15 rows)
INSERT INTO OrderItems (order_id, item_id, quantity, note, line_total) VALUES 
(1, 1, 2, '', 5.00), -- 2 Espresso
(1, 10, 2, '', 6.00), -- 2 Croissants
(2, 4, 1, 'Soy milk', 4.50), -- 1 Latte
(3, 13, 1, '', 6.50), -- 1 Ham & Cheese
(3, 2, 1, '', 3.00), -- 1 Americano
(4, 19, 2, '', 12.00), -- 2 Smoothies
(5, 3, 1, '', 4.00), -- 1 Cappuccino
(5, 17, 1, '', 3.00), -- 1 Brownie
(6, 12, 1, 'Toasted', 3.50), -- 1 Bagel
(7, 5, 2, '', 7.00), -- 2 Iced Coffee
(8, 20, 1, 'No salsa', 7.00), -- 1 Burrito
(9, 1, 1, '', 2.50), -- 1 Espresso (Cancelled order item)
(10, 15, 1, 'Dressing on side', 8.00), -- 1 Salad
(11, 7, 1, '', 4.75), -- 1 Iced Latte
(11, 11, 1, '', 3.50), -- 1 Muffin
(12, 16, 1, '', 5.00), -- 1 Cheesecake
(13, 14, 2, '', 15.00), -- 2 Turkey Club
(14, 6, 2, '', 8.00), -- 2 Cold Brew
(15, 3, 1, 'Extra foam', 4.00); -- 1 Cappuccino
