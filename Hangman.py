import random
import string

scoreboard = []

print("H A N G M A N")

while True:

    words_library = ["python", "java", "swift", "javascript"]
    word_to_guess = random.choice(words_library)
    attempts = 8
    word_to_show = [i.replace(i, "-") for i in word_to_guess]  # making a word only a - sequence
    indicies = []  # emply list for guessted letters
    input_history = []

    menu = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')

    if menu == "exit":
        break
    elif menu == "results":
        print("You won:", scoreboard.count("w"), "times.\n" + "You lost:", scoreboard.count("l"), "times.")
        continue
    elif menu == "play":

        while attempts !=0:

            print("\n" + "".join(word_to_show))
            user_input = input("Input a letter: ")

            if  len(user_input) != 1:
                print("Please, input a single letter.\n")
                continue
            elif user_input not in string.ascii_lowercase:
                print("Please, enter a lowercase letter from the English alphabet.\n")
                continue
            else:
                input_history.append(user_input)

                if input_history.count(user_input) > 1:
                    print("You've already guessed this letter.")
                elif user_input in word_to_guess:
                    for index in range(len(word_to_guess)):  # for each letter in word
                        if word_to_guess.startswith(user_input, index):  # if the meaning for index starts with user input
                            indicies.append(index)  # add this index to list
                            for index in indicies:  # for each index in list
                                word_to_show[index] = user_input  # replacing - with guessed letter
                    if "-" not in word_to_show:
                        print("\nYou guessed the word", word_to_guess + "!\n" + "You survived!")
                        scoreboard.append("w")
                        break
                elif user_input not in word_to_guess:
                    print("That letter doesn't appear in the word.")
                    attempts -= 1
                    if attempts == 0:
                        print("You lost!")
                        scoreboard.append("l")
                        break

            indicies.clear()  # we need it for a new cycle of searching

        continue