/* 1st stage
best_student = "SELECT name FROM Students
JOIN Student_Subject ON Students.student_id = Student_Subject.student_id
GROUP BY name
HAVING grade = 3 and avg(result) = 5" */

/* 2st stage
achievement_point = "SELECT name, sum(bonus) as [bonus point] FROM students
JOIN Student_Achievement on students.student_id = Student_Achievement.student_id
JOIN Achievement on Student_Achievement.achievement_id = Achievement.achievement_id
GROUP by name
ORDER by [bonus point] DESC
LIMIT 4" */

/* 3rd stage
average_student = "SELECT name, CASE 
	WHEN AVG(result) > 3.5 THEN 'above average'
	ELSE 'below average'
	END AS [best]
FROM Student_Subject
JOIN Students ON Student_Subject.student_id = Students.student_id
GROUP by name"*/

best_of_department = "SELECT name, department_name FROM Students
JOIN Student_Subject on Students.student_id = Student_Subject.student_id
JOIN Department on Students.department_id = Department.department_id
GROUP BY name
HAVING avg(result) > 4.5"