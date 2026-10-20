-- q02 Roll-up: day -> month
SELECT month, SUM(amount) AS revenue
FROM sales
GROUP BY month
ORDER BY month;
