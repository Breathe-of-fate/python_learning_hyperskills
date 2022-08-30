class CoffeeMachine:
    
    def __init__(self, water, milk, coffee, cups, money):
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cups = cups
        self.money = money
    
    def status(self):
        print("\nThe coffee machine has:", f"{self.water} ml of water", f"{self.milk} ml of milk", f"{self.coffee} g of coffee beans", f"{self.cups} disposable cups", f"${self.money} of money", sep="\n")
        
    def fill(self, water, milk, coffee, cups):
        self.water += water
        self.milk += milk
        self.coffee += coffee
        self.cups += cups
    
    def take(self):
        print(f"I gave you ${self.money}\n")
        self.money = 0
    
    def buy(self):
        print("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
        action = input()

        if action == 'back':
            return 1
        elif action == "1":
            if self.check_ingridients(-250, -0, -16, -1):
                self.water -= 250
                self.milk -= 0
                self.coffee -= 16
                self.cups -= 1
                self.money += 4
        elif action == "2":
            if self.check_ingridients(-350, -75, -20, -1):
                self.water -= 350
                self.milk -= 75
                self.coffee -= 20
                self.cups -= 1
                self.money += 7
        elif action == "3":
            if self.check_ingridients(-200, -100, -12, -1):
                self.water -= 200
                self.milk -= 100
                self.coffee -= 12
                self.cups -= 1
                self.money += 6

    def check_ingridients(self, need_water, need_milk, need_coffee, need_cups):
        ingridients_needed = [need_water, need_milk, need_coffee, need_cups]
        ingridients_have = [self.water, self.milk, self.coffee, self.cups]
        ingridients_names = ["water", "milk", "coffee", "cups"]
        checked_list = [ingridients_names[i] for i in range(0, 3) if ingridients_have[i] + ingridients_needed[i] < 0]
            
        if len(checked_list) > 0:
            print("Sorry, not enough", str(*checked_list) + "!\n")
            return 0
        else:
            print("I have enough resources, making you a coffee!\n")
            return True
        
    def start(self):
    	while True:
            action = input("Write action (buy, fill, take, remaining, exit):\n")
            if action == "buy":
                self.buy()
            elif action == "fill":
                self.fill(
                	int(input("\nWrite how many ml of water you want to add:\n")),
                  	int(input("Write how many ml of milk you want to add:\n")),
                  	int(input("Write how many grams of coffee coffee you want to add:\n")),
                  	int(input("Write how many disposable cups you want to add:\n")))
                print()
            elif action == "take":
                self.take()
            elif action == "remaining":
                self.status()
            elif action == "exit":
            	break

CoffeeMachine(400, 540, 120, 9, 550).start()

# or it is possible to use this one:

def coffee_machine(water, milk, coffee, cups, money):

    while True:

        def check_ingridients(need_water, need_milk, need_coffee, need_cups):
            ingridients_needed = [need_water, need_milk, need_coffee, need_cups]
            ingridients_have = [water, milk, coffee, cups]
            ingridients_names = ["water", "milk", "coffee", "cups"]
            checked_list = [ingridients_names[i] for i in range(0, 3) if ingridients_have[i] + ingridients_needed[i] < 0]
            
            if len(checked_list) > 0:
                print("Sorry, not enough", str(*checked_list) + "!\n")
                return 0
            else:
                print("I have enough resources, making you a coffee!\n")
            
        print("\nWrite action (buy, fill, take, remaining, exit):")

        action = input()
        
        if action == "buy":
            
            print("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")    
            
            action = input()
            
            if action == "back":
                continue
            
            elif int(action) == 1:
                if check_ingridients(-250, -0, -16, -1) == 0:
                    continue
                water -= 250
                milk -= 0
                coffee -= 16
                cups -= 1
                money += 4

            elif int(action) == 2:
                if check_ingridients(-350, -75, -20, -1) == 0:
                    continue
                water -= 350
                milk -= 75
                coffee -= 20
                cups -= 1
                money += 7

            elif int(action) == 3:
                if check_ingridients(-200, -100, -12, -1) == 0:
                    continue
                water -= 200
                milk -= 100
                coffee -= 12
                cups -= 1
                money += 6

        elif action == "fill":
            print("\nWrite how many ml of water you want to add:")
            water += int(input())
            print("Write how many ml of milk you want to add:")
            milk += int(input())
            print("Write how many grams of coffee beans you want to add:")
            coffee += int(input())
            print("Write how many disposable cups you want to add:")
            cups += int(input())

        elif action == "take":
            print(f"I gave you ${money}")
            money = 0

        elif action == "remaining":
            print("\nThe coffee machine has:", f"{water} ml of water", f"{milk} ml of milk", f"{coffee} g of coffee beans", f"{cups} disposable cups", f"${money} of money", sep="\n")

        elif action == "exit":
            break

coffee_machine(400, 540, 120, 9, 550)