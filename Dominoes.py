def dominos_start():
    """This function creates a domino set, divides all dominoes to 3 parts and chooses a first player to start"""
    import random
    
    while True:
        dominos_set = [[i, n] for i in range(0, 7) for n in range(0, 7) if i >= n]
        random.shuffle(dominos_set)
        stock = dominos_set[:14]
        computer = dominos_set[14:21]
        player = dominos_set[21:]

        doubles = [[i, n] for i in range(0, 7) for n in range(0, 7) if i == n]
        doubles.reverse()

        for i in doubles:
            if i in computer:
                who_first = [i, "It's your turn to make a move. Enter your command."]
                computer = [i for i in computer if i != who_first[0]]
                break
            elif i in player:
                who_first = [i, "Computer is about to make a move. Press Enter to continue..."]
                player = [i for i in player if i != who_first[0]]
                break
            else:
                continue
        return stock, computer, [who_first[0]], [str(player.index(i) + 1) + ":" + str(i) for i in player], who_first[1]

def game_loop():
    import random
    
    all_lists = list(dominos_start()[:])

    while True:

        print("=" * 70)
        print(f"Stock size: {len(all_lists[0])}")
        print(f"Computer pieces: {len(all_lists[1])}\n")
        if len(all_lists[2]) <= 6:
            print(* all_lists[2], sep="")
        else:
            print(* all_lists[2][:3], "...", * all_lists[2][-3:], sep="")
        print("", "Your pieces:", * all_lists[3], sep="\n")
        if len(all_lists[3]) == 0:
            return "\nStatus: The game is over. You won!"
        if len(all_lists[1]) == 0:
            return "\nStatus: The game is over. The computer won!"
        if all_lists[2].count(all_lists[2][0][0]) == 8 and (all_lists[2][0][0] and all_lists[2][len(all_lists[2]) - 1][1]):
            return "\nStatus: The game is over. It's a draw!"
        print("\nStatus: " + all_lists[4])
        all_possible_compinations = [* range(-len(all_lists[3]), 0), * range(1, len(all_lists[3]) + 1)]

        def check_input():
            user_choice = input()
            while True:
                if user_choice == "":
                    return user_choice
                elif any([i.isalpha() for i in user_choice]) or (user_choice != "0" and user_choice not in str(all_possible_compinations)):
                    print("Invalid input. Please try again.")
                    user_choice = input()
                    continue
                else:
                    if "-" in user_choice and str(all_lists[2][0][0]) in all_lists[3][int(user_choice[1:]) - 1][2:]:
                        return user_choice
                    elif str(all_lists[2][len(all_lists[2]) - 1][1]) in all_lists[3][int(user_choice) - 1][2:]:
                        return user_choice
                    elif user_choice == "0":
                        return user_choice
                    else:
                        print("Illegal move. Please try again.")
                        user_choice = input()
                        continue      
                    
        user_choice = str(check_input())

        if "Computer" in all_lists[4]:
            all_lists[4] = "It's your turn to make a move. Enter your command."
        elif "It's" in all_lists[4]:
            all_lists[4] = "Computer is about to make a move. Press Enter to continue..."

        if user_choice == "": #computer part
            
            while True:

                def computer_ai():

                    all_numbers = [[i, [y for x in all_lists[1] for y in x].count(i) + [y for x in all_lists[2] for y in x].count(i)] for i in range(0, 7)] # совмещаем два списка и считаем для каждой цифры очки (1-ая цифра - какая, 2: сколько встречается)
                    dominos_scores = [iii[1] for i in all_lists[1] for ii in i for iii in all_numbers if ii == iii[0]] # присваиваем очки к домино (очки за первую цифру, очки за вторую)
                    scores_list = [sum(dominos_scores[i:i + 2]) for i in range(0, len(dominos_scores), 2)] # считаем сумму очков, получаем список сумм очков в порядке доминошек [1, 2, 3]
                    scores_indicies_list = sorted(list(enumerate(scores_list, 1)), key=lambda tup: tup[1], reverse=True) # список с индексами и значениями
                    indicies_list = [i[0] - 1 for i in scores_indicies_list]

                    possible_list = []
                    for i in range(0, len(all_lists[1])):
                        if all_lists[2][0][0] in all_lists[1][indicies_list[i]]:
                            possible_list.append(-indicies_list[i])
                        elif all_lists[2][len(all_lists[2]) - 1][1] in all_lists[1][indicies_list[i]]:
                            possible_list.append(indicies_list[i])
                    
                    if len(possible_list) > 0:
                        return possible_list[0]
                    else:
                        return ""

                user_choice = computer_ai()

                if user_choice == "":
                    if len(all_lists[0]) > 0:
                        domino_to_operate = random.choice(all_lists[0])
                        all_lists[1].append(domino_to_operate)
                        all_lists[0].remove(domino_to_operate)
                        break
                    elif len(all_lists[0]) == 0:
                        break                    
                elif user_choice < 0:
                    user_choice = str(user_choice)
                    if all_lists[2][0][0] != all_lists[1][int(user_choice[1:])][1]:
                        all_lists[2].insert(0, all_lists[1][int(user_choice[1:])][::-1])
                    else:
                        all_lists[2].insert(0, all_lists[1][int(user_choice[1:])])
                    all_lists[1].remove(all_lists[1][int(user_choice[1:])])
                    break
                elif user_choice >= 0:
                    if all_lists[2][len(all_lists[2]) - 1][1] != all_lists[1][user_choice][0]:
                        all_lists[2].append(all_lists[1][user_choice][::-1])
                    else:
                        all_lists[2].append(all_lists[1][user_choice])
                    all_lists[1].remove(all_lists[1][user_choice])
                    break
                
        elif "-" in user_choice:
            if all_lists[2][0][0] != int(all_lists[3][int(user_choice[1:]) - 1][6]):
                all_lists[2].insert(0, [int(i) for i in all_lists[3][int(user_choice[1:]) - 1][3:7] if i.isnumeric()][::-1])
            else:
                all_lists[2].insert(0, [int(i) for i in all_lists[3][int(user_choice[1:]) - 1][3:7] if i.isnumeric()])
            
            all_lists[3].remove(all_lists[3][int(user_choice[1]) - 1])
            all_lists[3] = [str(all_lists[3].index(i) + 1) + ":" + str(i[2:]) for i in all_lists[3]]            
        
        elif int(user_choice) == 0:
            if len(all_lists[0]) > 0:
                domino_to_operate = random.choice(all_lists[0])
                all_lists[3].append(domino_to_operate)
                all_lists[3][len(all_lists[3]) - 1] = str(len(all_lists[3])) + ":" + str(all_lists[3][len(all_lists[3]) - 1])
                all_lists[0].remove(domino_to_operate)

        elif int(user_choice) > 0:
            if all_lists[2][len(all_lists[2]) - 1][1] != int(all_lists[3][int(user_choice) - 1][3]):
                all_lists[2].append([int(i) for i in all_lists[3][int(user_choice) - 1][3:7] if i.isnumeric()][::-1])
            else:
                all_lists[2].append([int(i) for i in all_lists[3][int(user_choice) - 1][3:7] if i.isnumeric()])
            
            all_lists[3].remove(all_lists[3][int(user_choice) - 1])
            all_lists[3] = [str(all_lists[3].index(i) + 1) + ":" + str(i[2:]) for i in all_lists[3]]

print(game_loop())