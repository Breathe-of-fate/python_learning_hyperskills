limit = int(input())

applicants = [i.split() for i in open("applicants.txt").read().splitlines()]

faculty = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
lessons_rank_indexes = [(3, 2), (3, 3), (5, 4), (4, 4), (2, 4)]
lessons_rank_dict = {faculty[i]: lessons_rank_indexes[i] for i in range(len(faculty))}

app_for_deps = {i: [] for i in faculty}

for i in range(7, 10):
    for ii, j in lessons_rank_dict.items():
        n_1, n_2 = j
        applicants.sort(key=lambda x: (-max((float(x[n_1]) + float(x[n_2])) / 2, float(x[6])), x[0], x[1]))
        for iii in applicants.copy():
            if iii[i] == ii and len(app_for_deps[iii[i]]) < limit:
                result = iii[0], iii[1],\
                         max((float(iii[n_1]) + float(iii[n_2])) / 2, float(iii[6]))
                app_for_deps[iii[i]].append(result)
                applicants.remove(iii)

for applicants in app_for_deps.values():
    applicants.sort(key=lambda x: (-float(x[2]), x[0], x[1]))

for department, applicants in app_for_deps.items():
    with open(department + ".txt", "w") as department_file:
        for iii in applicants:
            print(*iii, file=department_file)