import random

def check_answer():
    x = input()
    while x.isdigit() is False:
        if x!= "" and x[0] == '-' and x[1:].isdigit():
            return int(x)
        else:
            print("Incorrect format.")
            x = input()
    return int(x)

def incorrect_format(x, y, z=None):
    while x not in y:
        print("Incorrect format.")
        print(z) if z else None
        x = input()
    return x

print(warning := "Which level do you want? Enter a number:\n1 - simple operations with numbers 2-9\n2 - integral squares of 11-29")
user_choice = incorrect_format(input(), ("1", "2"), warning)

answers, counter = 0, 0

if user_choice == '1':
    while counter!= 5:
        print(ex := f'{random.randint(2, 9)} {random.choice(["-", "+", "*"])} {random.randint(2, 9)}')
        if check_answer() == int(eval(ex)):
            print("Right!")
            answers += 1
        else:
            print("Wrong!")
        counter += 1
    print(f"Your mark is {answers}/5.")
elif user_choice == "2":
    while counter!= 5:
        print(ex := random.randint(11, 29))
        if check_answer() == ex ** 2:
            print("Right!")
            answers += 1
        else:
            print("Wrong!")
        counter += 1
    print(f"Your mark is {answers}/5.")

if input("Would you like to save your result to the file? Enter yes or no.\n") in ("yes", "YES", "y", "Yes"):
    name = input("What is your name?\n")
    with open('results.txt', 'w') as file:
        print(f"{name}: {answers}/5 in level {user_choice} ({'simple operations with numbers 2-9' if user_choice == '1' else 'integral squares of 11-29'})", file=file)
    print('The results are saved in "results.txt".')