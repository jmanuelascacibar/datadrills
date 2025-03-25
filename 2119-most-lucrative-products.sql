/* select the 5 most lucrative products
 in terms of total revenue for thee first half of 2022 */

WITH cte AS (
    SELECT product_id,
            SUM(cost_in_dollars * units_sold) AS revenue,
            RANK() OVER (ORDER BY SUM(cost_in_dollars * units_sold) DESC) AS rnk
    FROM online_orders
    WHERE MONTH(date_sold) BETWEEN 1 AND 6
    GROUP BY product_id
)
SELECT product_id, revenue
FROM cte
WHERE rnk <= 5;

/* Using nested queries */
SELECT product_id, revenue
FROM (
    SELECT  product_id,
            SUM(cost_in_dollars * units_sold) as revenue,
            RANK() OVER (ORDER BY SUM(cost_in_dollars * units_sold) DESC) as rnk
    FROM online_orders
    WHERE MONTH(date_sold) BETWEEN 1 AND 6
    GROUP BY product_id
) as subquery_result
WHERE rnk <=5;
