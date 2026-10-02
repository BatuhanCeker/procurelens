-- 1. 10 klavye ve 5 fare iceren 1 numarali siparisi onayla.
UPDATE purchase_orders SET approved = 1 WHERE id = 1;

-- 2. Ilk teslimat: 6 klavye, 5 fare. Klavyenin 4 adedi henuz gelmedi.
-- BEGIN/COMMIT: belge ve kalemleri birlikte kaydet (transaction).
BEGIN;
INSERT INTO receipts (id, order_id, reference, received_on)
VALUES (1, 1, 'TESLIM-001', '2026-10-02');
INSERT INTO receipt_lines (receipt_id, order_line_id, quantity)
VALUES (1, 1, 6), (1, 2, 5);
COMMIT;
