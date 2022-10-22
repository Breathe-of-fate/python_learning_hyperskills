import sqlite3
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('db_name', type=str)
parser.add_argument('--ingredients', type=str)
parser.add_argument('--meals', type=str)
args = parser.parse_args()

open_db = sqlite3.connect(args.db_name)
modify_db = open_db.cursor()
modify_db.executescript("""PRAGMA foreign_keys = ON;
                           CREATE TABLE IF NOT EXISTS meals       (meal_id INTEGER PRIMARY KEY , meal_name TEXT UNIQUE NOT NULL);
                           CREATE TABLE IF NOT EXISTS ingredients (ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT UNIQUE NOT NULL);
                           CREATE TABLE IF NOT EXISTS measures    (measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE);
                           CREATE TABLE IF NOT EXISTS recipes     (recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT);
                           CREATE TABLE IF NOT EXISTS serve       (serve_id INTEGER PRIMARY KEY, recipe_id INTEGER NOT NULL, meal_id INTEGER NOT NULL,
                                                                   CONSTRAINT FK_meal
                                                                   FOREIGN KEY (meal_id) REFERENCES meals (meal_id),
                                                                   CONSTRAINT FK_reci
                                                                   FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id));
                           CREATE TABLE IF NOT EXISTS quantity     (quantity_id INTEGER PRIMARY KEY,
                                                                   measure_id INTEGER NOT NULL,
                                                                   ingredient_id INTEGER NOT NULL,
                                                                   quantity INTEGER NOT NULL,
                                                                   recipe_id INTEGER NOT NULL,
                                                                   CONSTRAINT FK_measure
                                                                   FOREIGN KEY (measure_id) REFERENCES measures (measure_id),
                                                                   CONSTRAINT FK_ingredient
                                                                   FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id),
                                                                   CONSTRAINT FK_recipe
                                                                   FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id));""")

def last_filled_row(x):
    return len(modify_db.execute(f"SELECT * FROM {x}").fetchall()) + 1

def search_for_id(x, y):
    req = modify_db.execute(f"SELECT {x}_id FROM {x}s WHERE {x}_name LIKE '%{y}%'").fetchone()
    if req is not None:
        for i in req:
            return i
    return None

def one_tuple_query(x):
    res = [i[0] for i in x]
    if len(res) == 1:
        res.append("0")
    return tuple(res)

def tuples_len(x):
    return 1 if "0" in x else len(x)

def handle_args(x):
    h_a = x.split(",")
    if len(h_a) == 1:
        h_a.append("0")
    return tuple(h_a)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

if args.ingredients and args.meals:

    if len([i for i in args.ingredients.split(",") if i in data["ingredients"]]) < len(args.ingredients.split(",")):
        print("There are no such recipes in the database.")
    else:
        ingredient_id = one_tuple_query(modify_db.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient_name IN {handle_args(args.ingredients)}"))
        recipe_id = one_tuple_query(modify_db.execute(f"SELECT recipe_id FROM quantity WHERE ingredient_id IN {ingredient_id} GROUP BY recipe_id HAVING COUNT(recipe_id) = {tuples_len(ingredient_id)}"))
        meal_id = one_tuple_query(modify_db.execute(f"SELECT DISTINCT meal_id FROM serve WHERE recipe_id IN {recipe_id}"))
        meal_names = one_tuple_query(modify_db.execute(f"SELECT meal_name FROM meals WHERE meal_id IN {meal_id}"))
        print(f"Recipes selected for you:", str(one_tuple_query(modify_db.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id IN {recipe_id}"))).replace("(", "").replace(")", "").replace("'", ""))

else:

    for i in data.keys():
        for ii in data[i]:
            modify_db.execute(f"INSERT INTO {i} VALUES (?, ?)", (last_filled_row(i), ii))
    open_db.commit()

    res_name = input("Pass the empty recipe name to exit.\nRecipe name: ")
    while res_name != "":

        last_row = modify_db.execute("INSERT INTO recipes VALUES(?, ?, ?)", (last_filled_row("recipes"), res_name, input('Recipe description: '))).lastrowid
        print("1) breakfast  2) brunch  3) lunch  4) supper")
        for i in input("Enter proposed meals separated by a space: ").split():
            modify_db.execute("INSERT INTO serve VALUES(?, ?, ?)", (last_filled_row("serve"), last_row, i))

        user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()
        while len(user_choice) > 0:

            if len(user_choice) == 3:
                if search_for_id("measure", user_choice[1]) is None:
                    print("The name of measure is not conclusive!")
                    user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()
                    continue
                elif search_for_id("ingredient", user_choice[2]) is None:
                    print("The name of ingredient is not conclusive!")
                    user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()
                    continue
                else:
                    to_input = last_filled_row("quantity"), search_for_id("measure", user_choice[1]), search_for_id("ingredient", user_choice[2]), user_choice[0], last_row
                    modify_db.execute("INSERT INTO quantity VALUES (?, ?, ?, ?, ?)", (to_input))
                user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()
            else:
                if search_for_id("ingredient", user_choice[1]) is None:
                    print("The name of ingredient is not conclusive!")
                    user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()
                    continue
                else:
                    to_input = last_filled_row("quantity"), search_for_id("measure", ""), search_for_id("ingredient", user_choice[1]), user_choice[0], last_row
                    modify_db.execute("INSERT INTO quantity VALUES (?, ?, ?, ?, ?)", (to_input))
                user_choice = input("Input quantity of ingredient <press enter to stop>: ").split()

        res_name = input("Recipe name: ")

open_db.commit()
open_db.close()