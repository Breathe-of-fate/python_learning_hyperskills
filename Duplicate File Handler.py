import sys
import os
import hashlib

def wrong_input(x, y):
    user_choice = input(x)
    while user_choice not in y:
        user_choice = input("\nWrong option\n\n")
    return user_choice

def file_size(a, b):
    return os.path.getsize(os.path.join(a, b))

if len(sys.argv) == 1:
    print("Directory is not specified")
else:
    file_format = input("Enter file format:\n")
    print("\nSize sorting options:", "1. Descending", "2. Ascending\n", sep="\n")
    
    sorting_option = wrong_input("Enter a sorting option:\n", ["1", "2"])

    output = {}
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            if name.endswith(file_format):
                output.setdefault(file_size(root, name), []) 
                output[file_size(root, name)] += [os.path.join(root, name)]
    
    for i in sorted(output, reverse=True if sorting_option == "1" else False):
        print(f"\n{i} bytes", *output[i], sep="\n")
    
    if wrong_input("\nCheck for duplicates?\n", ("yes", "no")) == "yes":
        hashs = {}
        for i in output:
            for ii in output[i]:
                with open(ii, "rb") as item_to_hash:
                    hashing = hashlib.md5()
                    hashing.update(item_to_hash.read())
                    hashs.setdefault(i, {})
                    hashs[i].setdefault(hashing.hexdigest(), [])
                    hashs[i][hashing.hexdigest()] += [ii]

        for size, hash_n_list in hashs.items():
            for hash in list(hash_n_list.keys()):
                if len(hash_n_list[hash]) == 1:
                    del hash_n_list[hash]
        
        n = 1
        file_list = []               
        for size, hash_n_list in sorted(hashs.items(), reverse=True if sorting_option == "1" else False):
            print(f"\n{size} bytes")
            for hash, paths in hash_n_list.items():
                print(f"Hash: {hash}")
                for path in paths:
                    print(f"{n}. {path}")
                    file_list.append((size, path))
                    n += 1
        
        if wrong_input("\nDelete files?\n", ("yes", "no")) == "yes":
            user_choice = input("\nEnter file numbers to delete:\n").split()
            while len(user_choice) == 0 or all([True if i in [str(i) for i in range(1, len(file_list)  + 1)] else False for i in user_choice]) != True:
                user_choice = input("\nWrong option\n\nEnter file numbers to delete:\n").split()
            sum_to_show = []
            for path in user_choice:
                os.remove(file_list[int(path) - 1][1])
                sum_to_show.append(file_list[int(path) - 1][0])
            print("\nTotal freed up space:", sum(sum_to_show))