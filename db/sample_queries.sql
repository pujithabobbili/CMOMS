-- Sample Queries for Report Appendices

-- 1. List all active menu items and their category names ordered by category/display order.
-- Joins MenuItems with MenuCategories to get category names.
-- Filters by is_active = 1.
SELECT 
    c.name AS Category,
    m.name AS Item,
    m.price AS Price
FROM MenuItems m
JOIN MenuCategories c ON m.category_id = c.category_id
WHERE m.is_active = 1
ORDER BY c.display_order, m.name;

-- 2. Daily sales total for a given date (using CURDATE() as example).
-- Aggregates line_total from OrderItems for orders created on the specific date.
-- Uses DATE() function to ignore time part of created_at.
SELECT 
    DATE(o.created_at) AS SaleDate,
    SUM(oi.line_total) AS TotalSales
FROM Orders o
JOIN OrderItems oi ON o.order_id = oi.order_id
WHERE DATE(o.created_at) = CURDATE()
AND o.order_status != 'CANCELLED'
GROUP BY DATE(o.created_at);

-- 3. Top 5 best-selling items by total quantity sold.
-- Aggregates quantity by item_id and joins with MenuItems for names.
-- Orders by total quantity descending and limits to 5.
SELECT 
    m.name AS ItemName,
    SUM(oi.quantity) AS TotalSold
FROM OrderItems oi
JOIN MenuItems m ON oi.item_id = m.item_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.order_status != 'CANCELLED'
GROUP BY m.item_id, m.name
ORDER BY TotalSold DESC
LIMIT 5;

-- 4. All orders for a given status with total amount and cashier name.
-- Joins Orders, Users, and OrderItems.
-- Groups by order to sum line totals.
SELECT 
    o.order_id,
    o.table_number,
    o.order_status,
    u.username AS Cashier,
    SUM(oi.line_total) AS OrderTotal
FROM Orders o
JOIN Users u ON o.user_id = u.user_id
LEFT JOIN OrderItems oi ON o.order_id = oi.order_id
WHERE o.order_status = 'SERVED' -- Example status
GROUP BY o.order_id, o.table_number, o.order_status, u.username;

