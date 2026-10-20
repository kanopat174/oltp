-- q11 Rows and revenue before JOIN (fact_sales) vs after JOIN (sales view) + FK check
SELECT 'before_join_fact_sales' AS source,
       COUNT(*) AS row_count,
       SUM(quantity * unit_price) AS revenue,
       (SELECT COUNT(*) FROM pragma_foreign_key_check) AS fk_violations
FROM fact_sales
UNION ALL
SELECT 'after_join_sales_view',
       COUNT(*),
       SUM(amount),
       (SELECT COUNT(*) FROM pragma_foreign_key_check)
FROM sales;
