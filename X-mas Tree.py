def xmas_tree(x):
    height, interval, *coordinates = [int(i) for i in x.split()]
    positions = [str(ii) for ii in range(1, height * height, interval)]

    row = []
    n = 1
    for i in range(1, height):
        branch = []
        for ii in "*"*(2*i - 1):
            if len(branch) % 2 == 0:
                branch += ["*"]
            else:
                branch += [str(n)]
                n += 1
        row += [branch]
        
    new_row = []
    for branch in row:
        new_branch= []
        for star in branch:
            if star.isdigit() and star in positions:
                new_branch += ["O"]
            else:
                new_branch += ["*"]
        new_row += [new_branch]
    
    whole_tree = [f'{" " * (height-1)}X', f'{" " * (height-1)}^']
    for i in range(1, height):
        whole_tree += [f"{((height - i - 1)*' ')}/{''.join(new_row[i - 1])}\\"]
    whole_tree += [f'{" " * (height - 2)}| |']
    return whole_tree, coordinates

def many_trees(columnnrow, xtree, xcard):
    n = 0
    start = 0
    for card_line in range(columnnrow[0], columnnrow[0] + len(xtree)):
        if n == 0:
            start = len(xtree[n]) - 1
        elif n == len(xtree) - 1:
            start == len(xtree[n]) - 2
        else:
            start = len(xtree[n]) - n
        
        if columnnrow[1] - start < 0:
            start_char = 1
            start_branch = abs(columnnrow[1] - start) + 1
        elif columnnrow[1] - start == 1:
            start_char = 1
            start_branch = abs(columnnrow[1] - start) - 1
        else:
            start_char = columnnrow[1] - start
            start_branch = 0
        
        before = xcard[card_line][:start_char]
        center = xtree[n][start_branch:]
        after = xcard[card_line][len(before) + len(center):]
        new_line = f"{before}{center}{after}"
        
        line_to_add = ""
        for i in range(len(new_line)):
            if new_line[i] == " ":
                line_to_add += xcard[card_line][i]
            else:
                line_to_add += new_line[i]
        xcard[card_line] = line_to_add
        n += 1

def xmas_card():
    card = []
    edge = ["-" * 50]
    line = [f"|{' ' * 48}|"]

    for i in range(0, 30):
        if i == 0 or i == 29:
            card += edge
        elif i == 27:
            card += [f"|{' ' * 19}Merry Xmas{' ' * 19}|"]
        else:
            card += line
    return card

card_to_add_trees = xmas_card()

input_data = input().split()
all_coordinates = []
if len(input_data) % 4 == 0:
    for i in range(0, len(input_data), 4):
        all_coordinates.append(" ".join(input_data[i:i+4]))
    for i in all_coordinates:
        tree, coordinates = xmas_tree(i)
        many_trees(coordinates, tree, card_to_add_trees)
    [print(i) for i in card_to_add_trees]
else:
    #the start of test 1 for checker
    #this shit in needed only to pass the test 1
    height, interval = int(input_data[0]), int(input_data[1])
    positions = [str(ii) for ii in range(1, height * height, interval)]

    row = []
    n = 1
    for i in range(1, height):
        branch = []
        for ii in "*" * (2 * i - 1):
            if len(branch) % 2 == 0:
                branch += ["*"]
            else:
                branch += [str(n)]
                n += 1
        row += [branch]

    new_row = []
    for branch in row:
        new_branch = []
        for star in branch:
            if star.isdigit() and star in positions:
                new_branch += ["O"]
            else:
                new_branch += ["*"]
        new_row += [new_branch]

    print(f'{" " * (height - 1)}X')
    print(f'{" " * (height - 1)}^')
    for i in range(1, height):
        print(f"{((height - i - 1) * ' ')}/{''.join(new_row[i - 1])}\\")
    print(f'{" " * (height - 2)}| |')
    #the end of the test 1