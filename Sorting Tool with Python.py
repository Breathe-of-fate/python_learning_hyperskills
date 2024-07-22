import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sortingType', nargs="?", default="natural")
parser.add_argument('-dataType', nargs="?", default="word")
parser.add_argument('-inputFile', nargs="?")
parser.add_argument('-outputFile', nargs="?")
args, unknown = parser.parse_known_args()

def output(elements, by_what):
    amount = len(elements)
    if by_what == "byCount": 
        stats = dict()
        for i in elements:
            frequency = elements.count(i)
            percent = int((100 * frequency) / amount)        
            stats.setdefault(i, [frequency, percent])
        return dict(sorted(stats.items(), key=lambda x: (x[1][0], x[0])))
    elif by_what == "natural":
        return [amount, sorted(elements)]   

if not args.sortingType and args.dataType:
    print("No sorting type defined!")
    exit()
elif args.sortingType and not args.dataType:
    print("No data type defined!")
    exit()
elif unknown:
    [print(f'"{i}" is not a valid parameter. It will be skipped.') for i in unknown]
        
all_data = ""

if args.inputFile:
    with open(args.inputFile, "r") as file:
        for i in file.readlines():
            all_data += i + "!"
else:
    while True:
        try:
            all_data += input() + "!"
        except EOFError:
            break
        
if args.outputFile:
    file = open(args.outputFile, "w+")
    
divided_data = all_data.split("!")
divided_elements = [i.split() for i in divided_data]
only_integers = []
if args.dataType == "long":
    for i in divided_elements.copy():
        for ii in i:
            if ii[0] != "-" and not ii.isnumeric():
                print(f'"{ii}" is not a long. It will be skipped.')
            else:
                only_integers.append(int(ii))
    divided_elements = only_integers
max_value = ""

if args.sortingType == "natural":
    
    if args.dataType == "long":
        amount, data = output(divided_elements, "natural")
        print(f"Total numbers: {amount}.\nSorted data:", *sorted(data), file=None if not args.outputFile else file)
    
    elif args.dataType == "line":
        divided_elements = [i for i in divided_data if len(i) > 0]
        amount, data = output(divided_elements, "natural")
        print(f"Total lines: {amount}.\nSorted data:", *sorted(data), sep="\n", file=None if not args.outputFile else file)
    
    elif args.dataType == "word":
        divided_elements = [ii for i in divided_elements for ii in i]
        amount, data = output(divided_elements, "natural")
        print(f"Total words: {amount}.\nSorted data:", *sorted(data), file=None if not args.outputFile else file)

elif args.sortingType == "byCount":
    
    if args.dataType == "long":
        print(f"Total numbers: {len(divided_elements)}.", file=None if not args.outputFile else file)
        for i, ii in output(divided_elements, "byCount").items():
            print(f"{i}: {ii[0]} time(s), {ii[1]}%", file=None if not args.outputFile else file)
    
    elif args.dataType == "line":
        divided_elements = [i for i in divided_data if len(i) > 0]
        print(f"Total lines: {len(divided_elements)}.", file=None if not args.outputFile else file)
        for i, ii in output(divided_elements, "byCount").items():
            print(f"{i}: {ii[0]} time(s), {ii[1]}%", file=None if not args.outputFile else file)
    
    elif args.dataType == "word":
        divided_elements = [ii for i in divided_elements for ii in i]
        print(f"Total words: {len(divided_elements)}.", file=None if not args.outputFile else file)
        for i, ii in output(divided_elements, "byCount").items():
            print(f"{i}: {ii[0]} time(s), {ii[1]}%", file=None if not args.outputFile else file)
            
if args.outputFile: file.close()