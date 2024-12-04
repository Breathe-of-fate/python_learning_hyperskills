/*Stage1
SELECT pc_code, model, speed, ram
FROM PC
WHERE ram >= 16
ORDER by ram, speed DESC

Stage2
SELECT round(AVG(price), 2) as average_price
FROM Printer
WHERE type = "Inkjet" and color = "C"

Stage3
SELECT maker, SUM(price) as total_price FROM Laptop
JOIN Product on Laptop.model= Product.model
GROUP by maker
ORDER by total_price

Stage4
SELECT 
    maker,
    SUM(CASE WHEN type = 'PC' THEN 1 ELSE 0 END) AS pc_count,
    SUM(CASE WHEN type = 'Laptop' THEN 1 ELSE 0 END) AS laptop_count
FROM 
    Product
GROUP BY 
    maker
HAVING
	laptop_count <> 0 AND pc_count <> 0
	
Stage5*/

WITH RankedPCs AS (SELECT
                        pc_code,
                        model,
                        speed,
                        ram,
                        hd,
                        cd,
                        price,
                        RANK() OVER (PARTITION BY ram ORDER BY price DESC) AS price_rank
                    FROM PC)
SELECT
    pc_code,
    model,
    speed,
    ram,
    hd,
    cd,
    price
FROM
    RankedPCs
WHERE
    price_rank = 2;
