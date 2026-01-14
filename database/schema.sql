CREATE DATABASE IF NOT EXISTS product_scanner;
USE product_scanner;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(100),
    brand VARCHAR(100),
    manufacturing_date DATE,
    expiry_date DATE,
    price DECIMAL(10,2),
    description TEXT
);
