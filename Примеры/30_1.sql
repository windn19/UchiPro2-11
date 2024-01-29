SELECT title
FROM movies
WHERE director_id =
   (SELECT id
    FROM directors
    WHERE name = 'Кристофер Нолан');
