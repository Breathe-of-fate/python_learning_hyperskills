import os, time, threading

def main_menu():
    menu = ["Menu:", "1. Add road", "2. Delete road", "3. Open system", "0. Quit"]
    print(*menu, sep="\n")

def add_road():
    new_road = input("Input road name: ")
    if len(all_roads) >= roads_num:
        print("Queue is full")
    else:
        timers("add", to_add=new_road)
        print(f"{new_road} Added!")   

def delete_road():
    if len(all_roads) > 0:
        first_road = list(all_roads)[0]
        timers("delete", first_road)
        print(f"{first_road} deleted!")
    else:
        print("Queue is empty")

def timers(mode, to_delete="", to_add=""):
    global all_roads
    if mode == "usial":
        for road in list(all_roads):
            if all_roads[road][1] > 1:
                all_roads[road][1] -= 1
            else:
                if len(all_roads) == 1:
                    all_roads[road][0] = "open"
                    all_roads[road][1] = road_interval
                elif all_roads[road][0] == "open":
                    all_roads[road][0] = "closed"
                    all_roads[road][1] = road_interval * len(all_roads) - road_interval
                else:
                    all_roads[road][0] = "open"
                    all_roads[road][1] = road_interval

    elif mode == "delete":
        all_roads.pop(to_delete)

    elif mode == "add":
        if len(all_roads) == 0:
            all_roads.setdefault(to_add, ["open", road_interval])
        else:
            last_time = ""
            for ind, key in enumerate(all_roads):
                if "open" in all_roads[key]:
                    last_time = all_roads[list(all_roads)[ind - 1]][1]
            if len(all_roads) == 1:
                all_roads.setdefault(to_add, ["closed", last_time])
            else:
                all_roads.setdefault(to_add, ["closed", last_time + road_interval])

def open_system():
    global all_roads
    while running:  # while thread runs
        uptime = round(time.time() - start_time)
        if state == "system":  # and if in system state
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"! {uptime}s. have passed since system startup !")
            print(f"! Number of roads: {roads_num} !")
            print(f"! Interval: {road_interval} !\n")
            for i in all_roads:
                color = "\u001B[31m" if all_roads[i][0] == "closed" else "\u001B[32m"
                print(f'Road "{i}" will be {color}{all_roads[i][0]} for {all_roads[i][1]}s.{"\u001B[0m"}')
            print('\n! Press "Enter" to open menu !')
            time.sleep(1)
            timers("usial")

def check_input(x):
    while True:
        if not x.isdigit() or int(x) <= 0:
            x = input("Incorrect input. Try again: ")
        else:
            return int(x)

start_time = time.time()
all_roads = dict()
state = "menu"  # switcher between states
running = True  # running flag
counter_thread = threading.Thread(target=open_system, name="QueueThread")
counter_thread.start()

print("Welcome to the traffic management system!")
roads_num = check_input(input("Input the number of roads: "))
road_interval = check_input(input("Input the interval: "))

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    main_menu()
    choice = input()
    if choice == "1":
        add_road()
        input()
    elif choice == "2":
        delete_road()
        input()
    elif choice == "3":
        state = "system"  # and turns to thread
        input()  # when the main thread waits for input open_system is active
        state = "menu"  # main thread is active again
    elif choice == "0":
        running = False
        counter_thread.join()
        print("Bye!")
        break
    else:
        print("Incorrect option")
        input()