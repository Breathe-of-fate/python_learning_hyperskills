import gzip

list_to_print = []
n = 1

while n < 4:
    seq_list = gzip.open(input()).read().decode('utf8').splitlines()[1::4]
    seq_list_len = [len(seq_list[i]) for i in range(0, len(seq_list))]
    GC_content = [((seq_list[i].count("G") + seq_list[i].count("C")) / len(seq_list[i])) * 100 for i in range(0, len(seq_list))]
    GC_content_av = [round(sum(GC_content)/len(GC_content), 2)]
    N_content = [round(seq_list[i].count("N")/len(seq_list[i])*100, 2) for i in range(0, len(seq_list))]
    list_to_print.append([len(seq_list), round(sum(seq_list_len) / len(seq_list_len)), len(seq_list) - len(set(seq_list)), len([i for i in N_content if i > 0]), *GC_content_av, round(sum(N_content)/len(N_content), 2)])
    n += 1

best = [[i[3], i[5]] for i in list_to_print].index(min([[i[3], i[5]] for i in list_to_print]))

print(f"\nReads in the file = {list_to_print[best][0]}")
print(f"Reads sequence average length = {list_to_print[best][1]}")
print(f"\nRepeats = {list_to_print[best][2]}")
print(f"Reads with Ns = {list_to_print[best][3]}")
print(f"\nGC content average = {list_to_print[best][4]}%")
print(f"\nNs per read sequence = {list_to_print[best][5]}%")

