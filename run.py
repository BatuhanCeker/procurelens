"""SQL dosyalarini calistiran yardimci. Harici paket gerektirmez."""
import argparse
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent


def initialize(db):
    db.execute('PRAGMA foreign_keys = ON')
    for name in ('schema.sql', 'guards.sql', 'seed.sql', 'workflow.sql'):
        try:
            db.executescript((ROOT / name).read_text(encoding='utf-8'))
        except sqlite3.Error:
            db.rollback()
            raise


def report_queries():
    text = (ROOT / 'reports.sql').read_text(encoding='utf-8')
    for block in text.split('-- report: ')[1:]:
        title, query = block.split('\n', 1)
        yield title, query


def main():
    parser = argparse.ArgumentParser(description='Satın alma ve stok SQL laboratuvarı')
    parser.add_argument('--save', type=Path, help='Yeni bir SQLite dosyasına kaydet; mevcut dosyaya dokunmaz.')
    args = parser.parse_args()
    if args.save:
        # x modu: var olan veritabanini yanlislikla silme veya ezme.
        try:
            args.save.open('x').close()
        except FileExistsError:
            parser.error('Bu dosya zaten var. Yeni bir dosya adı seçin.')
    with sqlite3.connect(str(args.save) if args.save else ':memory:') as db:
        initialize(db)
        for title, query in report_queries():
            print(f'\n{title}')
            cursor = db.execute(query)
            print(' | '.join(column[0] for column in cursor.description))
            for row in cursor:
                print(' | '.join(str(value) for value in row))
    if args.save:
        print(f'\nKaydedildi: {args.save.resolve()}')


if __name__ == '__main__':
    main()
