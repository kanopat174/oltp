-- q08 SQL pivot: province x month
SELECT province,
       SUM(CASE WHEN month = '2026-08' THEN amount ELSE 0 END) AS aug,
       SUM(CASE WHEN month = '2026-09' THEN amount ELSE 0 END) AS sep,
       SUM(amount) AS total
FROM sales
GROUP BY province
ORDER BY province;
