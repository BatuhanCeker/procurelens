import sqlite3
import unittest

from dashboard import build_report, get_risks
from run import ROOT, initialize


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        initialize(self.db)
        self.db.executescript((ROOT / 'demo.sql').read_text(encoding='utf-8'))

    def tearDown(self):
        self.db.close()

    def test_snapshot_values_and_priority(self):
        rows = get_risks(self.db, '2026-10-05')
        self.assertEqual([r['order_id'] for r in rows], [1, 3, 4])
        self.assertEqual(sum(r['open_value_kurus'] for r in rows), 1800000)
        self.assertEqual(rows[0]['open_value_kurus'], 200000)
        self.assertEqual(rows[0]['overdue_days'], 3)

    def test_due_today_is_not_overdue(self):
        rows = get_risks(self.db, '2026-10-05')
        self.assertEqual(rows[1]['status'], 'Bugün bekleniyor')
        self.assertEqual(rows[1]['overdue_days'], 0)
        self.assertEqual(rows[2]['status'], 'Planlı')

    def test_draft_and_completed_excluded(self):
        self.assertEqual({r['order_id'] for r in get_risks(self.db, '2026-10-05')}, {1, 3, 4})

    def test_multiple_deliveries_do_not_multiply_order_value(self):
        with self.db:
            self.db.execute("INSERT INTO receipts VALUES (6, 1, 'PART-2', '2026-10-04')")
            self.db.execute('INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (6, 1, 2)')
        row = get_risks(self.db, '2026-10-05')[0]
        self.assertEqual((row['remaining'], row['open_value_kurus']), (2, 100000))

    def test_future_receipt_does_not_reduce_snapshot_balance(self):
        with self.db:
            self.db.execute("INSERT INTO receipts VALUES (6, 1, 'FUTURE', '2026-10-07')")
            self.db.execute('INSERT INTO receipt_lines (receipt_id, order_line_id, quantity) VALUES (6, 1, 4)')
        self.assertEqual(get_risks(self.db, '2026-10-05')[0]['remaining'], 4)
        self.assertNotIn(1, {r['order_id'] for r in get_risks(self.db, '2026-10-07')})

    def test_invalid_promised_dates_rejected(self):
        for promised in ('2026-02-30', 'not-a-date', '2026-09-01'):
            with self.subTest(promised=promised), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('UPDATE purchase_orders SET promised_date = ? WHERE id = 2', (promised,))

    def test_report_escapes_data_and_handles_empty_result(self):
        rows = get_risks(self.db, '2026-10-05')
        rows[0]['supplier'] = '<script>unsafe</script>'
        html = build_report(rows, '2026-10-05')
        self.assertNotIn('<script>unsafe</script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('{{', html)
        empty = build_report([], '2026-10-05')
        self.assertIn('Gecikmiş açık kalem yok', empty)
        self.assertIn('0 ₺', empty)


if __name__ == '__main__':
    unittest.main(verbosity=2)
