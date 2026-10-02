"""SQL'den taşınabilir HTML raporu ve CSV üretir. Harici paket yoktur."""
import argparse
import csv
from datetime import date
from html import escape
from pathlib import Path
import sqlite3

from run import ROOT, initialize


def get_risks(db, as_of_date):
    date.fromisoformat(as_of_date)
    cursor = db.execute((ROOT / 'risk.sql').read_text(encoding='utf-8'), {'as_of_date': as_of_date})
    columns = [field[0] for field in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]


def money(kurus):
    return f'{kurus / 100:,.0f}'.replace(',', '.') + ' ₺'


def build_report(rows, as_of_date):
    overdue = [row for row in rows if row['overdue_days'] > 0]
    due_today = [row for row in rows if row['status'] == 'Bugün bekleniyor']
    cards = [
        ('AÇIK SİPARİŞ TUTARI', money(sum(r['open_value_kurus'] for r in rows)), 'Onaylı siparişlerin teslim alınmayan kısmı'),
        ('GECİKMİŞ TUTAR', money(sum(r['open_value_kurus'] for r in overdue)), f"{len(set(r['order_id'] for r in overdue))} sipariş için tedarikçi takibi"),
        ('BUGÜN BEKLENEN', money(sum(r['open_value_kurus'] for r in due_today)), 'Termin günü gecikme sayılmaz'),
        ('AÇIK SİPARİŞ', str(len(set(r['order_id'] for r in rows))), f'{len(rows)} ürün kalemi • taslaklar hariç'),
    ]
    cards_html = ''.join(f'<article class="metric"><div class="label">{label}</div><strong>{value}</strong><p>{hint}</p></article>' for label, value, hint in cards)
    table = ''
    for row in rows:
        state = 'late' if row['overdue_days'] else ('today' if row['status'] == 'Bugün bekleniyor' else 'planned')
        table += f'''<tr data-state="{state}" data-value="{row['open_value_kurus']}"><td class="mono">PO-{row['order_id']:03}</td>
        <td><b>{escape(row['supplier'])}</b><small>{escape(row['product'])}</small></td>
        <td>{escape(row['promised_date'])}</td><td>{row['remaining']} adet</td>
        <td class="number">{money(row['open_value_kurus'])}</td>
        <td><span class="badge {state}">{escape(row['status'])}</span></td>
        <td>{str(row['overdue_days']) + ' gün' if row['overdue_days'] else '—'}</td></tr>'''
    if overdue:
        first = overdue[0]
        action = f"{escape(first['supplier'])} ile PO-{first['order_id']:03} için iletişime geç. {first['remaining']} adet {escape(first['product']).lower()} {first['overdue_days']} gündür bekleniyor; yeni teslim tarihini teyit et."
    else:
        action = 'Gecikmiş açık kalem yok. Bugün beklenen teslimatları kontrol et.'
    template = (ROOT / 'templates' / 'report.html').read_text(encoding='utf-8')
    for token, value in {'DATE': escape(as_of_date), 'CARDS': cards_html, 'ROWS': table, 'ACTION': action}.items():
        template = template.replace('{{' + token + '}}', value)
    return template


def main():
    parser = argparse.ArgumentParser(description='Satın alma kontrol raporu')
    parser.add_argument('--as-of', default='2026-10-05', help='Rapor tarihi; örnek: 2026-10-05')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs' / 'demo')
    args = parser.parse_args()
    try:
        date.fromisoformat(args.as_of)
    except ValueError:
        parser.error('Tarih YYYY-MM-DD biçiminde ve geçerli olmalı.')
    if args.as_of < '2026-10-03':
        parser.error('Sunum senaryosu için 2026-10-03 veya sonrasını seçin.')
    with sqlite3.connect(':memory:') as db:
        initialize(db)
        db.executescript((ROOT / 'demo.sql').read_text(encoding='utf-8'))
        rows = get_risks(db, args.as_of)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'index.html').write_text(build_report(rows, args.as_of), encoding='utf-8')
    with (args.output / 'open-orders.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['order_id', 'supplier', 'product', 'promised_date', 'remaining', 'open_value_kurus', 'overdue_days', 'status'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'HTML: {args.output / "index.html"}\nCSV: {args.output / "open-orders.csv"}')


if __name__ == '__main__':
    main()
