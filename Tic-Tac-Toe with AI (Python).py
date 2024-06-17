import random

def field_maker(field=""):
    last = "---------"
    all_lines = [list("|       |") for i in range(3)] if not field else field
    print(last)
    [print("".join(i)) for i in all_lines]
    print(last)
    return all_lines

def user_move(matrix, x_or_o):
    while True:
        try:
            row, column = input("Enter the coordinates: ").split()
        except:
            print("You should enter numbers!")
            continue
        if not row.isdigit() or not column.isdigit():
            print("You should enter numbers!")
        elif row not in ["1", "2", "3"] or column not in ["1", "2", "3"]:
            print("Coordinates should be from 1 to 3!")
        else:
            if matrix[int(row) - 1][int(column)*2] == " ":
                matrix[int(row) - 1][int(column)*2] = x_or_o
                field_maker(matrix)
                return matrix
            else:
                print("This cell is occupied! Choose another one!")
                
def ai_move(matrix, x_or_o, level):
    
    def find_emptys():
        empty = []
        for row_num, row in enumerate(matrix):
            for sign_num, sign in enumerate(row):
                if sign_num in [2, 4, 6] and sign == " ":
                    empty.append(f"{row_num}, {sign_num}")
        return empty
    
    def win_or_block(x_or_o):
        coordinates = []
        for row_num, row in enumerate(matrix):
            for sign_num, sign in enumerate(row):
                if str(row).count(x_or_o) == 2 and sign_num in [2, 4, 6] and sign == " ":
                    coordinates.append(f"{row_num}, {sign_num}")

        ver = [[i[ii] for i in matrix] for ii in [2, 4, 6]]
        for ind, el in enumerate(ver):
            for ind2, el2 in enumerate(el):
                if str(el).count(x_or_o) == 2 and el2 == " ":
                    if ind == 0:
                        coordinates.append(f"{ind2}, 2")
                    elif ind == 1:
                        coordinates.append(f"{ind2}, 4")   
                    elif ind == 2:
                        coordinates.append(f"{ind2}, 6")  

        dig = [[matrix[0][2], matrix[1][4], matrix[2][6]], [matrix[0][6], matrix[1][4], matrix[2][2]]]
        for ind, el in enumerate(dig):
            for ind2, el2 in enumerate(el):
                if str(el).count(x_or_o) == 2 and el2 == " ":
                    if ind == 0:
                        ind2 = ind2 * 2 + 2
                        if ind2 == 2:
                            to_add = "0, 2"
                        elif ind2 == 4:
                            to_add = "1, 4"
                        else:
                            to_add = "2, 6"
                    else:
                        ind2 = 6 - ind2 * 2
                        if ind2 == 2:
                            to_add = "2, 2"
                        elif ind2 == 4:
                            to_add = "1, 4"
                        else:
                            to_add = "0, 6"                
                    coordinates.append(to_add)
        return coordinates
     
    if level == "easy":
        all_coordinates = find_emptys()
        print('Making move level "easy"')    
    elif level == "medium":
        win_coordinates = win_or_block(x_or_o)
        win_blocks = win_or_block("X" if x_or_o == "O" else "O")
        all_emptys = find_emptys()
        if win_coordinates:
            all_coordinates = win_coordinates
        elif win_blocks:
            all_coordinates = win_blocks  
        else:
            all_coordinates = all_emptys
        print('Making move level "medium"')
    elif level == "hard":
        if matrix[1][4] == " ":
            all_coordinates = ["1, 4"]
        else:
            win_coordinates = win_or_block(x_or_o)
            win_blocks = win_or_block("X" if x_or_o == "O" else "O")
            all_emptys = find_emptys()
            if win_coordinates:
                all_coordinates = win_coordinates
            elif win_blocks:
                all_coordinates = win_blocks  
            else:
                all_coordinates = all_emptys
        print('Making move level "hard"')
            
    random.seed()
    row, column = random.choice(all_coordinates).split(", ")
    matrix[int(row)][int(column)] = x_or_o
    field_maker(matrix)
    return matrix

def move_maker(all_lines, player1, player2):
    while True:
        x, o = str(all_lines).count("X"), str(all_lines).count("O")
        move_sign = "X" if x <= o or x == 0 else "O"
        if move_sign == "X":
            if player1 == "user":
                return user_move(all_lines, move_sign)
            else:
                return ai_move(all_lines, move_sign, player1)
        else:
            if player2 == "user":
                return user_move(all_lines, move_sign)
            else:
                return ai_move(all_lines, move_sign, player2)
        
def win_checker(matrix):

    rows = [[matrix[i][ii] for ii in [2, 4, 6]] for i in range(3)]
    columns = [[matrix[ii][i] for ii in range(3)] for i in [2, 4, 6]]
    digs = [[matrix[0][2], matrix[1][4], matrix[2][6]], [matrix[0][6], matrix[1][4], matrix[2][2]]]
    wins_coodinates = rows + columns + digs
    
    for i in wins_coodinates:
        if str(i).count("X") == 3:
            return "X wins\n"
        elif str(i).count("O") == 3:
            return "O wins\n"

    spaces = []
    for i in wins_coodinates:
        if " " in i:
            spaces.append(" ")
    if len(spaces) == 0:
        return "Draw\n"
            
def input_checker():
    while True:
        user_input = input("Input command: ")
        if user_input == "exit":
            exit()
        if len(user_input.split()) == 3:
            command, player1, player2 = user_input.split()
            menus = ["user", "easy", "medium", "hard"]
            if command == "start" and player1 in menus and player2 in menus:
                return f"{player1}, {player2}"
            else:
                print("Bad parameters!")
                continue
        else:
            print("Bad parameters!")
            continue

while True:
    settings = input_checker()
    play1, play2 = settings.split(", ")
    field = field_maker()
    winer = ""
    while not winer:
        field = move_maker(field, play1, play2)
        winer = win_checker(field) if play1 and play2 not in "hard" else "Draw\n"
    print(winer)