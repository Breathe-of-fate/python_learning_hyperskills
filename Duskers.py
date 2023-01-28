import sys
import random
import time
import os
from datetime import datetime
import datetime

locations = ['Burned Moscow', 'Dying Universe', 'Deep Space', 'Abanded Ishimura']

if len(sys.argv) > 1:
    anim_game_logo, anim_main_menu, anim_greetings, anim_hub, anim_search, anim_search_dot, anim_dep_robots, anim_explored, anim_acqured = 0, 0, 0, 0, 0, 0, 0, 0, 0
    #anim_game_logo, anim_main_menu, anim_greetings, anim_hub, anim_search, anim_search_dot, anim_dep_robots, anim_explored, anim_acqured = 0.003, 0.02, 0.02, 0.003, 0.02, 1, 0.03, 0.04, 0.04
    to_wait = int(random.choice([i for i in range(int(sys.argv[2]), int(sys.argv[3]) + 1)]))
    locations = sys.argv[4].replace(",", " ").split("/")
    random.seed(sys.argv[1])
else:
    anim_game_logo, anim_main_menu, anim_greetings, anim_hub, anim_search, anim_search_dot, anim_dep_robots, anim_explored, anim_acqured = 0, 0, 0, 0, 0, 0, 0, 0, 0
    to_wait = 0

def check_invalid_input(x, *y):
    print(*y)
    user_choice = input("Your command:\n").lower()
    while user_choice not in [i.replace("[", "").replace("]", "").lower() for i in x] + ["back"]:
        print("Invalid input\n", *y, sep="\n")
        user_choice = input("Your command:\n").lower()
    return user_choice

def animation(x, y):
    for i in x:
        print(i, end='', flush=True)
        time.sleep(y)

def animation_wait(x):
    for i in range(x):
        print(".", flush=True, end="")
        time.sleep(1)

def show_slots():
    slots = {}
    for i in ["1", "2", "3"]:
        if os.path.isfile(i + "-save_file.txt"):
            with open(i + "-save_file.txt", "r") as reading:
                from_file = reading.read().split(", ")
                upgrades = from_file[4:] if len(from_file) > 4 else ""
                to_out = []
                if upgrades != "":
                    to_out.append('ti_visible') if upgrades[0] == "True" else ""
                    to_out.append('enemy_visible') if upgrades[1] == "True" else ""
                else:
                    to_out = ""
                b = f"[{i[0]}] {from_file[0]} Titanium: {from_file[1]} Robots: {from_file[2]} Last save: {from_file[3]} Upgrades: {', '.join(to_out)}"
        else:
            b = f"[{i[0]}] empty"
        slots[i] = b
    print("   Select save slot:\n   ", "\n    ".join(slots.values()))

def load_game():
    while True:
        show_slots()
        user_choice = check_invalid_input(['1', '2', '3'])
        if user_choice != "back":
            if os.path.isfile(user_choice + "-save_file.txt"):
                with open(user_choice + "-save_file.txt", "r") as reading:
                    return reading.read().split(", ")
            else:
                print("Empty slot!\n")
        else:
            return user_choice

def check_ti(x, y):
    if x <= y:
        return True
    else:
        return False

def read_rating():
    if os.path.isfile("high_scores.txt"):
        with open("high_scores.txt", "r") as scores:
            records_in_file = ["".join(i).replace("\n", "").split(" ") for i in scores.readlines()]
            return records_in_file
    else:
        return []

ti_visible = False
enemy_visible = False
to_main = False
to_hub = False
to_exit = False
to_load = False
titanium = 0
robots = 3
user_choice = ""

