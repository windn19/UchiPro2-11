SELECT COUNT(title) as count, director_id
FROM movies
GROUP BY director_id;

