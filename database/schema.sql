-- MediTrack Enterprise Pharmacy Management System
-- Comprehensive Database Schema

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS medical_store;
USE medical_store;

-- Drop tables in reverse order of dependencies
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- 2. Users & RBAC
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role ENUM('admin', 'cashier', 'staff') DEFAULT 'staff',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Medicine Inventory
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    company VARCHAR(100),
    batch_no VARCHAR(50),
    expiry_date DATE,
    stock_qty INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    reorder_level INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. Customers
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    loyalty_points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Sales Transactions
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT,
    user_id INT NOT NULL, -- The cashier
    total_amount DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    grand_total DECIMAL(10, 2) NOT NULL,
    payment_mode ENUM('cash', 'card', 'upi', 'credit') DEFAULT 'cash',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 6. Sale Details (Items)
CREATE TABLE IF NOT EXISTS sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    inventory_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id)
);

-- 7. Audit & Activity Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50), -- LOGIN, LOGOUT, ADD_MEDICINE, DELETE_USER, etc.
    module_name VARCHAR(50), -- INVENTORY, BILLING, USERS
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 8. Seed Initial Data
-- Note: Admin password will be 'admin123' (hashed in setup script)
INSERT INTO users (username, password_hash, full_name, role) 
VALUES ('admin', '$2b$12$MxsU63W36GxH5b7MZjtJNuhI3z6/GYcBSb4RCH/xtcngaOYzM/.8q', 'System Administrator', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- Default Cashier account (password: cashier123)
INSERT INTO users (username, password_hash, full_name, role)
VALUES ('cashier', '$2b$12$EaJksEGvulcut3lamw6ueOQXtKlXS41aoCOFDF1.UjH31okRzNvDy', 'Main Cashier', 'cashier')
ON DUPLICATE KEY UPDATE username=username;

-- Seed Sample Inventory
INSERT INTO inventory (medicine_name, category, company, batch_no, expiry_date, stock_qty, price)
VALUES 
('Paracetamol 500mg', 'Painkiller', 'GSK', 'B101', '2026-12-01', 100, 10.50),
('Amoxicillin 250mg', 'Antibiotic', 'Pfizer', 'A202', '2025-06-15', 50, 45.00),
('Vitamin C 500mg', 'Supplement', 'Abbott', 'V303', '2027-01-10', 200, 15.00),
('Ibuprofen 400mg', 'Painkiller', 'Bayer', 'I404', '2026-08-20', 80, 25.00);
