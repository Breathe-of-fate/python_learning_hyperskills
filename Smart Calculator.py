import re

memory = dict()

while (numbers := input()) != "/exit":

    if numbers.startswith("/"): 
        if numbers == "/help": print("The program calculates the sum of numbers")  
        else: print("Unknown command")  

    elif expression := re.match(r"^ *(\w+) *(=) *(-*\w+) *$", numbers): #if it is expression
        variable, sign, value = expression.group(1), expression.group(2), expression.group(3)
        if not re.match(r"^[a-zA-Z]+$", variable):
            print("Invalid identifier")
        elif not re.match(r"^([a-zA-Z]+|-*\d+)$", value):
            print("Invalid assignment")
        else:
            try: new_value = int(value)
            except:
                try: new_value = memory[value]
                except: print("Unknown variable")
            try: memory[variable] = new_value
            except: memory.setdefault(variable, new_value)

    elif re.match(r"^ *[a-zA-Z]+ *$", numbers):
        try: print(memory[numbers.strip()])
        except: print("Unknown variable")
        
    elif numbers:
        if '//' in numbers:
            print("Invalid expression")
        else:
            try: print(int(eval(numbers, memory)))
            except: print("Invalid expression")

print("Bye!")