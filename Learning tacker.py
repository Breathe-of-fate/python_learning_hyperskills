import re
import hashlib

def empty_checker(x):
    return True if not x or x.isspace() else False

def credentials_checker(x):
    if empty_checker(x):
        print("Incorrect credentials.")
        return None
    credentials = x.split()
    if credentials[0] == "back":
        return "back"
    elif len(credentials) < 3 and "@" not in x:
        print("Incorrect credentials.")
    else:
        name_pattern = r"(?i)^[a-z][a-z ]*(?:('|-)(?!['-])[a-z ]*)*[a-z]$"
        name = credentials[0]
        surname = ' '.join(credentials[1:-1])
        email = credentials[-1]
        if not re.fullmatch(name_pattern, name):
            print("Incorrect first name.")
        elif not re.fullmatch(name_pattern, surname):
            print("Incorrect last name.")
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{1,}\b', email):
            print("Incorrect email.")
        else:
            return [hashlib.md5(bytes(name+surname+email, "utf-8")).hexdigest(), name, surname, email]

def main_menu(user_choice):
    if empty_checker(user_choice):
        print("No input.")
    elif user_choice not in ("exit", "add students", "back", "list", "add points", "find", "statistics", "notify"):
        print("Unknown command!")
    else:
        return user_choice

def add_students():
    added_students = {}
    while True:
        user_choice = credentials_checker(input())
        if user_choice == "back":
            print(f"Total {len(added_students)} students have been added.")
            break
        elif not user_choice:
            continue
        if user_choice[3] in [added_students[i][0] for i in added_students]:
            print("This email is already taken.")
            continue
        added_students.setdefault(user_choice[0], [user_choice[3], user_choice[1], user_choice[2]])
        print("The student has been added.")
    return added_students

def add_points(x, y):
    print("Enter an id and points or 'back' to return")
    
    statistics = {"activity": {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0},
                  "popularity": {"Python": set(), "DSA": set(), "Databases": set(), "Flask": set()},
                  "difficulty": {}}
    
    while True:
        student_and_points = input().split(" ", 1)
        if student_and_points[0] == "back":
            
            statistics["popularity"] = {i: len(statistics["popularity"][i]) for i in statistics["popularity"]}
            
            for genre in statistics:
                if genre != "difficulty":
                    for course in statistics[genre]:
                        statistics[genre][course] += y[genre][course]
                else:
                    for student in statistics[genre]:
                        for index in range(0, 4):
                            statistics[genre][student][index] += y[genre][student][index]     
            
            return statistics
        
        else:
            if student_and_points[0] in x:
                if len(student_and_points) > 1 and re.match("^\d+ \d+ \d+ \d+$", student_and_points[1]):
                    new_points = [int(i) for i in student_and_points[1].split()]
                    
                    #amount of submissions
                    for i in statistics["activity"]:
                        statistics["activity"][i] += 1 if new_points[list(statistics["activity"]).index(i)] != 0 else 0
                        
                    #enrolled students
                    for i in range(0, 4):
                        if new_points[i] != 0:
                            statistics["popularity"][list(statistics["popularity"])[i]].add(student_and_points[0])
                            
                    #difficulty level {user:[p,o,i,n,t,s]}
                    statistics["difficulty"].setdefault(student_and_points[0], [0, 0, 0, 0])
                    y["difficulty"].setdefault(student_and_points[0], [0, 0, 0, 0])
                    for i in range(0, 4):
                        statistics["difficulty"][student_and_points[0]][i] += new_points[i]
                    
                    if len(x[student_and_points[0]]) < 4:
                        x[student_and_points[0]].append(new_points)
                    else:
                        old_points = x[student_and_points[0]][3]
                        x[student_and_points[0]][3] = [sum(i) for i in zip(old_points, new_points)]
                    print("Points updated.")
                else:
                    print("Incorrect points format.")
            else:
                print(f"No student is found for id={student_and_points[0]}.")
                
def find_student(x):
    print("Enter an id and points or 'back' to return")
    while True:
        student = input()
        if student == "back":
            break
        elif student in x:
            points = x[student][3]
            print(f"{student} points: Python={points[0]}, DSA={points[1]}; Databases={points[2]}; Flask={points[3]}")
        else:
            print(f"No student is found for id={student}.")
            
