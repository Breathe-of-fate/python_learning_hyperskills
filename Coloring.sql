/*Stage 1
SELECT id, name FROM Square
WHERE Square.id NOT IN (SELECT square_id FROM Painting)
ORDER BY name DESC
*/

/*Stage 2
SELECT color, SUM(volume) as total_paint_used FROM Spray
JOIN Painting ON id = spray_id
GROUP BY color
ORDER BY total_paint_used
*/

/*Stage 3
SELECT id, 255 - sum(coalesce(volume, 0)) as remaining_volume FROM Spray
LEFT JOIN Painting on id = spray_id
GROUP by id
*/

/*Stage 4
SELECT square_id, COUNT(DISTINCT spray_id) AS num_sprays FROM Painting
*/

/*Stage 5
select distinct name
from Spray
join Painting on id = spray_id
where color = 'R'
group by square_id, name
having count(color = 'R') > 1 and count(color = 'B') > 0;
*/

/*Stage 6*/
WITH empty_cans AS (SELECT spray_id
                    FROM Painting
                    GROUP by spray_id
                    HAVING sum(volume) = 255)
    
SELECT Square.name
FROM Painting
JOIN Spray on Spray.id = Painting.spray_id
JOIN Square on Painting.square_id = Square.id
JOIN empty_cans on empty_cans.spray_id = Painting.spray_id
GROUP by Painting.square_id
HAVING sum(volume) = 765
ORDER by Painting.square_id;
