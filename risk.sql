-- Teslimat takibi: :as_of_date rapor tarihidir (YYYY-MM-DD).
-- Once teslimatlari siparis kalemi bazinda toplariz. Boylece birden fazla
-- teslimat, siparis tutarini JOIN sirasinda cogaltmaz.
-- Bu bir guncel durum raporudur. Gecmis onay durumlari kaydedilmedigi icin
-- gecmise yonelik onay denetimi iddiasi tasimaz.
WITH received AS (
    SELECT rl.order_line_id, SUM(rl.quantity) AS quantity
    FROM receipt_lines rl
    JOIN receipts r ON r.id = rl.receipt_id
    WHERE r.received_on <= :as_of_date
    GROUP BY rl.order_line_id
), outstanding AS (
    SELECT o.id AS order_id, s.name AS supplier, p.name AS product,
           o.promised_date, l.quantity - COALESCE(r.quantity, 0) AS remaining,
           l.unit_price_kurus,
           CAST(julianday(:as_of_date) - julianday(o.promised_date) AS INTEGER) AS days_past_due
    FROM purchase_orders o
    JOIN suppliers s ON s.id = o.supplier_id
    JOIN order_lines l ON l.order_id = o.id
    JOIN products p ON p.id = l.product_id
    LEFT JOIN received r ON r.order_line_id = l.id
    WHERE o.approved = 1 AND o.order_date <= :as_of_date
)
SELECT order_id, supplier, product, promised_date, remaining,
       remaining * unit_price_kurus AS open_value_kurus,
       MAX(days_past_due, 0) AS overdue_days,
       CASE WHEN days_past_due > 0 THEN 'Gecikmiş'
            WHEN days_past_due = 0 THEN 'Bugün bekleniyor'
            ELSE 'Planlı' END AS status
FROM outstanding
WHERE remaining > 0
ORDER BY overdue_days DESC, open_value_kurus DESC, order_id, product;
