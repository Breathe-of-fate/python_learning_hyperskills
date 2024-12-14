/*Stage 1
ALTER TABLE Pass_in_trip
MODIFY COLUMN trip_date DATE;

UPDATE Pass_in_trip
SET trip_date = DATE(trip_date);

SELECT * FROM Pass_in_trip*/

/*Stage 2
SELECT 
    Passenger.passenger_name, 
    COUNT(Passenger.passenger_name) as num_flights, 
    company_name FROM Airline_company
JOIN Trip ON Airline_company.ID_comp = Trip.ID_comp
JOIN Pass_in_trip ON Trip.trip_no = Pass_in_trip.trip_no
JOIN Passenger ON Pass_in_trip.ID_psg = Passenger.ID_psg
GROUP by Passenger.passenger_name, company_name
HAVING num_flights > 1*/

/*Stage 3
SELECT  
      CONCAT(town_from, "-", town_to) as route,
      AVG(TIMESTAMPDIFF(MINUTE, time_out, time_in)) as avg_flight_duration,
      COUNT(Pass_in_trip.seat_number) as total_passengers,
      AVG(TIMESTAMPDIFF(SECOND, time_out, time_in)) * COUNT(Pass_in_trip.seat_number) * 0.01 as total_income
FROM Trip
JOIN Pass_in_trip on Trip.trip_no = Pass_in_trip.trip_no
GROUP by route
ORDER by total_income DESC*/

/*Stage 4
SELECT
      CASE WHEN plane_type LIKE "%Boeing%" THEN "Boeing" ELSE "Airbus" END as aircraft_type,
      AVG(TIMESTAMPDIFF(MINUTE, time_out, time_in)) as avg_flight_duration,
      COUNT(*) as num_flights
FROM Trip
GROUP by aircraft_type*/

/*Stage 5
WITH NewTable AS 
(SELECT company_name, 
               town_from as departure_city, 
               town_to as arrival_city,
               AVG(TIMESTAMPDIFF(MINUTE, time_out, time_in)) as avg_flight_duration,
               ROW_NUMBER() OVER (PARTITION BY company_name ORDER by AVG(TIMESTAMPDIFF(MINUTE, time_out, time_in)) DESC) as rate
       FROM Airline_company
       JOIN Trip on Airline_company.ID_comp = Trip.ID_comp
       GROUP by company_name, departure_city, arrival_city)

SELECT company_name,
       departure_city,
       arrival_city,
       avg_flight_duration
FROM NewTable
WHERE rate <=2*/

/*Stage 6 */
WITH passenger_income AS 
    (SELECT
    p.ID_psg,
    p.passenger_name,
    SUM(TIMESTAMPDIFF(SECOND, t.time_out, t.time_in) * 0.01) AS passenger_income_dollars,
    SUM(TIMESTAMPDIFF(SECOND, t.time_out, t.time_in) * 0.01) / SUM(SUM(TIMESTAMPDIFF(SECOND, t.time_out, t.time_in) * 0.01)) OVER() * 100 AS percent
  FROM Passenger p 
    JOIN Pass_in_trip pit ON p.ID_psg = pit.ID_psg
    JOIN Trip t ON t.trip_no = pit.trip_no
  GROUP BY p.ID_psg
  ORDER BY percent DESC)
    
SELECT
    ID_psg,
    passenger_name,
    passenger_income_dollars,
    ROUND(SUM(percent) OVER (ORDER BY percent DESC), 2) AS cumulative_share_percent,
    CASE
    WHEN ROUND(SUM(percent) OVER (ORDER BY percent DESC), 2) <= 80 THEN 'A'
    WHEN ROUND(SUM(percent) OVER (ORDER BY percent DESC), 2) <= 95 THEN 'B'
    ELSE 'C'
END AS category
FROM passenger_income