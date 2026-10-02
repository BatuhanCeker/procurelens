PRAGMA foreign_keys = ON;

CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);

CREATE TABLE purchase_orders (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    order_date TEXT NOT NULL,
    approved INTEGER NOT NULL DEFAULT 0 CHECK (approved IN (0, 1)),
    promised_date TEXT NOT NULL DEFAULT '2026-10-05'
        CHECK (date(promised_date, '+0 days') IS NOT NULL
           AND date(promised_date, '+0 days') = promised_date
           AND promised_date >= order_date)
);

CREATE TABLE order_lines (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES purchase_orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (typeof(quantity) = 'integer' AND quantity > 0),
    unit_price_kurus INTEGER NOT NULL
        CHECK (typeof(unit_price_kurus) = 'integer' AND unit_price_kurus > 0),
    UNIQUE (order_id, product_id)
);

-- Her teslimat belgesinin başlığı bir kez oluşturulur.
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES purchase_orders(id),
    reference TEXT NOT NULL CHECK (length(trim(reference)) > 0),
    received_on TEXT NOT NULL,
    UNIQUE (order_id, reference)
);

-- Mal kabul satırları bu eğitim projesinde stok giriş hareketidir.
-- Aynı miktarı ayrı bir stok tablosunda tutmayarak tutarsızlığı önlüyoruz.
CREATE TABLE receipt_lines (
    id INTEGER PRIMARY KEY,
    receipt_id INTEGER NOT NULL REFERENCES receipts(id),
    order_line_id INTEGER NOT NULL REFERENCES order_lines(id),
    quantity INTEGER NOT NULL CHECK (typeof(quantity) = 'integer' AND quantity > 0),
    UNIQUE (receipt_id, order_line_id)
);
