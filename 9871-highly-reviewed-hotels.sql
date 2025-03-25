/* List all hotels with their total number of reviews
Show the results sorted by the number of reviews from highest to lowest
output the hotel name along with the reviews */

SELECT hotel_name, total_number_of_reviews
FROM hotel_reviews
GROUP BY hotel_name, total_number_of_reviews /*remove duplicates*/
ORDER BY total_number_of_reviews DESC;
