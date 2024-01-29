SELECT AVG(duration) as avg, director_id
FROM movies
GROUP BY director_id
HAVING avg > 120;