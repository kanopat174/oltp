-- Challenge A1: top 3 stores by revenue (extended.db)
SELECT store_name, province, SUM(amount) AS revenue, COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY store_name, province
ORDER BY revenue DESC
LIMIT 3;
