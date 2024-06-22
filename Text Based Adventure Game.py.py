import json
import os

def input_checker(x, y):
  
  while x.casefold() not in y:
    print("Unknown input! Please enter a valid one.")
    x = input().casefold()
  return x

def menu():

  menu = {("1", "START"):"Start a new game (START)", 
          ("2", "LOAD"):"Load your progress (LOAD)", 
          ("3", "QUIT"):"Quit the game (QUIT)"}
  [print(f"{i[0]}. {ii}") for i, ii in menu.items()]

  right_answers = [i.casefold() for i, ii in menu] + [ii.casefold() for i, ii in menu]
  user_choice = input_checker(input(), right_answers)
    
  for i in menu:
    if user_choice in [i[0], i[1].casefold()]:
      return i[0]
    
      
def new_game():
  
  print("Starting a new game...")
  user_name = input("Enter a username ('/b' to go back): ")
  if user_name == "/b":
    return
  
  print("Create your character:")
  stats = {"name":input("   Name: "),
           "species":input("   Species: "),
           "gender":input("   Gender: ")}
  
  print("Pack your bag for the journey:")
  bag =  {"snack":input("   Snack: "),
          "weapon":input("   Weapon: "),
          "tool":input("   Tool: ")}
  
  print("Choose your difficulty:")
  diff_level = {("1", "Easy"):5, ("2", "Medium"):3, ("3","Hard"):1}
  [print(f"   {i[0]}. {i[1]}") for i in diff_level]
  right_answers = [i[0].casefold() for i in diff_level] + [i[1].casefold() for i in diff_level]
  difficulty = input_checker(input(), right_answers)
  for i, ii in diff_level.items():
    if difficulty in [i[0], i[1].casefold()]:
      difficulty = i[1].casefold()
      lives = ii
      break
   
  print(f'Good luck on your journey, {stats["name"]}!')
  print("Your character:", ", ".join(stats.values()))
  print("Your character:", ", ".join(bag.values()))
  print("Difficulty:", difficulty)
  print("Number of lives:", lives)
  print("---------------------------")
  
  return {"stats": {**stats}, "bag": {**bag}, "difficulty":difficulty, "user_name":user_name, "lives":lives}

def inner_menu(character, option, scene, level):
  
  game_menu = {"/h":"Type the number of the option you want to choose.\nCommands you can use:\n/i => Shows inventory.\n/q => Exits the game.\n/c => Shows the character traits.\n/h => Shows help.\n/s => Save the game", 
               "/c":f"Your character: {", ".join(character["stats"].values())}.\nLives remaining: {character["lives"]}\n", 
               "/i":f"Inventory: {", ".join(character["bag"].values())}\n",
               "/s":"Game saved!",
               "/q":"Thanks for playing!"}
  while True:
    print(game_menu[option])
    if option == "/s":
      with open(rf"data\saves\{character["user_name"]}.json", "w") as json_file:
          to_write = {"character":character["stats"],
                        "inventory": character["bag"],
                        "progress": {"level": f"level{level}", "scene": scene},
                        "lives": character["lives"],
                        "difficulty": character["difficulty"]}
          json_file.write(json.dumps(to_write))
    elif option == "/q":
      exit()
    option = input()
    if option == "/b":
      break 
  
def game_process(character_stats=""):
  
  if character_stats:
    user_stats["stats"] = character_stats["character"]
    user_stats["bag"] = character_stats["inventory"]
    user_stats["lives"] = character_stats["lives"]
    user_stats["difficulty"] = character_stats["difficulty"]
    cur_level, cur_scene = list(character_stats["progress"].values())

  with open(r"data\story2.json", "r") as json_file:
    story = json.load(json_file)
  
  def level(level_num):

    scenes = story[f"level{level_num}"]["scenes"]
    next_scene = "scene1" if not character_stats else cur_scene
      
    while next_scene != "end":
      if character_stats:
        print(f"------ Level {int(level_num) + 1} ------\n")
      print(scenes[next_scene]["text"])
      scene_options = scenes[next_scene]["options"]
      for ind, option in enumerate(scene_options, 1):
        print(f"{ind}. {check_items(option["option_text"], user_stats["bag"])}")
      user_choice = input_checker(input("\n"), [str(i) for i in range(1, len(scene_options) + 1)] + ["/h", "/c", "/i", "/s", "/b", "/q"])
      if user_choice.isdigit():
        user_choice = int(user_choice) - 1
      elif user_choice == "/b":
        break
      else:
        user_choice = inner_menu(user_stats, user_choice, next_scene, level_num)
        continue
      result_text = scene_options[user_choice]["result_text"]
      result_text = check_items(result_text, user_stats["bag"])
      actions = scene_options[user_choice]["actions"]
      next_scene = scene_options[user_choice]["next"] 
      print(f"\n{result_text}")
      for i in actions:
        item = i.strip("-+}{")
        if item in user_stats["bag"]:
          if i.startswith("-"):
            user_stats["bag"][item] = ""
            print(f"------ Item removed: {item} ------")
          else:
            user_stats["bag"][item] += item
            print(f"------ Item added: {item} ------")
        elif item == "heal" or item == "hit": 
          if item == "heal":
            user_stats["lives"] += 1
            print(f"------ Lives remaining: {user_stats["lives"]} ------")
          elif item == "hit":
            user_stats["lives"] -= 1
            print(f"------ Lives remaining: {user_stats["lives"]} ------")
        elif item not in user_stats["bag"]:
          print(f"------ Item added: {item} ------\n")
    print(f"------ Level {int(level_num) + 1} ------\n")
  
  for i in range(1 if not character_stats else int(cur_level[-1]), len([i for i in story])):
    if i != 3:
      level(i)
    else:
      return
      
def check_items(text, where):
  if "{" in text:
    start, end = text.find("{"), text.find("}")
    element = text[start + 1:end]
    text = text[:start] + where[element] + text[end + 1:]
  return text

def load_game():
  all_files = [i.replace(".json", "") for i in os.listdir("./data/saves")]
  print("Choose username (/b - back):\n")
  print(*all_files, sep="\n")
  while True:
    user_choice = input("\n")
    if user_choice == "/b":
      return
    elif user_choice not in all_files:
      continue
    else:
      with open(f".\\data\\saves\\{user_choice}.json", "r") as file:
        stats = json.load(file)
      print("Loading your progress...")
      return stats
    
user_stats = {"stars":"", "bag":"", "difficulty":"", "user_name":"", "lives":""}
user_choice = ""

while user_choice != "3":
  print("***Welcome to the Journey to Mount Qaf***\n")
  user_choice = menu()
  if user_choice == "1":
    user_stats = new_game()
    if user_stats == None:
      continue
    game = game_process()
  elif user_choice == "2":
    game_process(load_game())
  elif user_choice == "3":
    print("Bye")
    break