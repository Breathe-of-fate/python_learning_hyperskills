/*Stage 1
CREATE PROCEDURE GetEmployeesByDept (IN dept_name VARCHAR(45))
BEGIN
    SELECT first_name, 
           last_name, 
           jobs.title AS job_title 
    FROM employees
    JOIN departments ON employees.department_id = departments.id
    JOIN jobs ON employees.job_id = jobs.id
    WHERE departments.name = dept_name
    ORDER BY first_name;
END;

CALL GetEmployeesByDept('Office of Finance');

Stage 2
CREATE PROCEDURE EmployeeTotalPay(
    IN first_name VARCHAR(45),
    IN last_name VARCHAR(45),
    IN total_hours INT,
    IN normal_hours INT,
    IN overtime_rate FLOAT,
    IN max_overtime_pay FLOAT,
    OUT total_pay FLOAT)
BEGIN
    DECLARE base_pay DOUBLE;
    DECLARE hourly_rate DOUBLE;
    DECLARE overtime_hours INT DEFAULT greatest(0, total_hours - normal_hours);
    DECLARE overtime_pay DOUBLE;
    DECLARE job_type VARCHAR(45);

    SELECT jobs.hourly_rate INTO hourly_rate
    FROM employees
    JOIN jobs ON employees.job_id = jobs.id
    WHERE employees.first_name = first_name and employees.last_name = last_name;

    SELECT jobs.type INTO job_type
    FROM employees
    JOIN jobs ON employees.job_id = jobs.id
    WHERE employees.first_name = first_name AND employees.last_name = last_name;

    SET base_pay = hourly_rate * least(total_hours, normal_hours);
    SET overtime_pay = IF(job_type = 'Full Time', least(overtime_hours * hourly_rate * overtime_rate, max_overtime_pay), 0);
    SET total_pay = base_pay + overtime_pay;
END;

CALL EmployeeTotalPay('Philip', 'Wilson', 2160, 2080, 1.5, 6000, @total_pay_philip);
CALL EmployeeTotalPay('Daisy', 'Diamond', 2100, 2080, 1.5, 6000, @total_pay_daisy);

SELECT
    @total_pay_philip as `Philip Wilson`,
    @total_pay_daisy as `Daisy Diamond`;


Stage 3
CREATE FUNCTION TaxOwed(taxable_income FLOAT)
RETURNS FLOAT
BEGIN
    DECLARE tax FLOAT;

    IF taxable_income <= 11000 THEN
        SET tax = taxable_income * 0.10;
    ELSEIF taxable_income <= 44725 THEN
        SET tax = 1100 + (taxable_income - 11000) * 0.12;
    ELSEIF taxable_income <= 95375 THEN
        SET tax = 5147 + (taxable_income - 44725) * 0.22;
    ELSEIF taxable_income <= 182100 THEN
        SET tax = 16290 + (taxable_income - 95375) * 0.24;
    ELSEIF taxable_income <= 231250 THEN
        SET tax = 37104 + (taxable_income - 182100) * 0.32;
    ELSEIF taxable_income <= 578125 THEN
        SET tax = 52832 + (taxable_income - 231250) * 0.35;
    ELSE
        SET tax = 174238.25 + (taxable_income - 578125) * 0.37;
    END IF;
RETURN ROUND(tax, 1);
END;

SELECT 
    TaxOwed(137164.80) AS 'Philip Wilson',
    TaxOwed(89232.00) AS 'Daisy Diamond';


Stage 4*/
CREATE FUNCTION EmployeeHourlyRate(full_name VARCHAR(91))
RETURNS FLOAT
BEGIN
    DECLARE hourly_rate FLOAT;
    SELECT j.hourly_rate
    INTO hourly_rate
    FROM employees AS e
    JOIN jobs AS j ON e.job_id = j.id
    WHERE CONCAT(e.first_name, ' ', e.last_name) = full_name;
    RETURN hourly_rate;
END;

CREATE FUNCTION EmployeeBasePay(full_name VARCHAR(91))
RETURNS FLOAT
BEGIN
    DECLARE hourly_rate FLOAT(10, 5);
    SET hourly_rate = EmployeeHourlyRate(full_name);
    RETURN 2080 * hourly_rate;
END;

CREATE FUNCTION EmployeeOvertimePay(full_name VARCHAR(91), hours_worked INT)
RETURNS FLOAT
BEGIN
    DECLARE overtime_hours INT;
    DECLARE overtime_rate FLOAT(10, 5);
    SET overtime_rate = EmployeeHourlyRate(full_name) * 1.5;
    SET overtime_hours = hours_worked - 2080;
    RETURN
        CASE 
            WHEN overtime_hours <= 0 THEN 0 
            WHEN overtime_hours * overtime_rate > 6000 THEN 6000
            ELSE overtime_hours * overtime_rate
        END;
END;

CREATE FUNCTION TaxOwed(taxable_income FLOAT)
RETURNS FLOAT
BEGIN
    RETURN
        CASE
            WHEN taxable_income BETWEEN 0 AND 11000 THEN taxable_income * 0.1
            WHEN taxable_income BETWEEN 11001 AND 44725 THEN (taxable_income - 11000) * 0.12 + 1100
            WHEN taxable_income BETWEEN 44726 AND 95375 THEN (taxable_income - 44725) * 0.22 + 5147
            WHEN taxable_income BETWEEN 95376 AND 182100 THEN (taxable_income - 95375) * 0.24 + 16290
            WHEN taxable_income BETWEEN 182101 AND 231250 THEN (taxable_income - 182100) * 0.32 + 37104
            WHEN taxable_income BETWEEN 231251 AND 578125 THEN (taxable_income - 231250) * 0.35 + 52832
            WHEN taxable_income > 578126 THEN (taxable_income - 578125) * 0.37 + 174238.25
        END;
END;

CREATE PROCEDURE PayrollReport(IN department VARCHAR(45))
BEGIN
    WITH EmployeeCTE AS (
        SELECT 'Dixie Herda' AS full_name, 2095 AS hours_worked UNION ALL
        SELECT 'Stephen West', 2091 UNION ALL
        SELECT 'Philip Wilson', 2160 UNION ALL
        SELECT 'Robin Walker', 2083 UNION ALL
        SELECT 'Antoinette Matava', 2115 UNION ALL
        SELECT 'Courtney Walker', 2206 UNION ALL
        SELECT 'Gladys Bosch', 900),
         CalculatedPay AS 
                            (SELECT
                                full_name,
                                hours_worked,
                                EmployeeBasePay(full_name) AS base_pay,
                                EmployeeOvertimePay(full_name, hours_worked) AS overtime_pay
                            FROM EmployeeCTE)
    SELECT
        full_name AS full_names,
        ROUND(base_pay, 2) AS base_pay,
        ROUND(overtime_pay, 2) AS overtime_pay,
        ROUND(base_pay + overtime_pay, 2) AS total_pay,
        ROUND(TaxOwed(base_pay + overtime_pay), 2) AS tax_owed,
        ROUND(base_pay + overtime_pay - TaxOwed(base_pay + overtime_pay), 2) AS net_income
    FROM CalculatedPay
    ORDER BY net_income DESC;
END;

CALL PayrollReport('City Ethics Commission');