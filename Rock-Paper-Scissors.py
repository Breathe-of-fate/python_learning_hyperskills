import random

username = input("Enter your name: ")
print("Hello,", username)

rating_file = open("rating.txt", "r+")
rating = rating_file.readlines()
rating_value = [i[len(username) + 1:].replace("\n", "") for i in rating if username in i]
rating_names = [i[:len(username)] for i in rating]

if username not in [i[:len(username)] for i in rating]:
    print(f"{username} 0", file=rating_file, flush=True)
rating_file.close()

all_combinations = {"rock": ["lightning", "gun", "air", "water", "dragon", "paper", "devil"],
                    "gun": ["lightning", "sponge", "air", "water", "dragon", "paper", "devil"],
                    "lightning": ["wolf", "sponge", "air", "water", "dragon", "paper", "devil"],
                    "devil": ["wolf", "sponge", "air", "water", "dragon", "paper", "tree"],
                    "dragon": ["wolf", "sponge", "air", "water", "human", "paper", "tree"],
                    "water": ["wolf", "sponge", "air", "snake", "human", "paper", "tree"],
                    "air": ["wolf", "sponge", "scissors", "snake", "human", "paper", "tree"],
                    "paper": ["wolf", "sponge", "scissors", "snake", "human", "fire", "tree"],
                    "sponge": ["wolf", "rock", "scissors", "snake", "human", "fire", "tree"],
                    "wolf": ["gun", "rock", "scissors", "snake", "human", "fire", "tree"],
                    "tree": ["gun", "rock", "scissors", "snake", "human", "fire", "lightning"],
                    "human": ["gun", "rock", "scissors", "snake", "devil", "fire", "lightning"],
                    "snake": ["gun", "rock", "scissors", "dragon", "devil", "fire", "lightning"],
                    "scissors": ["gun", "rock", "water", "dragon", "devil", "fire", "lightning"],
                    "fire": ["lightning", "gun", "air", "water", "dragon", "rock", "devil"]}

element_list = input()

if element_list == "":
    element_list = ["rock", "scissors", "paper"]
else:
    element_list = element_list.split(",")

print("Okay, let's start")

while True:

    user_choice = input()

    if user_choice == "!exit":
        print("Bye!")
        break
    elif user_choice == "!rating":
        print("Your rating:", rating_value)
        continue
    elif user_choice not in element_list:
        print("Invalid input")
        continue

    computer_choice = random.choice(element_list)

    if user_choice == computer_choice:
        print(f"There is a draw ({computer_choice})")
        win_scores = 50
    elif user_choice in all_combinations[computer_choice]:
        print(f"Well done. The computer chose {computer_choice} and failed")
        win_scores = 100
    else:
        print(f"Sorry, but the computer chose {computer_choice}")
        win_scores = 0

    rating_value = str(int("".join(rating_value)) + win_scores)
    rating[rating_names.index(username)] = "".join([i[:len(username)] for i in rating if username in i]) + " " + "".join(rating_value) + "\n"

    rating_file = open("rating.txt", "w")
    print("".join(rating), file=rating_file, flush=True)
    rating_file.close()