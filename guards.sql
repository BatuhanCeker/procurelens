-- İLERİ SEVİYE / İSTEĞE BAĞLI OKUMA
-- Trigger: veri değişmeden önce çalışan veritabanı kontrolü.
-- Mülakat hazırlığında önce reports.sql içindeki temel sorguları öğren.

CREATE TRIGGER approve_nonempty_order
BEFORE UPDATE OF approved ON purchase_orders
WHEN NEW.approved = 1 AND NOT EXISTS (
    SELECT 1 FROM order_lines WHERE order_id = OLD.id
)
BEGIN
    SELECT RAISE(ABORT, 'Bos siparis onaylanamaz');
END;

CREATE TRIGGER create_draft_order
BEFORE INSERT ON purchase_orders WHEN NEW.approved <> 0
BEGIN
    SELECT RAISE(ABORT, 'Siparis taslak olusturulmali');
END;

CREATE TRIGGER freeze_approved_order
BEFORE UPDATE ON purchase_orders WHEN OLD.approved = 1
BEGIN
    SELECT RAISE(ABORT, 'Onayli siparis degistirilemez');
END;

CREATE TRIGGER insert_draft_line
BEFORE INSERT ON order_lines
WHEN (SELECT approved FROM purchase_orders WHERE id = NEW.order_id) = 1
BEGIN
    SELECT RAISE(ABORT, 'Onayli siparise kalem eklenemez');
END;

CREATE TRIGGER update_draft_line
BEFORE UPDATE ON order_lines
WHEN (SELECT approved FROM purchase_orders WHERE id = OLD.order_id) = 1
  OR (SELECT approved FROM purchase_orders WHERE id = NEW.order_id) = 1
BEGIN
    SELECT RAISE(ABORT, 'Onayli siparis kalemi degistirilemez');
END;

CREATE TRIGGER delete_draft_line
BEFORE DELETE ON order_lines
WHEN (SELECT approved FROM purchase_orders WHERE id = OLD.order_id) = 1
BEGIN
    SELECT RAISE(ABORT, 'Onayli siparis kalemi silinemez');
END;

CREATE TRIGGER receive_approved_order
BEFORE INSERT ON receipts
WHEN (SELECT approved FROM purchase_orders WHERE id = NEW.order_id) <> 1
BEGIN
    SELECT RAISE(ABORT, 'Taslak siparise mal kabul yapilamaz');
END;

CREATE TRIGGER validate_receipt_line
BEFORE INSERT ON receipt_lines
BEGIN
    SELECT CASE WHEN
        (SELECT order_id FROM receipts WHERE id = NEW.receipt_id) <>
        (SELECT order_id FROM order_lines WHERE id = NEW.order_line_id)
    THEN RAISE(ABORT, 'Teslimat ile siparis kalemi uyusmuyor') END;

    SELECT CASE WHEN NEW.quantity + COALESCE(
        (SELECT SUM(quantity) FROM receipt_lines
         WHERE order_line_id = NEW.order_line_id), 0
    ) > (SELECT quantity FROM order_lines WHERE id = NEW.order_line_id)
    THEN RAISE(ABORT, 'Siparisten fazla mal kabul edilemez') END;
END;

-- Bu ilk surum iade/duzeltme akislarini desteklemez; kayit gecmisi korunur.
CREATE TRIGGER no_receipt_update BEFORE UPDATE ON receipts
BEGIN SELECT RAISE(ABORT, 'Teslimat gecmisi degistirilemez'); END;
CREATE TRIGGER no_receipt_delete BEFORE DELETE ON receipts
BEGIN SELECT RAISE(ABORT, 'Teslimat gecmisi silinemez'); END;
CREATE TRIGGER no_receipt_line_update BEFORE UPDATE ON receipt_lines
BEGIN SELECT RAISE(ABORT, 'Stok hareketi degistirilemez'); END;
CREATE TRIGGER no_receipt_line_delete BEFORE DELETE ON receipt_lines
BEGIN SELECT RAISE(ABORT, 'Stok hareketi silinemez'); END;
