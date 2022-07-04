def greet(bot_name, birth_year):
    print('Hello! My name is ' + bot_name + '.')
    print('I was created in ' + birth_year + '.')


def remind_name():
    print('Please, remind me your name.')
    name = input()
    print('What a great name you have, ' + name + '!')


def guess_age():
    print('Let me guess your age.')
    print('Enter remainders of dividing your age by 3, 5 and 7.')

    rem3 = int(input())
    rem5 = int(input())
    rem7 = int(input())
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print("Your age is " + str(age) + "; that's a good time to start programming!")


def count():
    print('Now I will prove to you that I can count to any number you want.')

    num = int(input())
    curr = 0
    while curr <= num:
        print(curr, '!')
        curr = curr + 1


def test():
    print("Let's test your programming knowledge.")
    print("Why do we use methods?")

    #  text values
    var_1 = "1. To repeat a statement multiple times."
    var_2 = "2. To decompose a program into several small subroutines."
    var_3 = "3. To determine the execution time of a program."
    var_4 = "4. To interrupt the execution of a program."
    wrong_answer = "Please, try again!"
    right_answer = "Completed, have a nice day!"

    #  making right value
    var_2_list = list(var_2)
    var_2_value = int(var_2_list[0])
    
    print(var_1)
    print(var_2)
    print(var_3)
    print(var_4)
    
    answer = 0
    
    while answer != var_2_value:
        answer = int(input())
        if answer!= var_2_value:
            print(wrong_answer)
        else:
            print(right_answer)
            break

def end():
    print('Congratulations, have a nice day!')


greet('Aid', '2020')  # change it as you need
remind_name()
guess_age()
count()
test()
end()
