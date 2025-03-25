# Question

You have been asked to find the 5 most lucrative products in terms of total revenue for the first half of 2022 (from January to June inclusive).

Output their IDs and the total revenue.

# Answer

The first thing is to create a `cte` (Common table expression) that will be use later in the query.

### CTE

A CTE is a temporary table that exists only for the duration of your query. It's like a mini query that you can later use in your main query.

When you write `WITH cte as (...)`, you're saying: I'm going to define a temporary result set called 'cte' that contains the following data, I'll refer to this result set later in my query. 

In our task:

````sql
WITH cte AS (
  SELECT product_id,
         SUM(cost_in_dollars * units_sold) AS revenue,
         RANK() OVER (ORDER BY SUM(cost_in_dollars * units_sold) DESC) AS rnk
  FROM online_orders
  WHERE MONTH(date_sold) BETWEEN 1 AND 6
  GROUP BY product_id
)
````
This creates a temporary result set called 'cte' that contains 3 columns:
- product_id
- revenue (the sum of cost in dollar * units sold)
- rnk (the rank of each product based on revenue)

Then the main query uses this CTE:

````sql
SELECT product_id, revenue
FROM cte
WHERE rnk <= 5;
````

This select only the product id and revenue column from the CTE, filtering to include only the top 5 ranked products by revenue. 

### Why do you need to repeat the revenue calculation to the RANK function?

When SQL processes your query, it first identities all the columns to retrieve product_id` and the sum calculation. Then it calculates the window functions RANK in this case. After these steps are complete, it applies the aliases to the result columns. Since the alias `revenue` isn't visible to the RANK function during processing, you need to repeat the entire calculation. 


### Using a nested subqueries 

You can also create a query without using CTE. You would need to write nested subquery. 

A nested subquery is a query that is contained inside another query like a Russian doll. 

```sql
SELECT product_id, revenue
FROM (
    SELECT  product_id,
            SUM(cost_in_dollars * units_sold) as revenue,
            RANK() OVER (ORDER BY SUM(cost_in_dollars * units_sold) DESC) AS rnk
    FROM online_orders
    WHERE MONTH(date_sold) BETWEEN 1 AND 6
    GROUP BY product_id
) as subquery_result
WHERE rnk <=5;
```

The entire calculation for product revenues and rankings happens inside parenthesis as an inner query (the subquery).
