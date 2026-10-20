from pathlib import Path
import shutil
import sqlite3
import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = next(d / 'data' / 'warehouse.db' for d in (HERE, *HERE.parents) if (d / 'data' / 'warehouse.db').exists())
DST = HERE / 'challenge.db'
shutil.copyfile(SRC, DST)

CHECK = '''SELECT (SELECT COUNT(*) FROM fact_sales)                     AS fact_rows,
                  (SELECT SUM(quantity * unit_price) FROM fact_sales)   AS fact_revenue,
                  (SELECT COUNT(*) FROM sales)                          AS view_rows,
                  (SELECT COUNT(DISTINCT order_id) FROM sales)          AS orders,
                  (SELECT SUM(amount) FROM sales)                       AS view_revenue'''

con = sqlite3.connect(DST)
con.execute('PRAGMA foreign_keys=ON')
before = pd.read_sql_query(CHECK, con)

# product_key 1=Tea(50), 2=Cookie(80); store_key 1=Bangsaen(Chonburi), 2=Siam(Bangkok)
try:
    con.execute("INSERT INTO dim_date VALUES (20261001, '2026-10-01', 2026, '2026-10')")
    con.executemany('INSERT INTO fact_sales VALUES (?,?,?,?,?,?,?)', [
        ('O1007', 1, 20261001, 1, 1, 3, 50),
        ('O1007', 2, 20261001, 2, 1, 2, 80),
        ('O1008', 1, 20261001, 1, 2, 4, 50),
    ])
    assert not con.execute('PRAGMA foreign_key_check').fetchall(), 'FK violation'
    con.commit()
except Exception:
    con.rollback()
    raise

after = pd.read_sql_query(CHECK, con)
df = pd.read_sql_query('SELECT * FROM sales', con)
con.close()

print('ก่อน INSERT\n', before.to_string(index=False))
print('\nหลัง INSERT\n', after.to_string(index=False))
row = after.iloc[0]
assert row.fact_rows == row.view_rows and row.fact_revenue == row.view_revenue, 'JOIN lost or duplicated rows'

pivot = pd.pivot_table(df, index='province', columns='month', values='amount',
                       aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
assert pivot.loc['Total', 'Total'] == df['amount'].sum()
print('\nPivot province x month (มีคอลัมน์ 2026-10 เพิ่มเองอัตโนมัติ)\n', pivot)
pivot.to_csv(HERE.parent / 'results' / 'challenge_pivot_oct.csv', encoding='utf-8-sig')
