/* Stage1
SELECT model, type, price 
FROM Printer
WHERE price >= 200
*/

/* Stage 2
SELECT maker, Laptop.model, hd, speed, price
	FROM Laptop
JOIN Product ON Laptop.model = Product.model
WHERE hd >= 1000
ORDER BY hd, speed DESC, price
*/

/* Stage 3
SELECT COUNT(amount) as Number FROM 
	(SELECT COUNT(model) as amount FROM Product
	GROUP by maker
	HAVING amount = 1) as wtf
*/

WITH all_comps AS (SELECT model, speed, price FROM Laptop
                   UNION
                   SELECT model, speed, price FROM PC),
				   
	 plus_maker AS (SELECT maker, all_comps.model, speed, price FROM all_comps
				   JOIN Product on all_comps.model = Product.model)

				   SELECT maker, model, speed, price FROM plus_maker
				   WHERE speed = (SELECT MIN(speed) FROM all_comps)