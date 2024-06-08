from io import StringIO
import argparse

memory_file = StringIO()
all_cards = dict()
raiting = dict()

def print_n_log(a):
    memory_file.read()
    memory_file.write(a)
    print(a)

def input_n_log(a):
    memory_file.read()
    memory_file.write(a)
    return input(a)

def check_term(a, b, c):
    while a in b:
        print_n_log(f'The {c} "{a}" already exists. Try again:')
        a = input_n_log(a)
    return a

def add_cards():
    card = check_term(input_n_log(f"The card:\n"), all_cards, "card")
    all_cards.setdefault(card, "")
    definition = check_term(input_n_log(f"The definition of the card:\n"), all_cards.values(), "definition")
    all_cards[card] = definition
    print_n_log(f'The pair ("{card}":"{definition}") has been added.\n')
        
def remove_card():
    to_remove = input_n_log("Which card?\n")
    try:
        del all_cards[to_remove]
        print_n_log("The card has been removed.\n")
    except:
        print_n_log(f'Can\'t remove "{to_remove}": there is no such card.\n')
        
def import_cards(a):
    try:
        with open(a, "r") as file:
            from_file = file.readlines()
            for i in from_file:
                card, definition, rate = i.split(", ")
                all_cards[card] = definition
                raiting[card] = int(rate.strip("\n"))
        print_n_log(f"{len(from_file)} cards have been loaded.\n")
    except:
        print_n_log("File not found.\n")
        
def export_cards(a):
    with open(a, "a+") as file:
        for i, ii in list(all_cards.items()):
            if i in raiting:
                file.write(f"{i}, {ii}, {raiting[i]}\n")
            else:
                file.write(f"{i}, {ii}, {0}\n")
    print_n_log(f"{len(all_cards)} cards have been saved.\n")

def check_knowledge():
    for i in range(int(input_n_log("How many times to ask?\n"))):
        card, definition = list(all_cards.items())[i % len(all_cards)]
        user_input = input_n_log(f'Print the definition of "{card}":\n')
        if user_input == all_cards[card]:
            print_n_log("Correct!\n")
        elif user_input != all_cards[card] and user_input in all_cards.values():
            definition_in = [key for key, value in all_cards.items() if value == user_input][0]
            raiting.setdefault(card, 0)
            raiting[card] += 1
            print_n_log(f'Wrong. The right answer is "{all_cards[card]}", but your definition is correct for "{definition_in}".\n')
        else:
            raiting.setdefault(card, 0)
            raiting[card] += 1
            print_n_log(f'Wrong. The right answer is "{all_cards[card]}".\n')
            
def loging():
    with open(input("File name:\n"), "w") as log:
        for line in memory_file.getvalue():
            log.write(line)
        print("The log has been saved.\n")
            
def hardest_cards():
    hardest_pairs = sorted(raiting.items(), key=lambda x:x[1], reverse=True)
    hardest_pairs2 = [i for i in hardest_pairs if i[1] == hardest_pairs[0][1]]
    if not hardest_pairs2:
        print("There are no cards with errors.\n")
    elif len(hardest_pairs2) > 1:
        print(f'The hardest cards are {str([i[0] for i in hardest_pairs2]).strip("[]").replace("\'", "\"")}.\n')
    else:
        print(f'The hardest card is "{hardest_pairs2[0][0]}". You have {hardest_pairs2[0][1]} errors answering it.\n')

parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

if args.import_from:
    import_cards(args.import_from)
            
while True:
    user_command = input_n_log("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
    if user_command in "add":
        add_cards()
    elif user_command in "remove":
        remove_card()
    elif user_command in "import":
        import_cards(input_n_log("File name:\n"))
    elif user_command in "export":
        export_cards(input_n_log("File name:\n"))
    elif user_command in "ask":
        check_knowledge()
    elif user_command in "exit":
        print_n_log("Bye bye!")
        break
    elif user_command in "log":
        loging()
    elif user_command in "hardest card":
        hardest_cards()
    elif user_command in "reset stats":
        raiting.clear()
        print("Card statistics have been reset.\n")

if args.export_to:
    export_cards(args.export_to)