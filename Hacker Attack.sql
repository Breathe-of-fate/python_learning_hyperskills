CREATE TABLE "person"(
             "person_id" VARCHAR(9) PRIMARY KEY,
             "full_name" TEXT,
             "address" TEXT,
             "building_number" TEXT,
             "phone_number" TEXT);

.mode csv
.import --skip 1 person.csv person
.mode column

/*SELECT person_id, full_name 
FROM person
ORDER BY person_id ASC
LIMIT 5;*/

/*-------------------here ends stage 1 - to create table, import data and show it*/

CREATE TABLE "teacher"(
             "person_id" VARCHAR(9) PRIMARY KEY,
             "class_code" TEXT);

.mode csv
.import --skip 1 teacher.csv teacher
.mode column
.print

/*SELECT person_id, full_name
FROM person
WHERE person_id not in (SELECT person_id
                        FROM teacher)
ORDER BY full_name
LIMIT 5;

.print

SELECT COUNT(person_id)
FROM person
WHERE person_id not in (SELECT person_id
                        FROM teacher)
ORDER BY full_name;*/

/*-------------------here ends stage 2 - to create table, import data and show it*/

CREATE TABLE "student"(
             "person_id" VARCHAR(9) PRIMARY KEY,
             "grade_code" TEXT);

INSERT INTO student (person_id)
SELECT person_id
FROM person
WHERE person_id not in (SELECT person_id
                        FROM teacher);

/*SELECT * 
FROM student
ORDER BY person_id
LIMIT 5;*/

/*-------------------here ends stage 3 - to create table, import data from another table and show it*/

CREATE TABLE "score1"(
             "person_id" VARCHAR(9),
             "score" INTEGER);

CREATE TABLE "score2"(
             "person_id" VARCHAR(9),
             "score" INTEGER);

CREATE TABLE "score3"(
             "person_id" VARCHAR(9),
             "score" INTEGER);

.mode csv
.import --skip 1 score1.csv score1
.import --skip 1 score2.csv score2
.import --skip 1 score3.csv score3
.mode column

/*SELECT * FROM score1
UNION ALL
SELECT * FROM score2
UNION ALL
SELECT * FROM score3*/

/*-------------------here ends stage 4 - to create 3 tables, union it and show*/

CREATE TABLE "score"(
             "person_id" VARCHAR(9),
             "score" INTEGER);

INSERT INTO score
SELECT * 
FROM
    (SELECT * FROM score1
    UNION ALL
    SELECT * FROM score2
    UNION ALL
    SELECT * FROM score3);

DROP TABLE score1;
DROP TABLE score2;
DROP TABLE score3;

/*SELECT * FROM score
ORDER BY person_id
LIMIT 5;

.print

SELECT person_id, count(score)
FROM score
GROUP BY person_id
HAVING count(score) = 3
ORDER BY person_id
LIMIT 5;*/

/*-------------------here ends stage 5 - to combine 3 tables, insert it in one, drop 3 temp tables and show 2 more*/

UPDATE student
SET grade_code = "GD-09"
WHERE person_id IN (SELECT person_id FROM student
                    WHERE person_id NOT IN (SELECT person_id FROM score));

UPDATE student
SET grade_code = "GD-10"
WHERE person_id IN (SELECT person_id 
                    FROM (SELECT person_id, count(score) OVER(PARTITION BY person_id) as "count(score)" FROM score)
                    WHERE "count(score)" = 1);

UPDATE student
SET grade_code = "GD-11"
WHERE person_id IN (SELECT person_id 
                    FROM (SELECT person_id, count(score) OVER(PARTITION BY person_id) as "count(score)" FROM score)
                    WHERE "count(score)" = 2);

UPDATE student
SET grade_code = "GD-12"
WHERE person_id IN (SELECT person_id 
                    FROM (SELECT person_id, count(score) OVER(PARTITION BY person_id) as "count(score)" FROM score)
                    WHERE "count(score)" = 3);

/*SELECT * FROM student ORDER BY person_id LIMIT 5;*/

/*-------------------here ends stage 6 - to update grades and show 5 lines*/

SELECT person_id, round(avg(score), 2) as "avg_score" 
FROM score
WHERE person_id IN
                  (SELECT person_id FROM student
                   WHERE grade_code = "GD-12")
GROUP BY person_id ORDER BY "avg_score" DESC