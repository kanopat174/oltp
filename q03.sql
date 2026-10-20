-- q03 Add location dimension to monthly result
SELECT month, province, SUM(amount) AS revenue
FROM sales
GROUP BY month, province
ORDER BY month, province;
