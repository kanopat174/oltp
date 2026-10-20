from pathlib import Path
import sqlite3
ROOT=Path(__file__).resolve().parent
# data/ อยู่ในโฟลเดอร์เดียวกัน หรือโฟลเดอร์แม่ (กรณีเก็บงานไว้ใน submission/)
p=next((d/'data'/'oltp.db' for d in (ROOT,ROOT.parent) if (d/'data'/'oltp.db').exists()),None)
if p is None:raise SystemExit('Run lab.py first')
with sqlite3.connect(p) as con:
    print('Before:',con.execute('SELECT * FROM orders').fetchall())
    # Guarded UPDATE: เปลี่ยนเฉพาะออเดอร์ O1004 ที่ยังเป็น PENDING เท่านั้น
    cur=con.execute("UPDATE orders SET status='PAID' WHERE order_id=? AND status='PENDING'",('O1004',))
    print('rowcount:',cur.rowcount)
    print('After:',con.execute('SELECT * FROM orders').fetchall())
# Run twice. Explain why the second guarded UPDATE should affect 0 rows.
