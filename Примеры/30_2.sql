SELECT title
FROM genres
WHERE id in
   (SELECT genre_id
    FROM movies_genres
    WHERE movie_id =
        (SELECT id
         FROM movies
         WHERE title = 'Интерстеллар') );
