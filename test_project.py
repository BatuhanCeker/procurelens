import sqlite3
import unittest

from run import initialize, report_queries


class ProcurementTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        initialize(self.db)
        self.reports = [sql for _, sql in report_queries()]

    def tearDown(self):
        self.db.close()

    def test_initial_stock_open_orders_and_totals(self):
        stock = self.db.execute(self.reports[5]).fetchall()
        self.assertEqual([row[2] for row in stock], [6, 5, 0])
        self.assertEqual(self.db.execute(self.reports[4]).fetchall(), [(1, 'Klavye', 10, 6, 4)])
        self.assertEqual(self.db.execute(self.reports[2]).fetchall(), [('Ornek Ofis Tedarik', 6000.0)])
        self.assertEqual(self.db.execute(self.reports[3]).fetchall(), [('Yeni Tedarikci',)])

    def test_partial_then_complete(self):
        self.assertEqual(self.db.execute(self.reports[6]).fetchall(), [(1, 'KISMI_TESLIM'), (2, 'TASLAK')])
        with self.db:
            self.db.execute("INSERT INTO receipts VALUES (2, 1, 'TESLIM-002', '2026-10-03')")
            self.db.execute('INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (2, 1, 4)')
        self.assertEqual(self.db.execute(self.reports[6]).fetchone(), (1, 'TAMAMLANDI'))
        self.assertEqual(self.db.execute(self.reports[4]).fetchall(), [])
        self.assertEqual(self.db.execute(self.reports[5]).fetchone()[2], 10)

    def test_overdelivery_rolls_back_receipt(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'fazla'):
            with self.db:
                self.db.execute("INSERT INTO receipts VALUES (2, 1, 'BAD', '2026-10-03')")
                self.db.execute('INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (2, 1, 5)')
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0], 1)
        self.assertEqual(self.db.execute(self.reports[5]).fetchone()[2], 6)

    def test_draft_receipt_rejected(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'Taslak'):
            self.db.execute("INSERT INTO receipts VALUES (2, 2, 'BAD', '2026-10-03')")

    def test_duplicate_reference_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO receipts VALUES (2, 1, 'TESLIM-001', '2026-10-03')")

    def test_mismatched_order_line_rejected(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'uyusmuyor'):
            self.db.execute('INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (1, 3, 1)')

    def test_invalid_quantities_rejected(self):
        for value in (0, -1, 1.5):
            with self.subTest(value=value), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('INSERT INTO order_lines (order_id, product_id, quantity, unit_price_kurus) VALUES (2, 1, ?, 100)', (value,))

    def test_missing_product_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO order_lines (order_id, product_id, quantity, unit_price_kurus) VALUES (2, 999, 1, 100)')

    def test_empty_order_cannot_be_approved(self):
        self.db.execute("INSERT INTO purchase_orders (id, supplier_id, order_date, approved) VALUES (3, 1, '2026-10-03', 0)")
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'Bos'):
            self.db.execute('UPDATE purchase_orders SET approved = 1 WHERE id = 3')

    def test_approved_without_delivery(self):
        self.db.execute('UPDATE purchase_orders SET approved = 1 WHERE id = 2')
        self.assertEqual(self.db.execute(self.reports[6]).fetchall()[1], (2, 'ONAYLI'))

    def test_approved_order_and_history_immutable(self):
        statements = [
            'UPDATE order_lines SET quantity = 20 WHERE id = 1',
            'DELETE FROM order_lines WHERE id = 1',
            'UPDATE purchase_orders SET approved = 0 WHERE id = 1',
            'INSERT INTO order_lines (order_id, product_id, quantity, unit_price_kurus) VALUES (1, 3, 1, 100)',
            'UPDATE receipt_lines SET quantity = 10 WHERE id = 1',
            'DELETE FROM receipt_lines WHERE id = 1',
            'UPDATE receipts SET order_id = 2 WHERE id = 1',
            'DELETE FROM receipts WHERE id = 1',
            "INSERT INTO purchase_orders (id, supplier_id, order_date, approved) VALUES (3, 1, '2026-10-03', 1)",
        ]
        for sql in statements:
            with self.subTest(sql=sql), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute(sql)


if __name__ == '__main__':
    unittest.main(verbosity=2)
