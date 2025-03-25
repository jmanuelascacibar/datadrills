/* Find the number of workers by department 
 who joined on or after April 1, 2014.
Output the department name along with the corresponding number of workers.
Sort the results based on the number of workers in descending order.*/

SELECT department,
       COUNT(worker_id) AS num_workers
FROM worker
WHERE MONTH(joining_date) >= 4
GROUP BY department
ORDER BY num_workers DESC