def count_statistics(stats):
    def most_and_least(stats, x):
        if x == "difficulty":
            difficulty = {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0}
            for index in range(0, 4):
                if [i for i in difficulty][index] not in stats["difficulty"]:
                    not_zero = [stats["difficulty"][i][index] for i in stats["difficulty"] if stats["difficulty"][i][index] != 0]
                    difficulty[[i for i in difficulty][index]] += sum(not_zero) / len([i for i in not_zero if i != 0])
            sorted_rating = sorted(difficulty.items(), key=lambda x: x[1], reverse=True)
        else:    
            sorted_rating = sorted(stats[x].items(), key=lambda x: x[1], reverse=True)
        
        if sorted_rating[0][1] == 0:
            most, least = "n/a", "n/a"
        elif sorted_rating[0][1] == sorted_rating[3][1]:
            most, least = [i[0] for i in sorted_rating], "n/a"
        else:
            most, least = [i[0] for i in sorted_rating][:3], sorted_rating[3][0]

        if x == "popularity":
            print(f'Most popular: {", ".join(most) if type(most) is list else most}', f'Least popular: {least}', sep="\n")
        elif x == "activity":
            print(f'Highest activity: {", ".join(most) if type(most) is list else most}', f'Lowest activity: {least}', sep="\n")
        else:
            print(f'Easiest course: {", ".join(most) if type(most) is list else most}', f'Hardest course: {least}', sep="\n")
        
    print("Type the name of a course to see details or 'back' to quit:")
    most_and_least(stats, "popularity")
    most_and_least(stats, "activity")
    most_and_least(stats, "difficulty")
    
    courses = ["Python", "DSA", "Databases", "Flask"]
    while True:
        course = input()
        if course == "back":
            break
        elif course.casefold() in str(courses).casefold():
            for i in courses:
                if course.casefold() in i.casefold():
                    course = i
            found = []
            for student in stats['difficulty']:
                if type(stats['difficulty'][student]) is not int:
                    points = stats['difficulty'][student][courses.index(course)]
                    if points != 0:
                        max_points = [600, 400, 480, 550][courses.index(course)]
                        found.append((student, points, f"    {round((points * 100)/max_points, 1)}%"))
            print(f"{courses[courses.index(course)]}\nid", "                              points", "completed")
            [print(*i) for i in sorted(found, key=lambda x: (-x[1], x[0]))]  
        else:
            print("Unknown course.")
            
def notify(students, informed):
    maxes = [("Python", 600), ("DSA", 400), ("Databases", 480), ("Flask", 550)]
    n = 0
    for i in {i:students[i] for i in students if len(students[i]) == 4}:
        if i not in {student for course in informed for student in informed[course]}:
            for ii in range(0, 4):
                mail, name, surname, points = students[i]
                if points[ii] == maxes[ii][1] and i not in informed[maxes[ii][0]]:
                    print(f"To: {mail}\nRe: Your Learning Progress\nHello, {name} {surname}! You have accomplished our {maxes[ii][0]} course!")
                    informed[maxes[ii][0]].add(i)
            n += 1
    print(f"Total {n} students have been notified.")
            
    
print("Learning Progress Tracker")
all_students = ""
statistics = {"activity": {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0},
              "popularity": {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0},
              "difficulty": {"Python": 0, "DSA": 0, "Databases": 0, "Flask": 0}}
notifed = {"Python": set(), "DSA": set(), "Databases": set(), "Flask": set()}

while True:
    user_choice = main_menu(input())
    if user_choice == "exit":
        print("Bye!")
        break
    elif user_choice == "back":
        print("Enter 'exit' to exit the program.")
    elif user_choice == "add students":
        print("Enter student credentials or 'back' to return:")
        all_students = add_students()
    elif user_choice == "list":
        print("Students:\n" + "\n".join(all_students) if len(all_students) > 0 else "No students found")
    elif user_choice == "add points": 
        statistics = add_points(all_students, statistics)
    elif user_choice == "find":
        find_student(all_students)
    elif user_choice == "statistics":
        count_statistics(statistics)
    elif user_choice == "notify":
        notify(all_students, notifed)
    else:
        continue