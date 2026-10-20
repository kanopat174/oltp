from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parent
# data/ อยู่ในโฟลเดอร์เดียวกัน หรือโฟลเดอร์แม่ (กรณีเก็บงานไว้ใน submission/)
DB=next((d/'data'/'warehouse.db' for d in (ROOT,ROOT.parent) if (d/'data'/'warehouse.db').exists()),None)
if DB is None:raise SystemExit('Run lab.py first')
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)
with sqlite3.connect(DB.as_uri()+'?mode=ro',uri=True) as con:
    df=pd.read_sql_query('SELECT * FROM sales',con)
print(df.head())

# P1: province x month, sum(amount), fill_value=0, margins=True
p1=pd.pivot_table(df,index='province',columns='month',values='amount',
                  aggfunc='sum',fill_value=0,margins=True,margins_name='Total')
print('\nP1 province x month (sum)\n',p1)

# P2: filter September, then category x province
sep=df[df['month']=='2026-09']
p2=pd.pivot_table(sep,index='category',columns='province',values='amount',aggfunc='sum',fill_value=0)
print('\nP2 September: category x province (sum)\n',p2)

# P3: assert เฉพาะเซลล์ Total x Total (ไม่รวมทุกเซลล์ เพราะแถว/คอลัมน์ Total จะนับซ้ำ)
grand=p1.loc['Total','Total']
assert grand==df['amount'].sum(),f'Grand total mismatch: {grand} != {df["amount"].sum()}'
print(f'\nassert OK: P1 Total x Total = {grand} = df["amount"].sum() = {df["amount"].sum()}')

# ทดลองข้อผิดพลาด: ไม่ระบุ aggfunc -> pandas ใช้ค่าเริ่มต้น mean
p1_mean=pd.pivot_table(df,index='province',columns='month',values='amount',fill_value=0)
print('\nก่อนแก้ (ลบ aggfunc -> mean)\n',p1_mean)
print('หลังแก้ (aggfunc="sum")\n',p1.drop(index='Total',columns='Total'))
print('Bangkok 2026-09 mean =',p1_mean.loc['Bangkok','2026-09'],'| sum =',p1.loc['Bangkok','2026-09'])

# Drink (แทน Excel PivotTable): Filters=category=Drink, Rows=province, Columns=month, Values=Sum(amount)
drink=pd.pivot_table(df[df['category']=='Drink'],index='province',columns='month',values='amount',
                     aggfunc='sum',fill_value=0,margins=True,margins_name='Total')
print('\nDrink: province x month (sum)\n',drink)
print('ยอดรวมหลังกรอง Drink =',drink.loc['Total','Total'])

# P4: export each result to CSV in your submission folder
p1.to_csv(OUT/'pivot_province_month.csv',encoding='utf-8-sig')
p2.to_csv(OUT/'pivot_september.csv',encoding='utf-8-sig')
drink.to_csv(OUT/'pivot_drink.csv',encoding='utf-8-sig')
p1_mean.to_csv(OUT/'pivot_mean_mistake.csv',encoding='utf-8-sig')
print('\nsaved:',', '.join(f.name for f in sorted(OUT.glob('pivot_*.csv'))))
