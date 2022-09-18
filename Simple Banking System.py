import sqlite3
import random

open_db = sqlite3.connect("card.s3db")
modify_db = open_db.cursor()
modify_db.execute("""CREATE TABLE IF NOT EXISTS card (  id INTEGER, 
                                                        number TEXT, 
                                                        pin TEXT, 
                                                        balance INTEGER DEFAULT 0   );""")

user_id = []


def read_db():

    modify_db.execute("SELECT * FROM card")
    return {str(i[0]): [i[1], i[2], i[3]] for i in modify_db.fetchall()}


def creating_account(x):

    while True:

        issuer_identification_number = "400000"
        customer_account_number = "".join(random.choices([str(i) for i in range(1, 10)], k=9))
        pin = "".join(random.choices([str(i) for i in range(10)], k=4))

        if customer_account_number in x:
            continue
        else:

            number_to_check = issuer_identification_number + customer_account_number
            luhn1 = [int(number_to_check[i])*2 if i % 2 == 0 else int(number_to_check[i]) for i in range(15)]
            luhn2 = [i - 9 if i > 9 else i for i in luhn1]

            if int(str(sum(luhn2))[1]) != 0:
                checksum = str(10 - int(str(sum(luhn2))[1]))
            else:
                checksum = "0"

            card_number = issuer_identification_number + customer_account_number + checksum
            modify_db.execute(f"INSERT into card VALUES ('{customer_account_number}', '{card_number}', '{pin}', 0)")
            open_db.commit()
            break

    print("Your card has been created", "Your card number:", card_number, "Your card PIN:", pin, "", sep="\n")


def user_account():
    while True:
        print("\n1. Balance", "2. Add income", "3. Do transfer",
            "4. Close account", "5. Log out", "0. Exit", sep="\n")
        user_choice = input()
        if user_choice == "1":
            print(f"\nBalance: {read_db()[user_id[0]][2]}")
            continue
        elif user_choice == "2":
            print("\nEnter income:")
            user_choice = int(input())
            modify_db.execute(f"UPDATE card SET balance = balance + {user_choice} WHERE id = {user_id[0]}")
            open_db.commit()
            continue
        elif user_choice == "3":
            print("\nTransfer", "Enter card number:", sep="\n")
            user_choice = input()
            luhn1 = [int(user_choice[i])*2 if i % 2 == 0 else int(user_choice[i]) for i in range(15)]
            luhn2 = [i - 9 if i > 9 else i for i in luhn1]
            if int(str(sum(luhn2))[1]) != 0:
                checksum = str(10 - int(str(sum(luhn2))[1]))
            else:
                checksum = "0"
            if checksum != user_choice[15]:
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            elif user_choice[6:15] not in read_db():
                print("Such a card does not exist.")
                continue
            elif user_choice[6:15] == user_id[0]:
                print("You can't transfer money to the same account!")
                continue
            print("Enter how much money you want to transfer:")
            to_transfer = int(input())
            if to_transfer > read_db()[user_id[0]][2]:
                print("Not enough money!")
                continue
            else:
                modify_db.execute(f"UPDATE card SET balance = balance + {to_transfer} WHERE id = {user_choice[6:15]}")
                modify_db.execute(f"UPDATE card SET balance = balance - {to_transfer} WHERE id = {user_id[0]}")
                open_db.commit()
                print("Success!")
        elif user_choice == "4":
            modify_db.execute(f"DELETE FROM card WHERE id = {user_id[0]}")
            open_db.commit()
            return "close"
        elif user_choice == "5":
            print("\nYou have successfully logged out!\n")
            return "log_out"
        elif user_choice == "0":
            print("\nBye!")
            return "exit"


def check_login(x):
    while True:
        print("\nEnter your card number:")
        user_input_card = input()
        print("Enter your PIN:")
        user_input_pin = input()
        if user_input_card[6:15] in x and x[user_input_card[6:15]][1] == user_input_pin:
            print("\nYou have successfully logged in!")
            user_id.append(user_input_card[6:15])
            return True
        else:
            print("\nWrong card number or PIN!\n")
            return False


while True:
    print("1. Create an account", "2. Log into account", "0. Exit", sep="\n")
    user_choice = input()

    if user_choice == "1":
        creating_account(read_db())
        continue
    elif user_choice == "2":
        if check_login(read_db()):
            if user_account() == "exit":
                print("Bye!")
                break
            else:
                continue
        else:
            continue
    elif user_choice == "0":
        print("Bye!")
        break
