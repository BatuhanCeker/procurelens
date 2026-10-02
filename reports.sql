-- report: 1. WHERE ve ORDER BY: taslak siparisler
SELECT id, order_date
FROM purchase_orders
WHERE approved = 0
ORDER BY order_date, id;

-- report: 2. JOIN: siparis kalemleri ve TRY tutarlari
SELECT o.id AS siparis, s.name AS tedarikci, p.name AS urun,
       l.quantity AS adet, l.unit_price_kurus / 100.0 AS birim_fiyat_TL,
       l.quantity * l.unit_price_kurus / 100.0 AS tutar_TL
FROM purchase_orders o
JOIN suppliers s ON s.id = o.supplier_id
JOIN order_lines l ON l.order_id = o.id
JOIN products p ON p.id = l.product_id
ORDER BY o.id, l.id;

-- report: 3. GROUP BY ve SUM: tedarikci bazinda onayli siparis tutari
SELECT s.name AS tedarikci,
       SUM(l.quantity * l.unit_price_kurus) / 100.0 AS toplam_TL
FROM suppliers s
JOIN purchase_orders o ON o.supplier_id = s.id
JOIN order_lines l ON l.order_id = o.id
WHERE o.approved = 1
GROUP BY s.id, s.name;

-- report: 4. LEFT JOIN ve IS NULL: hic siparis verilmeyen tedarikciler
SELECT s.name AS tedarikci
FROM suppliers s
LEFT JOIN purchase_orders o ON o.supplier_id = s.id
WHERE o.id IS NULL;

-- report: 5. HAVING: onayli siparislerin acik kalan kalemleri
SELECT o.id AS siparis, p.name AS urun, l.quantity AS siparis_adedi,
       COALESCE(SUM(r.quantity), 0) AS teslim_alinan,
       l.quantity - COALESCE(SUM(r.quantity), 0) AS kalan
FROM purchase_orders o
JOIN order_lines l ON l.order_id = o.id
JOIN products p ON p.id = l.product_id
LEFT JOIN receipt_lines r ON r.order_line_id = l.id
WHERE o.approved = 1
GROUP BY o.id, l.id, p.name, l.quantity
HAVING l.quantity > COALESCE(SUM(r.quantity), 0);

-- report: 6. Stok: yalnizca teslim alinan urunler sayilir; siparis stok degildir
SELECT p.sku, p.name AS urun, COALESCE(SUM(r.quantity), 0) AS stok
FROM products p
LEFT JOIN order_lines l ON l.product_id = p.id
LEFT JOIN receipt_lines r ON r.order_line_id = l.id
GROUP BY p.id, p.sku, p.name
ORDER BY p.id;

-- report: 7. CASE ve alt sorgu: siparis durumu (ayri bir durum alani tutmuyoruz)
SELECT o.id AS siparis,
    CASE
        WHEN o.approved = 0 THEN 'TASLAK'
        WHEN NOT EXISTS (
            SELECT 1 FROM receipts r JOIN receipt_lines rl ON rl.receipt_id = r.id
            WHERE r.order_id = o.id
        ) THEN 'ONAYLI'
        WHEN EXISTS (
            SELECT 1 FROM order_lines l
            WHERE l.order_id = o.id AND l.quantity > COALESCE(
                (SELECT SUM(rl.quantity) FROM receipt_lines rl WHERE rl.order_line_id = l.id), 0)
        ) THEN 'KISMI_TESLIM'
        ELSE 'TAMAMLANDI'
    END AS durum
FROM purchase_orders o
ORDER BY o.id;
