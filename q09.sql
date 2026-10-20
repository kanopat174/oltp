-- q09 Monthly subtotal + ALL row via UNION ALL
SELECT month, revenue FROM (
    SELECT month, SUM(amount) AS revenue, 0 AS sort_key
    FROM sales
    GROUP BY month
    UNION ALL
    SELECT 'ALL', SUM(amount), 1
    FROM sales
)
ORDER BY sort_key, month;
