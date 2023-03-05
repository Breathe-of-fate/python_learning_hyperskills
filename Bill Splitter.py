import random

def splitter(x, y, z):
    for i in x:
        x[i] = round(y / z, 2)

people = int(input("Enter the number of friends joining (including you):\n"))
party = {}

if people <= 0:
    print("\nNo one is joining for the party")
else:
    print("\nEnter the name of every friend (including you), each on a new line:")
    for i in range(people):
        party[input()] = 0
    bill = float(input('\nEnter the total bill value:\n'))
    lucky_one = input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n')
    if lucky_one.lower() == 'yes':
        lucky_one = random.choice(list(party))
        splitter(party, bill, len(party) - 1)
        party[lucky_one] = 0
        print(f'\n{lucky_one} is the lucky one!')
    else:
        print("\nNo one is going to be lucky")
        splitter(party, bill, len(party))
    print(f'\n{party}')