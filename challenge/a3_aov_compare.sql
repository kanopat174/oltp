-- Challenge A3: overall AOV vs simple average of monthly AOV vs order-weighted average
WITH m AS (
    SELECT month, SUM(amount) AS revenue, COUNT(DISTINCT order_id) AS orders,
           SUM(amount) * 1.0 / COUNT(DISTINCT order_id) AS aov
    FROM sales
    GROUP BY month
)
SELECT (SELECT ROUND(SUM(amount) * 1.0 / COUNT(DISTINCT order_id), 2) FROM sales) AS overall_aov,
       ROUND(AVG(aov), 2)                                    AS avg_of_monthly_aov,
       ROUND(SUM(aov * orders) / SUM(orders), 2)             AS order_weighted_aov
FROM m;
