import random

names = ["John", "Jack"]
k = 1
s_ = "'s turn!"
one_pencil = "|"
first_name = 0

print("How many pencils would you like to use:")
pencils = input()

while pencils.isnumeric() is False or pencils == "0":
    if pencils.isnumeric() is False:
        print("The number of pencils should be numeric")
        pencils = input()
    elif pencils == "0":
        print("The number of pencils should be positive")
        pencils = input()

pencils = int(pencils)

print("Who will be the first (" + names[0] + ", " + names[1] + "):")
first_name = input()

while first_name not in names:
    print("Choose between", names[0], "and", names[1])
    first_name = input()

print(pencils * one_pencil)

while pencils > 0:

    if first_name == names[0]:

        print(names[0] + s_)
        pencils_2 = input()

        while pencils_2 == "0" or pencils_2.isnumeric() is False or int(pencils_2) > 3 or int(pencils_2) > pencils:
            if pencils_2 == "0" or pencils_2.isnumeric() is False:
                print("Possible values: '1', '2' or '3'")
                pencils_2 = input()
            elif int(pencils_2) > 3:
                if int(pencils_2) > 3 and int(pencils_2) > pencils:
                    print("Too many pencils were taken")
                    print("Possible values: '1', '2' or '3'")
                    pencils_2 = input()
                elif int(pencils_2) > 3 and int(pencils_2) < pencils:
                    print("Too many pencils were taken")
                    print("Possible values: '1', '2' or '3'")
                    pencils_2 = input()
                elif int(pencils_2) > 3 and int(pencils_2) == pencils:
                    print("Too many pencils were taken")
                    print("Possible values: '1', '2' or '3'")
                    pencils_2 = input()
            elif int(pencils_2) > pencils:
                print("Too many pencils were taken")
                pencils_2 = input()
        pencils -= int(pencils_2)
        print(pencils * one_pencil)
        first_name = names[1]
    else:
        print(names[1] + "'s turn:")
        if pencils % 4 == 0:
            pencils_2 = 3
        elif pencils % 4 == 3:
            pencils_2 = 2
        elif pencils % 4 == 2:
            pencils_2 = 1
        elif pencils == 1:
            pencils_2 = 1
        else:
            pencils_2 = random.randint(1, 3)

        pencils -= int(pencils_2)
        print(pencils_2)
        print(pencils * one_pencil)
        first_name = names[0]

if first_name == names[0]:
    print(names[0], "won!")
else:
    print(names[1], "won!")
