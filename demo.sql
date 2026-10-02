-- Sunum icin genisletilmis senaryo; temel egitim verisi degismez.
-- Bir tamamlanmis siparis, bir bugun beklenen ve bir planli siparis.
INSERT INTO purchase_orders (id, supplier_id, order_date, promised_date) VALUES
    (3, 2, '2026-10-02', '2026-10-05'),
    (4, 1, '2026-10-02', '2026-10-08'),
    (5, 2, '2026-10-01', '2026-10-03');
INSERT INTO order_lines (id, order_id, product_id, quantity, unit_price_kurus) VALUES
    (4, 3, 3, 3, 400000), (5, 4, 2, 20, 20000), (6, 5, 1, 4, 50000);
UPDATE purchase_orders SET approved = 1 WHERE id IN (3, 4, 5);
BEGIN;
INSERT INTO receipts (id, order_id, reference, received_on)
VALUES (5, 5, 'TAMAM-001', '2026-10-03');
INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (5, 6, 4);
COMMIT;
