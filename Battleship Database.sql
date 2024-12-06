/*Stage 1
SELECT ship, result FROM Outcomes
WHERE battle = "Pearl Harbor"
ORDER BY ship

Stage 2
SELECT class, numGuns FROM Classes
WHERE numGuns = (SELECT MAX(numGuns) FROM Classes)

Stage 3
SELECT country, COUNT(*) as num_battleships FROM Classes
WHERE type = "bb"
GROUP by country
ORDER by num_battleships DESC
LIMIT 1

Stage 4
SELECT country, count(ship) as num_sunk_ships FROM Outcomes
JOIN Ships on Outcomes.ship = Ships.name
JOIN Classes on Ships.class = Classes.class
WHERE result = "sunk"
GROUP by country
ORDER by num_sunk_ships DESC

Stage 5
WITH temp_table AS 
	(SELECT
	 Ships.name, 
	 Ships.launched, 
	 Classes.country,
	 MIN(Ships.launched) OVER (PARTITION BY Classes.country) AS min_launched
	 FROM Ships
	 JOIN Classes ON Ships.class = Classes.class
	 WHERE Ships.name <> 'HMS Queen Elizabeth')


SELECT
    name, 
    launched, 
    country
FROM
	temp_table
WHERE
	launched = min_launched
GROUP by
	name
ORDER by 
	launched;

Stage 6*/

SELECT DISTINCT 
	Classes.class,  
	SUM(result = "damaged") as num_damaged,
	SUM(result = "sunk") as num_sunk,
	SUM(result = "OK") as num_ok
FROM 
	Classes
JOIN 
	Ships on Classes.class = Ships.class
JOIN
	Outcomes on Ships.name = Outcomes.ship
GROUP by 
	Classes.class
HAVING 
    COUNT(*) >= 3