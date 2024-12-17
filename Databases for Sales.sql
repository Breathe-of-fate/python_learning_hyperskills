/*Stage 1
CREATE TABLE IF NOT EXISTS manufacturers (
    manufacturer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45) NOT NULL,
    country VARCHAR(45) NOT NULL
);
    
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    manufacturer_id INT NOT NULL,
    model VARCHAR(45) NOT NULL,
    price DECIMAL NOT NULL,
    horsepower INT NOT NULL,
    fuel_efficiency INT NOT NULL,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers (manufacturer_id)
);
    
CREATE TABLE IF NOT EXISTS inventory (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL,
    reorder_level INT NOT NULL DEFAULT 2,
    last_inventory_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

Stage 2
CREATE TRIGGER update_inventory
AFTER INSERT ON sales
FOR EACH ROW
    UPDATE inventory
    SET quantity = quantity - NEW.quantity,
        last_inventory_date = NEW.sale_date
    WHERE product_id = NEW.product_id;

INSERT INTO sales (sale_date, customer_id, product_id, employee_id, quantity, total_price) 
VALUES
    (DATE('2023-05-01'), 1, 1, 1, 2, 56000.00),
    (DATE('2023-05-02'), 2, 2, 1, 1, 22000.00),
    (DATE('2023-05-02'), 1, 3, 2, 1, 41250.00),
    (DATE('2023-05-03'), 2, 4, 2, 2, 60000.00),
    (DATE('2023-05-03'), 1, 1, 2, 3, 84000.00);

SELECT * FROM inventory;

Stage 3
CREATE INDEX customer_sales_product
ON sales (customer_id, product_id);

CREATE VIEW sales_summary AS
SELECT p.model, SUM(s.quantity) AS total_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.model;

SELECT * FROM sales_summary;

Stage 4
WITH monthly_sales AS (
    SELECT
        employee_id,
        (SUM(quantity) / SUM(SUM(quantity)) OVER()) * 100 AS sales_percentage,
        DATE_FORMAT(sale_date, '%M %Y') AS month_year
    FROM sales
    GROUP BY employee_id, month_year
),
employee_monthly_bonus AS (
    SELECT
        employee_id,
        month_year,
        CASE 
            WHEN sales_percentage < 5 THEN 0 
            WHEN sales_percentage BETWEEN 5 AND 10 THEN 2000
            WHEN sales_percentage BETWEEN 10 AND 20 THEN 5000 
            WHEN sales_percentage BETWEEN 20 AND 30 THEN 10000
            WHEN sales_percentage BETWEEN 30 AND 40 THEN 15000 
            ELSE 25000
        END AS employee_bonus
    FROM monthly_sales
)


SELECT 
    CONCAT(employees.first_name, ' ', employees.last_name) AS employee_name,
    employees.position,
    employee_monthly_bonus.month_year,
    employee_monthly_bonus.employee_bonus
FROM employees
JOIN employee_monthly_bonus ON employees.employee_id = employee_monthly_bonus.employee_id
WHERE employees.position = 'Sales Associate';

Stage 5*/
SELECT 
    p.model,
    p.price,
    SUM(s.total_price) AS total_sale_per_model,
    i.quantity AS inventory_per_model,
    SUM(s.total_price) / i.quantity AS sales_inventory_ratio
FROM 
    products p
JOIN 
    sales s ON p.product_id = s.product_id
JOIN 
    inventory i ON p.product_id = i.product_id
GROUP BY 
    p.model, p.price, i.quantity
ORDER BY 
    sales_inventory_ratio DESC;