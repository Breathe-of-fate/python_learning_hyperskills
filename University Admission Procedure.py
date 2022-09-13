with open("applicants.txt") as open_file:
    applicants = [i.split() for i in open_file.read().splitlines()]

by_deps = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}
ranks_for_deps = {"Biotech": (3, 2), "Chemistry": (3, 3), "Engineering": (5, 4), "Mathematics": (4, 4), "Physics": (2, 4)}

limit = int(input())

for indicies in range(7, 10):

    for dep, ranks in ranks_for_deps.items():
        rank1, rank2 = ranks

        for student in sorted(applicants, key=lambda x: (-max((float(x[rank1]) + float(x[rank2])) / 2, float(x[6])), x[0], x[1])): # 1st sort, by mean, exam, name, surname
            if student[indicies] == dep and len(by_deps[student[indicies]]) < limit:
                by_deps[student[indicies]].append([student[0], student[1], max((float(student[rank1]) + float(student[rank2])) / 2, float(student[6]))])
                applicants.remove(student)

for dep, students in by_deps.items():
    with open(dep + ".txt", "w") as for_file:
        for student in sorted(students, key=lambda x: (-float(x[2]), x[0], x[1])): # 2nd sort, by mean, name and surname
            print(*student, file=for_file)
