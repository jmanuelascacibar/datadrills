/* Find the number of employees 
 working in the Admin department 
 that joined in April or later.*/

SELECT COUNT(*) as number_admins
FROM worker
WHERE LOWER(department) = "admin" 
AND MONTH(joining_date) >=4;