while to_exit != True:

    if to_hub == False:

        ti_visible = False
        enemy_visible = False
        to_main = False
        to_exit = False
        to_load = False
        titanium = 0
        robots = 3
        user_choice = ""

        animation("""\n██████╗ ██╗   ██╗███████╗██╗  ██╗███████╗██████╗ ███████╗
██╔══██╗██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝
██║  ██║██║   ██║███████╗█████╔╝ █████╗  ██████╔╝███████╗
██║  ██║██║   ██║╚════██║██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
██████╔╝╚██████╔╝███████║██║  ██╗███████╗██║  ██║███████║
╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝\n\n""", anim_game_logo)

        main_menu = ["[New]  Game", "[Load] Game", "[High] Scores", "[Help]", "[Exit]"]
        dialog_in_main = ["[Yes]", "[No]", "[Menu]"]

        animation("\n".join(main_menu) + "\n", anim_main_menu)

        user_choice = check_invalid_input(["[New]", "[Load]", "[High]", "[Help]", "[Exit]"])

    if user_choice == "new" or to_hub == True:

        if to_hub == False:
            user_name = input('\nEnter your name:\n')
            animation(f"\nGreetings, commander, {user_name}!\n", anim_greetings)
            user_choice = check_invalid_input(dialog_in_main, "Are you ready to begin?\n[Yes] [No] Return to Main[Menu]\n")
            while user_choice == "no":
                user_choice = check_invalid_input(dialog_in_main, "\nHow about now.\nAre you ready to begin?\n[Yes] [No] Return to Main[Menu]\n")

        if user_choice == "yes" or to_hub == True: #hub

            while True:

                if to_main == True:
                    break
                if to_exit == True:
                    break

                animation("\n".join([f"║{'═' * 80}║\n",
                                f" {'█' * 5} " * robots, ((" █   █ " * robots + "\n") * 3)[:-1], f" {'█' * 5} " * robots, \
                                f"\n  Titanium: {titanium}", \
                                f"║{'═' * 80}║", \
                                f"║{' ' * 18}[Ex]plore{' ' * 26}[Up]grade{' ' * 18}║", \
                                f"║{' ' * 18}[Save]{' ' * 29}[M]enu{' ' * 21}║", \
                                f"║{'═' * 80}║\n"]), anim_hub)

                user_choice = check_invalid_input(["[Ex]", "[Save]", "[Up]", "[M]"])
                if user_choice == "m":
                    print(f"""{' ' * 29}║{'═' * 24}║\n{' ' * 29}║{' ' * 10}MENU{' ' * 10}║\n{' ' * 29}║{' ' * 24}║
                             ║[Back] to game          ║
                             ║ Return to [Main] Menu  ║
                             ║[Save] and exit         ║
                             ║[Exit] game             ║
                             ║{'═' * 24}║""")
                    user_choice = check_invalid_input(["[Back]", "[Main]", "[Save]", "[Exit]"])
                    if user_choice == "back":
                        continue
                    elif user_choice == "main":
                        break
                    elif user_choice == "save":
                        continue
                    elif user_choice in ("exit", "save"):
                        print("\nThanks for playing, bye!")
                        to_exit = True

                elif user_choice == "back":
                    to_main = True

                elif user_choice == "ex":
                    loc_amount = random.randint(1, 9)
                    numbers = [str(i) for i in range(1, loc_amount + 1)]
                    n = 1
                    ti = []

                    while user_choice not in "".join([str(i) for i in range(1, len(ti) + 1)]) + "back":

                        if len(ti) == loc_amount:
                            user_choice = check_invalid_input("".join(numbers), "\nNothing more in sight.\n       [Back]\n")
                            continue

                        ti.append([f"[{n}]", random.choice(locations), random.randint(10, 100), random.random()])
                        animation("Searching", anim_search), animation_wait(to_wait), print()

                        for i in ti:
                            print(*i[:2], f"Titanium: {i[2]}" if ti_visible else "", f"Encounter rate: {round(i[3] * 100)}%" if enemy_visible else "")

                        user_choice = check_invalid_input("[s]" + "".join([str(i) for i in range(1, len(ti) + 1)]), "\n[S] to continue searching\n")
                        if user_choice == ["s"]:
                            n += 1
                            continue
                        elif user_choice in ["".join([str(i) for i in range(1, len(ti) + 1)])]:
                            continue
                        elif user_choice == "back":
                            continue

                    if user_choice == "back":
                        continue

                    elif user_choice in "".join([str(i) for i in range(1, len(ti) + 1)]):
                        animation("Deploying robots", anim_dep_robots), animation_wait(to_wait), print()
                        if random.random() < ti[int(user_choice) - 1][3]:
                            robots -= 1
                            if robots == 0:
                                animation("Enemy encounter!!!", anim_dep_robots), print()
                                animation("Mission aborted, the last robot lost...", anim_dep_robots), print()
                                print(f"""        ║{'═' * 30}║\n        ║          GAME OVER!          ║\n        ║{'═' * 30}║\n""")
                                readed_rating = read_rating()
                                readed_rating.append([user_name, str(titanium), datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S-%f")])
                                readed_rating.sort(key=lambda x: (-int(x[1]), datetime.datetime.strptime(f'{x[2]}', '%Y-%m-%d-%H:%M:%S-%f')))
                                with open("high_scores.txt", "w") as scores:
                                    [scores.write(" ".join(i) + "\n") for i in readed_rating[:10]]
                                to_hub = False
                                break
                            else:
                                animation("\nEnemy encounter", anim_dep_robots), animation_wait(to_wait)
                                animation(f"\n{ti[int(user_choice) - 1][1]} explored successfully, 1 robot lost.", anim_explored)
                        else:
                            animation(f"\n{ti[int(user_choice) - 1][1]} explored successfully, with no damage taken.", anim_explored)
                        animation(f"\nAcquired {ti[int(user_choice) - 1][2]} lumps of tianium.", anim_acqured), print("\n")
                        titanium += ti[int(user_choice) - 1][2]

                elif user_choice == "save":
                    show_slots()
                    user_choice = check_invalid_input(["1", "2", "3"])
                    with open(user_choice + "-save_file" + ".txt", "w") as save_slot:
                        save_slot.write(f"{user_name}, {titanium}, {robots}, {time.strftime('%Y-%m-%d %H:%M', time.localtime())}, {ti_visible}, {enemy_visible}")
                    print(f"""{' ' * 8}║{'═' * 30}║\n        ║    GAME SAVED SUCCESSFULLY   ║\n        ║{'═' * 30}║""")

                elif user_choice == "up":
                    print(f"""{' ' * 25}║{'═' * 30}║\n{' ' * 25}║         UPGRADE STORE        ║\n{' ' * 25}║{' ' * 24}Price ║
                         ║[1] Titanium Scan         250 ║
                         ║[2] Enemy Encounter Scan  500 ║
                         ║[3] New Robot            1000 ║
                         ║{' ' * 30}║
                         ║[Back]                        ║
                         ║{'═' * 30}║\n""")
                    while True:
                        user_choice = check_invalid_input("123")
                        if user_choice == "back":
                            break
                        elif user_choice in ("123"):
                            if user_choice == "1":
                                if check_ti(250, titanium):
                                    print("Purchase successful. You can now see how much titanium you can get from each found location.")
                                    ti_visible = True
                                    titanium -= 250
                                    break
                                else:
                                    print("Not enough titanium to buy.")
                            elif user_choice == "2":
                                if check_ti(500, titanium):
                                    print("Purchase successful. You will now see how likely you will encounter an enemy at each found location.")
                                    enemy_visible = True
                                    titanium -= 500
                                    break
                                else:
                                    print("Not enough titanium to buy.")
                            elif user_choice == "3":
                                if check_ti(1000, titanium):
                                    print("Purchase successful. You now have an additional robot")
                                    robots += 1
                                    titanium -= 1000
                                    break
                                else:
                                    print("Not enough titanium to buy.")

        elif user_choice == "menu":
            continue

    elif user_choice == "load":
        to_load = load_game()
        if to_load != "back":
            user_name = to_load[0]
            titanium = int(to_load[1])
            robots = int(to_load[2])
            ti_visible = True if to_load[4] == 'True' else False
            enemy_visible = True if to_load[5] == 'True' else False
            print(f"{' ' * 8}║{'═' * 29}║\n{' ' * 8}║   GAME LOADED SUCCESSFULLY  ║\n{' ' * 8}║{'═' * 29}║")
            print(f"Welcome back, commander {user_name}!")
            to_hub = True
        else:
            user_choice = to_load
            to_main = True

    elif user_choice == "high":
        readed_rating = read_rating() # to show rating
        if len(readed_rating) != 0:
            print("\n      HIGH SCORES\n")
            for i in range(1, len(readed_rating) + 1):
                print(f"({i}) {readed_rating[i - 1][0]} {readed_rating[i - 1][1]}")
            print("\n        [Back]")
        else:
            print("\nNo scores to display.\n\t[Back]")
        user_choice = check_invalid_input(["[Back]"])
        if user_choice == "back":
            continue

    elif user_choice == "exit":
        print("\nThanks for playing, bye!")
        break

    elif user_choice == "help":
        print("\nHello! This game was made for JetBrains Academy.\nI lost for this shit some monthes so enjoy it. Please...\n\n  [Back]")
        user_choice = check_invalid_input(["[Back]"])
        if user_choice == "back":
            continue