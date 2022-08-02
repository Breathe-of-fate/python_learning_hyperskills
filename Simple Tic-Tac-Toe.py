start_input = "_________"
groups_ammount = int(len(start_input) // 3)
char_by_char_list = [char for full_list in start_input for char in full_list]
char_by_groups_list = [char_by_char_list[ind:ind + groups_ammount] for ind in range(0, len(char_by_char_list), groups_ammount)]
final_result = ""
user_switch = 1

def print_matrix():
    print("---------")
    for inner_list in char_by_groups_list:
        print("|", * inner_list, "|")
    print("---------")

print_matrix()

while True:

    win_lines = [[inner_list[0] for inner_list in char_by_groups_list], [inner_list[1] for inner_list in char_by_groups_list], [inner_list[2] for inner_list in char_by_groups_list], * [inner_list for inner_list in char_by_groups_list], [char_by_groups_list[ind][ind] for ind in range(0, groups_ammount)], [char_by_groups_list[ind][(groups_ammount - 1) - ind] for ind in range(0, groups_ammount)]]

    for inner_list in win_lines:
        if len([*[win_lines_inner for win_lines_inner in win_lines if win_lines_inner.count("X") == 3]]) == 1:
            final_result = "X wins"
        elif len([*[win_lines_inner for win_lines_inner in win_lines if win_lines_inner.count("O") == 3]]) == 1:
            final_result = "O wins"
        elif [y for x in char_by_groups_list for y in x].count("_") == 0:
            final_result = "Draw"
    
    if final_result != "":
        break
    else:
        move_input_check = [char for char in input().replace(" ", "")]

        if len([*[char for char in move_input_check if char.isalpha()]]) > 0:
            print("You should enter numbers!")
            continue
        else:
            move_input_check = [int(char) for char in move_input_check]
            if len([*[char for char in move_input_check if char < 1], *[char for char in move_input_check if char > groups_ammount]]) > 0:
                print("Coordinates should be from 1 to 3!")
                continue
            else:
                ind1, ind2 = int(move_input_check[0]) - 1, int(move_input_check[1]) - 1

                if char_by_groups_list[ind1][ind2] != "_":
                    print("This cell is occupied! Choose another one!")
                    continue
                else:
                    if user_switch % 2 > 0:
                        char_by_groups_list[ind1][ind2] = "X"
                        print_matrix()
                        user_switch += 1
                        continue
                    else:
                        char_by_groups_list[ind1][ind2] = "O"
                        print_matrix()
                        user_switch += 1
                        continue                        
                    
print(final_result)