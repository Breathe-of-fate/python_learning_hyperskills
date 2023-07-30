import datetime
import re

def filter_parameter(x):
    if x == "date":
        x = "\nEnter date (in format «YYYY-MM-DD»):\n"
    elif user_input == "note":
        x = "\nEnter text of note:\n"
    else:
        x = "\nEnter name:\n"
    return x

def search(what, where, by_what):
    while True:    
        records = {}
        for keys in where:
            records.setdefault(keys, [])
            for record in where[keys]:
                if re.findall(what[5:] if by_what == "date" else what, record, flags=re.IGNORECASE):
                    records[keys] += [record[12:]]

        if by_what in ("note", "name"):
            amount = len(records[by_what])
            if amount:
                what = f'"{what}"'
                print(f"\nFound {amount} {'note(s) that contain ' + what if by_what == 'note' else 'date(s) of birth'}:")
                print(*records[by_what], sep="\n")
                return records
            else:
                what = input(f"\nNo such {'note' if by_what == 'note' else 'person'} found. Try again:\n")
                continue
        elif by_what == "date":
            amount = [len(records["note"]), len(records["name"])]
            if amount[0] != 0 and amount[1] != 0:
                print(f"\nFound {str(amount[0]) + ' note(s)' if amount[0] else ''}{' and ' + str(amount[1]) + ' date(s) of birth on this date' if amount[1] else ''}:\n")
                print(*records["note"] if amount[0] else '', *records["name"] if amount[1] else '', "", sep="\n")
                return records
            else:
                what = input(f"\nNo such {by_what} found. Try again:\n")

def check_input(text_in_input, what_to_search, error_text):
    user_input = input(text_in_input)
    while user_input not in what_to_search:
        print(error_text)
        user_input = input(text_in_input)
    return user_input

def write_read_notes(save_file_name, what_to_do, open_mode="a+", what_to_write={}):
    with open(save_file_name, open_mode) as save_file:
        if what_to_do == "read":
            save_file.seek(0)
            all_records = {}
            for i in save_file.readlines():
                note = i.replace("\n", "").split(", ")
                note_or_name = "note" if len(note) > 4 else "name"
                if note_or_name == "note":
                    record = f'Before the event note "{note[1]}" remains: {note[2]} day(s), {note[3]} hour(s) and {note[4]} minute(s).'
                else:
                    record = f'{note[1]}’s birthday is {"today" if note[2] == "0" else "in " + str(note[2] + " days")}. He (she) turns {note[3]} years old.'
                all_records.setdefault(note_or_name, [])
                all_records[note_or_name] += [f"{note[0]}, {record}"]
            return all_records
            
        elif what_to_do == "write":
            for i in what_to_write:
                save_file.write(f"{i}, {what_to_write[i]}\n")

today_date = datetime.datetime.today()
save_file_name = "notes.txt"
print(f"Current date and time:\n{today_date.strftime('%Y-%m-%d %H:%M')}")

while True:
    all_notes = write_read_notes(save_file_name, "read")
    user_input = check_input("\nEnter the command (add, view, delete, exit):\n", ("add", "view", "delete", "exit"), "\nThis command is not in the menu")
    if user_input == "add":
        user_input = input("\nWhat do you want to add (note, birthday)?\n")
        if user_input == "note":
            user_input = int(input("\nHow many notes do you want to add?\n"))
            if user_input > 0:
                notes_to_add = {}
                for i in range(1, user_input + 1):
                    while True:
                        user_input = input(f"\nEnter date and time of note #{i} (in format «YYYY-MM-DD HH:MM»):\n")
                        if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", user_input) is None:
                            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
                        else:
                            date_time_to_check = re.split('\D+', user_input)
                            if int(date_time_to_check[1]) not in range(1, 13):
                                print("Incorrect month value. The month should be in 1-12.")
                            elif int(date_time_to_check[3]) not in range(0, 24):
                                print("Incorrect hour value. The hour should be in 00-23.")
                            elif int(date_time_to_check[4]) not in range(0, 60):
                                print("Incorrect minute value. The minutes should be in 00-59.")
                            else:
                                break

                    notation = input(f"Enter text of note #{i}:\n")
                    notation_date = datetime.datetime.strptime(user_input, '%Y-%m-%d %H:%M')
                    remains = notation_date - today_date
                    days_remains = remains.days
                    hours_remains = remains.seconds // 3600
                    minutes_remains = (remains.seconds % 3600) // 60
                    notes_to_add[str(notation_date)[:10]] = f"{notation}, {days_remains}, {hours_remains}, {minutes_remains}"
                
                write_read_notes(save_file_name, "write", what_to_write=notes_to_add)
                print("\nNotes added!")
        
        elif user_input == "birthday":
            user_input = int(input("\nHow many dates of birth do you want to add?\n"))
            if user_input > 0:
                births_to_add = {}
                for i in range(1, user_input + 1):
                    name = input(f"\nEnter the name of #{i}:\n")
                    only_date_today = today_date.date()
                    birth_date = datetime.date.fromisoformat(input(f"Enter the date of birth of #{i} (in format «YYYY-MM-DD»):\n"))
                    birth_this_year = datetime.date(today_date.date().year, birth_date.month, birth_date.day)
                    birth_next_year = datetime.date(today_date.date().year + 1, birth_date.month, birth_date.day)

                    if only_date_today <= birth_this_year:
                        days_before = (birth_this_year - only_date_today).days
                        age = only_date_today.year - birth_date.year
                    else:
                        days_before = (birth_next_year - only_date_today).days
                        age = only_date_today.year - birth_date.year + 1
                        
                    births_to_add[birth_date] = f"{name}, {days_before}, {age}"

                write_read_notes(save_file_name, "write", what_to_write=births_to_add)
                print("\nBirthdates added!")

    elif user_input == "view":
        user_input = check_input("\nWhat do you want to view (date, note, name)?\n", ("date", "note", "name"), "\nThis command is not in the menu\n")
        text_in_input = filter_parameter(user_input)
        search(input(text_in_input), all_notes, user_input)

    elif user_input == "delete":
        user_input = check_input("\nWhat do you want to delete (date, note, name)?:\n", ("date", "note", "name"), "\nThis command is not in the menu\n")
        text_in_input = filter_parameter(user_input)
        founded = search(input(text_in_input), all_notes, user_input)

        for key in all_notes:
            for record in all_notes[key]:
                if record[12:] in founded[key]:
                    to_delete = re.search(r'".+"', record).group() if re.search("Before", record) else f'"{re.search(r", (.+)’", record).group(1)}"'
                    note_or_birth = "Note" if re.search("Before", record) else "Birthdate"
                    if input(f'Are you sure you want to delete {to_delete}?\n') == "yes":
                        all_notes[key].remove(record)
                        print(note_or_birth, "deleted!\n")
                    else:
                        print("Deletion canceled.\n")
        
        to_write = []
        for key in all_notes:
            for record in all_notes[key]:
                pattern = "(.+),.+\"(.+)\".+ (-*\d+) d.+ (\d+).+ (\d+)" if re.search(r'Before', record, flags=re.IGNORECASE) else \
                          "(.+), (.+)’.+in (\d+).+s (\d+)"
                line = ", ".join([ii for i in re.findall(pattern, record) for ii in i])
                to_write.append(f"{line}\n")
        with open(save_file_name, "w") as save_file:
            save_file.writelines(to_write)
        
    elif user_input == "exit":
        break