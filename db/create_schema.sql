-- Café Menu and Order Management System
-- Database Schema
-- Normalized to BCNF

-- 1. Users Table
-- BCNF Justification: 
-- Functional Dependencies: user_id -> {username, password, role}
-- All determinants are candidate keys.
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL, -- Plain text for this assignment as requested
    role ENUM('MANAGER', 'CASHIER') NOT NULL
);

-- 2. MenuCategories Table
-- BCNF Justification:
-- Functional Dependencies: category_id -> {name, display_order}
-- All determinants are candidate keys.
CREATE TABLE IF NOT EXISTS MenuCategories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    display_order INT NOT NULL
);

-- 3. MenuItems Table
-- BCNF Justification:
-- Functional Dependencies: item_id -> {category_id, name, price, is_active}
-- All determinants are candidate keys. category_id is a FK.
CREATE TABLE IF NOT EXISTS MenuItems (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES MenuCategories(category_id)
);

-- 4. Orders Table
-- BCNF Justification:
-- Functional Dependencies: order_id -> {user_id, table_number, order_status, notes, created_at, closed_at}
-- All determinants are candidate keys. user_id is a FK.
CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    table_number VARCHAR(10) NOT NULL,
    order_status ENUM('PENDING', 'IN_PREP', 'READY', 'SERVED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    notes VARCHAR(255) NOT NULL DEFAULT '',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- 5. OrderItems Table
-- BCNF Justification:
-- Functional Dependencies: order_item_id -> {order_id, item_id, quantity, note, line_total}
-- All determinants are candidate keys. order_id and item_id are FKs.
-- Note: line_total is derived but stored for historical accuracy (if prices change).
CREATE TABLE IF NOT EXISTS OrderItems (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    note VARCHAR(255) NOT NULL DEFAULT '',
    line_total DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES MenuItems(item_id)
);
