-- Tamami hayali egitim verisidir.
INSERT INTO suppliers (id, name) VALUES
    (1, 'Ornek Ofis Tedarik'), (2, 'Demo Teknoloji'), (3, 'Yeni Tedarikci');
INSERT INTO products (id, sku, name) VALUES
    (1, 'KL-001', 'Klavye'), (2, 'FR-001', 'Fare'), (3, 'MN-001', 'Monitor');

INSERT INTO purchase_orders (id, supplier_id, order_date, promised_date) VALUES
    (1, 1, '2026-10-01', '2026-10-02'), (2, 2, '2026-10-02', '2026-10-08');
INSERT INTO order_lines (id, order_id, product_id, quantity, unit_price_kurus) VALUES
    (1, 1, 1, 10, 50000), (2, 1, 2, 5, 20000), (3, 2, 3, 2, 400000);
