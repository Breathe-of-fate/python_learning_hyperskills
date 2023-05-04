earned_amount = {"Bubblegum": 202, 
                 "Toffee": 118, 
                 "Ice cream": 2250, 
                 "Milk chocolate":1680, 
                 "Doughnut": 1075, 
                 "Pancake": 80}
income = sum(earned_amount.values())

print("Earned amount:", *[f"{i}: {earned_amount[i]}" for i in earned_amount], f"\nIncome: {income}", sep="\n")
print(f"Net income: {income - int(input('Staff expenses: ')) - int(input('Other expenses: '))}")