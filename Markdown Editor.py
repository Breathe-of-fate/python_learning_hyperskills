formatters = ["plain", "bold", "italic", "header", "link", "inline-code", "ordered-list", "unordered-list", "new-line"]
formatter = ""
formated_text = []

def print_list():
    if len(formated_text) != 0:
        print(*formated_text, sep="")

def plain():
    formated_text.append(f"{input('Text: ')}")
    print_list()

def bold():
    formated_text.append(f"**{input('Text: ')}**")
    print_list()

def italic():
    formated_text.append(f"*{input('Text: ')}*")
    print_list()

def header():
    level = ""
    while True:
        level = int(input("Level: "))
        if level in range(1, 7):
            formated_text.append(f"{'#' * level} {input('Text: ')}\n")
            print_list()
            break
        else:
            print("The level should be within the range of 1 to 6")

def link():
    formated_text.append(f"[{input('Label: ')}]({input('URL: ')})")
    print_list()

def inline_code():
    formated_text.append(f"`{input('Text: ')}`")
    print_list()

def new_line():
    formated_text.append(f"\n")
    print_list()

def lists():
    num_of_rows = int(input("Number of rows: "))
    while num_of_rows <= 0:
        print("The number of rows should be greater than zero")
        num_of_rows = int(input("Number of rows: "))
    if "un" in formatter:
        for i in range(1, num_of_rows + 1):
            formated_text.append(f"* {input(f'Row #{i}: ')}\n")
    else:
        for i in range(1, num_of_rows + 1):
            formated_text.append(f"{i}. {input(f'Row #{i}: ')}\n")
    print_list()

while formatter != "!done":
    formatter = input("Choose a formatter: ")
    if formatter == "!help":
        print("Available formatters:", *formatters, "\nSpecial commands: !help !done")
    elif formatter in formatters:
        if formatter == "plain":
            plain()
        elif formatter == "bold":
            bold()
        elif formatter == "italic":
            italic()
        elif formatter == "header":
            header()
        elif formatter == "link":
            link()
        elif formatter == "inline-code":
            inline_code()
        elif formatter == "new-line":
            new_line()
        elif formatter == "ordered-list" or "unordered-list":
            lists()
    elif formatter != "!done" and formatter not in formatters:
        print("Unknown formatting type or command.")

with open("output.md", "w") as f:
    [f.write(i) for i in formated_text]