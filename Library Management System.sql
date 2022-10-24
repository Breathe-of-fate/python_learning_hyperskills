PRAGMA foreign_keys = ON;

create_book_table = "CREATE TABLE book (
    id INTEGER PRIMARY KEY NOT NULL,
    isbn TEXT NOT NULL,
    book_name TEXT NOT NULL,
    genre TEXT NOT NULL,
    author TEXT NOT NULL,
    book_year INTEGER NOT NULL,
    book_count INTEGER NOT NULL,
    book_page INTEGER NOT NULL,
    rank REAL NOT NULL
);"

insert_book_table = "INSERT INTO book VALUES 
    (1, '0393347095', 'The Metamorphosis', 'Novella', 'Franz Kafka', 2014, 2, 128, 4.4),
    (2, '0439358078', 'Harry Potter And The Order Of The Phoenix', 'Fantasy', 'J.K. Rowling', 2004, 3, 896, 4.2),
    (3, '0198800533', 'Anna Karenina', 'Realist Novel', 'Leo Tolstoy', 2017, 1, 896, 4.6);"

create_operation_table = "CREATE TABLE operation (
    id INTEGER PRIMARY KEY NOT NULL,
    student_id INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    iss_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    return_indicator NUMERIC NOT NULL,
    CONSTRAINT FK_book_id
    FOREIGN KEY (book_id) REFERENCES book (id),
    CONSTRAINT FK_student_id
    FOREIGN KEY (student_id) REFERENCES student (id),
    CONSTRAINT FK_staff_id
    FOREIGN KEY (staff_id) REFERENCES staff (id)
);"

insert_operation_table = "INSERT INTO operation VALUES
    (1, 3, 1, 1, DATE('now', '-4 day'), DATE('now', '+10 day'), 0),
    (2, 1, 1, 3, DATE('now', '-1 day'), DATE('now', '+13 day'), 0),
    (3, 2, 2, 2, DATE('now', '-1 day'), DATE('now', '+6 day'), 0),
    (4, 4, 2, 2, DATE('now'), DATE('now', '+14 day'), 0)
;"

create_student_table = "CREATE TABLE student (
    id INTEGER PRIMARY KEY NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth TEXT NOT NULL
);"

insert_student_table = "INSERT INTO student VALUES 
    (1, 'Mia Yang', 'Female', '1996-09-15'),
    (2, 'Bob Lee', 'Male', '1997-12-13'),
    (3, 'Eric Rampy', 'Male', '1995-08-21'),
    (4, 'Stefany Ferenz', 'Female', '1996-04-01')
;"

create_staff_table = "CREATE TABLE staff (
    id INTEGER PRIMARY KEY NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth TEXT NOT NULL
);"

insert_staff_table = "INSERT INTO staff VALUES 
    (1, 'Steve Smith', 'Male', '1992-04-23'),
    (2, 'Ashley Miller', 'Female', '1995-01-16')
;"

update_staff_inf = "UPDATE staff SET full_name = 'Ashley Bailey' WHERE full_name = 'Ashley Miller';"
update_operation_inf = "UPDATE operation SET return_date = DATE('now'), return_indicator = 1 WHERE student_id = 3;"
update_book_inf = "UPDATE book SET book_count = book_count + 1 WHERE book_name = 'The Metamorphosis';"

student_inf = "SELECT full_name FROM student JOIN operation ON student.id = operation.student_id WHERE operation.book_id = 2;"