SELECT movies.title as title, genres.title as genre
FROM movies_genres
JOIN movies ON movie_id = movies.id
JOIN genres ON genre_id = genres.id;
