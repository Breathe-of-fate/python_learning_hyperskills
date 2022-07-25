def is_one_digit(v):  # name of function 1
    if v == int(v) and (- 10 < v < 10):  # condition for yes
        a = True  # yes output
    else:  # condition for no
        a = False  # no output
    return a  # return output

def check(v1, v2, v3):  # name of function 2
    msg = ""  # msg initiation
    msg_6 = " ... lazy"
    msg_7 = " ... very lazy"
    msg_8 = " ... very, very lazy"
    msg_9 = "You are"
    if is_one_digit(v1) and is_one_digit(v2):  # condition 1 yes
        msg = msg + msg_6  # condition 1 no
    if (v1 == 1 or v2 == 1) and v3 == "*":  # condition 2 yes
        msg = msg + msg_7  # condition 2 no
    if (v1 == 0 or v2 == 0) and (v3 == "*" or v3 == "+" or v3 == "-"):  # condition 3 yes
        msg = msg + msg_8  # condition 3 no
    if msg != "":  # condition 4 yes
        msg = msg_9 + msg  # condition 4 no
        print(msg)

memory = 0  # initializing memory and making it float or int

oper_list = ["+", "-", "*", "/"]  # operation list
result = 0

while True:  # start

    print("Enter an equation")  # print mesg_0
    calc = input().split(" ")  # read calc

    x, oper, y = calc[0], calc[1], calc[2]  # split calc into variables x, operation, y

    if x == "M" or y == "M":  # checking memory
        if x == "M":
            x = memory
        if y == "M":
            y = memory
        elif y == "M":
            y = memory

    if str(x).isalpha() or str(y).isalpha():  # x or y is not a number -> yes condition
        print("Do you even know what numbers are? Stay focused!")  # print msg_1
        continue  # to the start
    else:  # x and y are numbers -> no condition -> next
        if oper not in oper_list:  # operation is not an operation -> no condition
            print("Yes ... an interesting math operation. You've slept through all classes, haven't you?")  # print msg_2
            continue  # to the start
        else:  # operation is an operation -> yes condition -> next

            if x == str(x):  # checking what x is and make it right
                if "." in str(x):
                    x = float(x)
                else:
                    x = int(x)

            if y == str(y):
                if "." in str(y):  # checking what y is and make it right
                    y = float(y)
                else:
                    y = int(y)

            check(x, y, oper)  # making some exercise sheet nobody needs really

            if oper == "+":  # from here to the end if checking the operator
                result = (x + y)
            elif oper == "-":
                result = (x - y)
            elif oper == "*":
                result = (x * y)
            elif oper == "/":
                if oper == "/" and y != 0:
                    result = (x / y)
                else:
                    print("Yeah... division by zero. Smart move...")  # print msg_3
                    continue  # to the start
        print(float(result))  # final result

        flag = False  # a flag to quit cycle

        while True:
            print("Do you want to store the result? (y / n):")  # print msg_4
            a = input()  # read input

            if a == "n":
                break
            elif a == "y":  # if yes then

                if is_one_digit(result):  # checking one more stupid condition

                    msg_index = 10
                    msg_10 = "Are you sure? It is only one digit! (y / n)"
                    msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
                    msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
                    msg_ = ""

                    while msg_index <= 12:  # checking a condition for yes answers

                        print(locals().get("".join(("msg_", str(msg_index)))))  # a string to show in each iteration
                        a = input()  # input a value

                        if a == "y":  # if yes then
                            if msg_index < 12:  # cheching if it is less 12
                                msg_index += 1  # if so + 1
                                continue  # and again
                            if msg_index == 12:  # if it is 12
                                flag = True  # chaning flag
                                memory = result  # write in memory
                                break  # and quit from this cycle
                        elif a == "n":  # if input is n
                            if a == "n":  # if input is n
                                flag = True  # chanhing flag
                                break  # quit from this cycle
                            else:  # if it is no but can be inputed amother
                                continue  # new iteration
                        else:  # if smth different
                            break  # quit this cycle
                        memory = result  # cycle is completed

                else:  # if function is false
                    memory = result  # write in memory
                    break  # next
            if flag is True:  # a flag to out this cycle
                break  # next

        print("Do you want to continue calculations? (y / n):")  # print msg_5
        a = input()  # read answer
        if a == "y" or a == "n":  # checking yes or no
            if a == "y":  # if yes
                continue  # start again
            elif a == "n":  # if no
                break  # end
